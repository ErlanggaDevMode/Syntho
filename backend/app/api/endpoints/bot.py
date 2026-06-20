from typing import Annotated

from app.core.config import settings
from app.core.database import get_db
from app.repositories.user import UserRepository
from app.schemas.bot import BotMessageInput, BotMessageResponse
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

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

    Registers new users and acts as a placeholder routing target for Step 6.
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

    # Simple command handling routing (business logic in backend)
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
    elif text in ("/report", "/summary"):
        response_text = (
            "📊 **Laporan Bulanan (Placeholder)**\n\n"
            "Total Pengeluaran: Rp0\n"
            "Total Pemasukan: Rp0\n\n"
            "AI parsing dan analisis data penuh akan segera hadir!"
        )
    else:
        response_text = (
            f'Pesan diterima: "{text}"\n\n'
            "Pesan akan dianalisis oleh AI di langkah selanjutnya."
        )

    return BotMessageResponse(response_text=response_text)
