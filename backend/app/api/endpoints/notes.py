from typing import Annotated
from uuid import UUID

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import User
from app.repositories.note import NoteRepository
from app.schemas.note import NoteCreate, NoteResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteResponse])
async def read_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Retrieve all notes associated with the current user."""
    note_repo = NoteRepository(db)
    return await note_repo.get_all_by_user_id(current_user.id)


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_user_note(
    payload: NoteCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a new note for the current user."""
    note_repo = NoteRepository(db)
    # The note from the web UI doesn't run through the AI automatically,
    # but we can set a basic summary placeholder for notes added manually.
    note_data = payload.model_dump()
    if "summary" not in note_data or not note_data["summary"]:
        note_data["summary"] = (payload.title or "Catatan manual") + " summary..."
    return await note_repo.create(current_user.id, note_data)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_note(
    note_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete a note by its UUID if it belongs to the current user."""
    note_repo = NoteRepository(db)
    note = await note_repo.get_by_id(note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or unauthorized.",
        )
    await note_repo.delete(note)
