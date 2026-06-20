from typing import Annotated

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import User
from app.repositories.user import UserRepository
from app.schemas.auth import TelegramAuthInput, TokenResponse, UserResponse
from app.services.auth import AuthService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/telegram", response_model=TokenResponse)
async def login_telegram(
    auth_data: TelegramAuthInput,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Authenticate user details retrieved from the Telegram Login Widget.

    If validation signature checks succeed, get or create the user and issue
    a JWT access token.
    """
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    token = await auth_service.authenticate_telegram(auth_data.model_dump())
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed. Invalid login widget signature.",
        )

    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    """Retrieve details of the currently authenticated user."""
    return current_user
