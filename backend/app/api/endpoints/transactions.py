from typing import Annotated
from uuid import UUID

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import User
from app.repositories.transaction import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionResponse])
async def read_transactions(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Retrieve all transactions associated with the current user."""
    tx_repo = TransactionRepository(db)
    return await tx_repo.get_all_by_user_id(current_user.id)


@router.post(
    "", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED
)
async def create_user_transaction(
    payload: TransactionCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a new transaction for the current user."""
    tx_repo = TransactionRepository(db)
    return await tx_repo.create(current_user.id, payload.model_dump())


@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_transaction(
    tx_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete a transaction by its UUID if it belongs to the current user."""
    tx_repo = TransactionRepository(db)
    tx = await tx_repo.get_by_id(tx_id)
    if not tx or tx.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found or unauthorized.",
        )
    await tx_repo.delete(tx)
