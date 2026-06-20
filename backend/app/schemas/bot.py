from pydantic import BaseModel


class BotMessageInput(BaseModel):
    telegram_id: int
    username: str | None = None
    full_name: str | None = None
    text: str


class BotMessageResponse(BaseModel):
    response_text: str
