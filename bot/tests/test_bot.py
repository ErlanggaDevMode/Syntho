from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.handlers.handlers import handle_message


@pytest.mark.asyncio
async def test_bot_message_handler_relay():
    # Mock update message and user details
    mock_update = MagicMock()
    mock_update.message = MagicMock()
    mock_update.message.text = "Bought coffee for 20k"
    mock_update.message.chat_id = 112233
    mock_update.message.reply_text = AsyncMock()  # Async mock to support await

    mock_user = MagicMock()
    mock_user.id = 123456
    mock_user.username = "testuser"
    mock_user.first_name = "Test"
    mock_user.last_name = "User"
    mock_update.message.from_user = mock_user

    mock_context = MagicMock()

    # Mock send_message_to_backend to return a mock string
    with patch(
        "app.handlers.handlers.send_message_to_backend", new_callable=AsyncMock
    ) as mock_send:
        mock_send.return_value = "Success response from backend!"

        # Invoke handler
        await handle_message(mock_update, mock_context)

        # Verify send_message_to_backend was called with correct parameters
        mock_send.assert_called_once_with(
            telegram_id=123456,
            username="testuser",
            full_name="Test User",
            text="Bought coffee for 20k",
        )

        # Verify reply was sent back
        mock_update.message.reply_text.assert_called_once_with(
            "Success response from backend!"
        )
