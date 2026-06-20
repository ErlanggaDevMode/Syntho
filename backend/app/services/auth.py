import hashlib
import hmac
import logging
from typing import Any

from app.core.config import settings
from app.core.security import create_access_token
from app.repositories.user import UserRepository

logger = logging.getLogger(__name__)


def verify_telegram_hash(auth_data: dict[str, Any], bot_token: str) -> bool:
    """Validate signature hash of Telegram Login Widget auth data."""
    check_hash = auth_data.get("hash")
    if not check_hash:
        return False

    # Create sorted data check string
    data_check_list = []
    for k, v in sorted(auth_data.items()):
        if k != "hash" and v is not None:
            data_check_list.append(f"{k}={v}")
    data_check_string = "\n".join(data_check_list)

    # Compute secret key
    secret_key = hashlib.sha256(bot_token.encode()).digest()

    # Compute hash
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(calculated_hash, check_hash)


class AuthService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_telegram(self, auth_data: dict[str, Any]) -> str | None:
        """Authenticate user using Telegram login widget payload.

        Returns JWT access token if validation passes, else None.
        """
        if not verify_telegram_hash(auth_data, settings.TELEGRAM_BOT_TOKEN):
            logger.warning("Telegram authentication signature check failed.")
            return None

        telegram_id = auth_data["id"]
        username = auth_data.get("username")
        first_name = auth_data.get("first_name", "")
        last_name = auth_data.get("last_name", "")
        full_name = f"{first_name} {last_name}".strip() or None

        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            logger.info(f"Creating new user for Telegram ID: {telegram_id}")
            user = await self.user_repo.create(
                telegram_id=telegram_id,
                username=username,
                full_name=full_name,
            )

        # Issue access token containing sub claim set to user ID
        token = create_access_token({"sub": str(user.id)})
        return token
