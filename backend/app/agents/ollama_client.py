import json
import logging
from typing import Type, TypeVar

import httpx
from app.core.config import settings
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


async def query_ollama(
    prompt: str,
    system_prompt: str | None = None,
    response_model: Type[T] | None = None,
    json_mode: bool = False,
) -> str | T:
    """Send a generation request to the local Ollama instance.

    If response_model is provided, forces JSON format, validates the result
    against the Pydantic schema, and returns the instantiated schema.
    """
    url = f"{settings.OLLAMA_HOST}/api/generate"
    format_opt = "json" if (response_model or json_mode) else None

    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0,  # Deterministic output for structured data
        },
    }
    if system_prompt:
        payload["system"] = system_prompt
    if format_opt:
        payload["format"] = format_opt

    try:
        async with httpx.AsyncClient(timeout=float(settings.AI_TIMEOUT)) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()

            raw_response = response.json().get("response", "").strip()

            if response_model:
                try:
                    parsed_json = json.loads(raw_response)
                    return response_model.model_validate(parsed_json)
                except (json.JSONDecodeError, ValidationError) as e:
                    logger.error(
                        f"Failed to parse or validate AI output: {raw_response}. Error: {e}"
                    )
                    raise ValueError(
                        "AI response structure could not be parsed into target schema."
                    ) from e

            return raw_response

    except httpx.RequestError as e:
        logger.error(f"Ollama connection request failed: {e}")
        raise RuntimeError(
            "AI inference engine is currently offline or unreachable."
        ) from e
