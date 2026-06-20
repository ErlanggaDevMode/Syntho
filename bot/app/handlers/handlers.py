import logging

from app.core.api import send_message_to_backend
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward command or text message to backend and reply with backend output."""
    if not update.message or not update.message.text:
        return

    user = update.message.from_user
    text = update.message.text

    if not user:
        return

    username = user.username
    full_name = f"{user.first_name} {user.last_name or ''}".strip()

    # Log incoming message
    logger.info(f"Incoming message from TG user {user.id}: {text}")

    # Call backend API
    response_text = await send_message_to_backend(
        telegram_id=user.id,
        username=username,
        full_name=full_name,
        text=text,
    )

    # Reply to Telegram user
    await update.message.reply_text(response_text)
