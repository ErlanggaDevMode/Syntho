import hashlib
import hmac
import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.core.config import settings
from app.main import app
from app.services.auth import verify_telegram_hash
from httpx import ASGITransport, AsyncClient


def test_verify_telegram_hash():
    bot_token = "test_bot_token"
    auth_data = {
        "id": 123456,
        "first_name": "Test",
        "username": "testuser",
        "auth_date": 1458238123,
    }

    # Generate valid hash
    data_check_list = []
    for k, v in sorted(auth_data.items()):
        data_check_list.append(f"{k}={v}")
    data_check_string = "\n".join(data_check_list)

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    auth_data_with_hash = auth_data.copy()
    auth_data_with_hash["hash"] = calculated_hash

    # Signature must be valid
    assert verify_telegram_hash(auth_data_with_hash, bot_token) is True

    # Signature must be invalid for incorrect data
    auth_data_invalid = auth_data_with_hash.copy()
    auth_data_invalid["username"] = "attacker"
    assert verify_telegram_hash(auth_data_invalid, bot_token) is False


@pytest.mark.asyncio
async def test_auth_endpoints():
    bot_token = settings.TELEGRAM_BOT_TOKEN
    auth_data = {
        "id": 999999,
        "first_name": "Auth",
        "last_name": "User",
        "username": "authuser",
        "auth_date": 1458238123,
    }

    # Generate a valid hash for the test bot token
    data_check_list = []
    for k, v in sorted(auth_data.items()):
        data_check_list.append(f"{k}={v}")
    data_check_string = "\n".join(data_check_list)

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    auth_data_with_hash = auth_data.copy()
    auth_data_with_hash["hash"] = calculated_hash

    # We mock the DB session and repository to run unit test without real DB
    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_user.telegram_id = 999999
    mock_user.username = "authuser"
    mock_user.full_name = "Auth User"
    mock_user.timezone = "Asia/Jakarta"
    mock_user.created_at = datetime.now(UTC).replace(tzinfo=None)

    with patch(
        "app.repositories.user.UserRepository.get_by_telegram_id",
        new_callable=AsyncMock,
    ) as mock_get_by_tg, patch(
        "app.repositories.user.UserRepository.create", new_callable=AsyncMock
    ) as mock_create, patch(
        "app.repositories.user.UserRepository.get_by_id", new_callable=AsyncMock
    ) as mock_get_by_id:

        mock_get_by_tg.return_value = None
        mock_create.return_value = mock_user
        mock_get_by_id.return_value = mock_user

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            # 1. Post to login
            response = await ac.post("/api/v1/auth/telegram", json=auth_data_with_hash)
            assert response.status_code == 200
            token_data = response.json()
            assert "access_token" in token_data
            assert token_data["token_type"] == "bearer"

            # 2. Get /me with the token
            access_token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            me_response = await ac.get("/api/v1/auth/me", headers=headers)
            assert me_response.status_code == 200
            user_data = me_response.json()
            assert user_data["username"] == "authuser"
            assert user_data["telegram_id"] == 999999
