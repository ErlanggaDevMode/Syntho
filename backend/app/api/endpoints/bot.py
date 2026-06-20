from datetime import datetime, timedelta
import logging
from typing import Annotated

from app.agents.agents import (
    ExpenseAgent,
    FallbackAgent,
    NoteAgent,
    ReminderAgent,
    ReportAgent,
    RouterAgent,
)
from app.core.config import settings
from app.core.database import get_db
from app.models.models import utc_now
from app.repositories.note import NoteRepository
from app.repositories.reminder import ReminderRepository
from app.repositories.transaction import TransactionRepository
from app.repositories.user import UserRepository
from app.schemas.bot import BotMessageInput, BotMessageResponse
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bot", tags=["bot"])


def verify_bot_secret(x_bot_secret: str = Header(..., alias="X-Bot-Secret")):
    """Ensure that the caller possesses the shared webhook secret."""
    if x_bot_secret != settings.TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid bot secret token.",
        )


@router.post(
    "/message",
    response_model=BotMessageResponse,
    dependencies=[Depends(verify_bot_secret)],
)
async def handle_bot_message(
    payload: BotMessageInput,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Handle incoming messages routed from the Telegram bot.

    Parses the message using AI agents, registers/finds the user, performs
    database CRUD operations, and replies with structured responses.
    """
    user_repo = UserRepository(db)

    # Automatically register user if not exists
    user = await user_repo.get_by_telegram_id(payload.telegram_id)
    if not user:
        user = await user_repo.create(
            telegram_id=payload.telegram_id,
            username=payload.username,
            full_name=payload.full_name,
        )

    text = payload.text.strip()

    # Handlers for static commands
    if text == "/start":
        response_text = (
            f"Halo {user.full_name or 'Pengguna'}! Selamat datang di Syntho.\n\n"
            "Saya adalah asisten AI pribadi Anda untuk mencatat pengeluaran dan catatan.\n"
            "Kirimkan pesan seperti:\n"
            "- 'Beli kopi 20 ribu'\n"
            "- 'Gaji masuk 3 juta'\n"
            "- 'Ide: dashboard inventaris'\n\n"
            "Ketik /help untuk info lebih lanjut."
        )
        return BotMessageResponse(response_text=response_text)

    elif text == "/help":
        response_text = (
            "💡 **Panduan Penggunaan Syntho**\n\n"
            "💵 **Mencatat Transaksi**:\n"
            "- 'Beli bensin 50 ribu pakai QRIS'\n"
            "- 'Makan siang 25k'\n\n"
            "📝 **Mencatat Catatan**:\n"
            "- 'Catatan: rapat kerja hari Senin'\n"
            "- 'Ide: bisnis cafe'\n\n"
            "📊 **Laporan**:\n"
            "- /report atau /summary untuk melihat laporan bulanan."
        )
        return BotMessageResponse(response_text=response_text)

    # Core AI Multi-Agent parsing workflow
    try:
        router_output = await RouterAgent.run(text)
        intent = router_output.intent

        # Determine report intent by text matching as well for direct commands
        if text in ("/report", "/summary"):
            intent = "report"

        if intent in ("expense", "income"):
            expense_data = await ExpenseAgent.run(text)
            tx_repo = TransactionRepository(db)
            tx_date = utc_now()
            if expense_data.transaction_date:
                try:
                    tx_date = datetime.fromisoformat(expense_data.transaction_date)
                except ValueError:
                    pass
            await tx_repo.create(
                user_id=user.id,
                tx_data={
                    "type": expense_data.intent,
                    "amount": expense_data.amount,
                    "category": expense_data.category or "Lainnya",
                    "description": expense_data.description or text,
                    "payment_method": expense_data.payment_method or "Tunai",
                    "transaction_date": tx_date,
                },
            )
            response_text = (
                f"✅ **Transaksi Berhasil Dicatat**\n"
                f"- Tipe: {expense_data.intent.capitalize()}\n"
                f"- Nominal: Rp{expense_data.amount:,.0f}\n"
                f"- Kategori: {expense_data.category or 'Lainnya'}\n"
                f"- Deskripsi: {expense_data.description or text}\n"
                f"- Pembayaran: {expense_data.payment_method or 'Tunai'}"
            )

        elif intent == "note":
            note_data = await NoteAgent.run(text)
            note_repo = NoteRepository(db)
            await note_repo.create(
                user_id=user.id,
                note_data={
                    "title": note_data.title,
                    "content": text,
                    "tags": note_data.tags,
                    "summary": note_data.summary,
                },
            )
            response_text = (
                f"📝 **Catatan Disimpan**\n"
                f"- Judul: {note_data.title}\n"
                f"- Ringkasan: {note_data.summary}\n"
                f"- Tag: {', '.join(note_data.tags) if note_data.tags else '-'}"
            )

        elif intent == "reminder":
            reminder_data = await ReminderAgent.run(text)
            reminder_repo = ReminderRepository(db)
            due_date = None
            if reminder_data.due_date:
                try:
                    due_date = datetime.fromisoformat(reminder_data.due_date)
                except ValueError:
                    pass
            if not due_date:
                due_date = datetime.now() + timedelta(days=1)
            await reminder_repo.create(
                user_id=user.id,
                reminder_data={
                    "title": reminder_data.title,
                    "due_date": due_date.replace(tzinfo=None),
                    "status": "pending",
                },
            )
            response_text = (
                f"⏰ **Pengingat Diset**\n"
                f"- Judul: {reminder_data.title}\n"
                f"- Waktu: {due_date.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        elif intent == "report":
            tx_repo = TransactionRepository(db)
            txs = await tx_repo.get_all_by_user_id(user.id)
            summary_lines = []
            for tx in txs[:20]:
                summary_lines.append(
                    f"- {tx.transaction_date.strftime('%Y-%m-%d')}: {tx.type.capitalize()} Rp{tx.amount:,.0f} - {tx.description} ({tx.category})"
                )
            transactions_summary = (
                "\n".join(summary_lines) if summary_lines else "Tidak ada transaksi."
            )
            report_text = await ReportAgent.run(transactions_summary)
            response_text = f"📊 **Laporan Analisis AI**:\n\n{report_text}"

        else:
            # intent == "unknown" or other fallbacks
            response_text = await FallbackAgent.run(text)

    except Exception as e:
        logger.exception("Failed to process message using AI agent system.")
        response_text = (
            "⚠️ Mohon maaf, terjadi gangguan saat memproses pesan Anda dengan AI. "
            "Pesan Anda gagal dianalisis."
        )

    return BotMessageResponse(response_text=response_text)
