from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TelegramAuthInput(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    auth_date: int
    hash: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    telegram_id: int
    username: str | None = None
    full_name: str | None = None
    timezone: str
    created_at: datetime
