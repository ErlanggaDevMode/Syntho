from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class TransactionBase(BaseModel):
    type: Literal["expense", "income"]
    amount: float
    category: str | None = None
    description: str | None = None
    payment_method: str | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID
    transaction_date: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
