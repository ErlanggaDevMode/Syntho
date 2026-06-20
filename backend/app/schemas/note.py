from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None


class NoteCreate(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: UUID
    user_id: UUID
    summary: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
