import logging
import sys

from app.core.config import settings
from app.handlers.handlers import handle_message
from telegram.ext import Application, MessageHandler, filters

# Setup logging to stdout
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger("syntho-bot")


def main() -> None:
    """Start the bot."""
    logger.info("Initializing Telegram Bot...")

    # Build python-telegram-bot application
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Relay all text and command messages to a single unified handler
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    )
    application.add_handler(MessageHandler(filters.COMMAND, handle_message))

    # Run bot based on configured mode
    if settings.TELEGRAM_BOT_MODE == "webhook":
        logger.info("Running Bot in Webhook Mode.")
        # Webhook requires public URL and SSL, config port and listen address
        application.run_webhook(
            listen="0.0.0.0",
            port=8080,
            secret_token=settings.TELEGRAM_WEBHOOK_SECRET,
        )
    else:
        logger.info("Running Bot in Polling Mode.")
        application.run_polling()


if __name__ == "__main__":
    main()
