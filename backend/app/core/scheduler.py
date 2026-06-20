import logging
from datetime import datetime, timedelta
import httpx
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.models import Reminder, User, Transaction
from app.agents.agents import ReportAgent

logger = logging.getLogger("syntho-scheduler")

scheduler = AsyncIOScheduler()


async def send_telegram_message(telegram_id: int, text: str) -> None:
    """Send a text message directly using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": telegram_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to send message to Telegram user {telegram_id}: {e}")


async def process_due_reminders():
    """Find pending reminders that are due and notify users."""
    logger.debug("Checking for due reminders...")
    async with SessionLocal() as db:
        now = datetime.now()
        stmt = (
            select(Reminder)
            .options(selectinload(Reminder.user))
            .where(Reminder.status == "pending")
            .where(Reminder.due_date <= now)
        )
        result = await db.execute(stmt)
        reminders = result.scalars().all()

        for reminder in reminders:
            user = reminder.user
            if user and user.telegram_id:
                msg = f"⏰ **Pengingat Penting!**\n\n📌 *{reminder.title}*\n📅 Jatuh tempo pada: {reminder.due_date.strftime('%Y-%m-%d %H:%M:%S')}"
                await send_telegram_message(user.telegram_id, msg)
                reminder.status = "completed"

        if reminders:
            await db.commit()


async def send_scheduled_report(period: str):
    """Generate and dispatch financial summary report to all users."""
    logger.info(f"Triggered scheduled {period} reports generation.")
    async with SessionLocal() as db:
        # Fetch all users
        result = await db.execute(select(User))
        users = result.scalars().all()

        for user in users:
            if not user.telegram_id:
                continue

            now = datetime.now()
            if period == "daily":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == "weekly":
                start_date = now - timedelta(days=7)
            else:
                # monthly
                start_date = now - timedelta(days=30)

            # Retrieve transactions
            tx_stmt = (
                select(Transaction)
                .where(Transaction.user_id == user.id)
                .where(Transaction.transaction_date >= start_date)
            )
            tx_res = await db.execute(tx_stmt)
            txs = tx_res.scalars().all()

            if not txs and period in ("weekly", "monthly"):
                # Avoid spamming empty weekly/monthly reports
                continue

            summary_lines = []
            total_expense = 0.0
            total_income = 0.0
            for tx in txs:
                summary_lines.append(
                    f"- {tx.transaction_date.strftime('%Y-%m-%d')}: {tx.type.capitalize()} Rp{tx.amount:,.0f} - {tx.description} ({tx.category})"
                )
                if tx.type == "expense":
                    total_expense += float(tx.amount)
                else:
                    total_income += float(tx.amount)

            transactions_summary = "\n".join(summary_lines)

            # Determine title headers
            if period == "daily":
                header = f"📋 **Laporan Harian ({now.strftime('%d %B %Y')})**\n\n"
            elif period == "weekly":
                header = f"📋 **Laporan Mingguan (7 Hari Terakhir)**\n\n"
            else:
                header = f"📋 **Laporan Bulanan (30 Hari Terakhir)**\n\n"

            header += (
                f"💵 Total Pemasukan: Rp{total_income:,.0f}\n"
                f"💸 Total Pengeluaran: Rp{total_expense:,.0f}\n"
                f"⚖️ Saldo Bersih: Rp{(total_income - total_expense):,.0f}\n\n"
            )

            # Request advice from AI Agent
            try:
                ai_advice = await ReportAgent.run(
                    transactions_summary or "Tidak ada transaksi tercatat."
                )
                report_msg = header + ai_advice
            except Exception as e:
                logger.error(f"ReportAgent fail: {e}")
                report_msg = (
                    header
                    + "💡 *Tip Keuangan:* Catat transaksi harian secara konsisten melalui Telegram."
                )

            await send_telegram_message(user.telegram_id, report_msg)


def start_scheduler():
    """Start the APScheduler job queues."""
    # Check reminders every minute
    scheduler.add_job(process_due_reminders, "interval", minutes=1, id="reminder_job")
    # Daily reports at 9:00 PM (21:00)
    scheduler.add_job(
        send_scheduled_report,
        CronTrigger(hour=21, minute=0),
        args=["daily"],
        id="daily_report_job",
    )
    # Weekly reports at 9:05 PM on Sunday
    scheduler.add_job(
        send_scheduled_report,
        CronTrigger(day_of_week="sun", hour=21, minute=5),
        args=["weekly"],
        id="weekly_report_job",
    )
    # Monthly reports at 9:00 AM on the 1st of every month
    scheduler.add_job(
        send_scheduled_report,
        CronTrigger(day=1, hour=9, minute=0),
        args=["monthly"],
        id="monthly_report_job",
    )

    scheduler.start()
    logger.info("APScheduler background service started.")


def shutdown_scheduler():
    """Stop the APScheduler job queues."""
    scheduler.shutdown()
    logger.info("APScheduler background service shutdown.")
