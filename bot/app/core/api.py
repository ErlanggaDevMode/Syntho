import logging

import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_message_to_backend(
    telegram_id: int,
    username: str | None,
    full_name: str | None,
    text: str,
) -> str:
    """Send text message details to the backend API and get response.

    Translates all user inputs to backend commands securely.
    """
    payload = {
        "telegram_id": telegram_id,
        "username": username,
        "full_name": full_name,
        "text": text,
    }
    headers = {"X-Bot-Secret": settings.TELEGRAM_WEBHOOK_SECRET}

    url = f"{settings.BACKEND_API_URL}/bot/message"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get(
                    "response_text",
                    "Error: No response text returned from backend.",
                )
            else:
                logger.error(
                    f"Backend API error ({response.status_code}): {response.text}"
                )
                return f"Maaf, terjadi kesalahan pada server backend (HTTP {response.status_code})."
    except httpx.RequestError as e:
        # Fallback to localhost if backend is not resolved (useful for local development)
        if "backend" in url:
            alt_url = url.replace("backend:8000", "localhost:8000")
            logger.info(f"Retrying connection using alternate URL: {alt_url}")
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(alt_url, json=payload, headers=headers)
                    if response.status_code == 200:
                        return response.json().get("response_text")
            except httpx.RequestError:
                pass

        logger.error(f"Failed to connect to backend: {e}")
        return "Maaf, tidak dapat menghubungkan ke asisten Syntho saat ini."
