from uuid import UUID
from app.models.models import Note
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class NoteRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_user_id(self, user_id: UUID) -> list[Note]:
        stmt = (
            select(Note)
            .where(Note.user_id == user_id)
            .order_by(Note.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, note_id: UUID) -> Note | None:
        stmt = select(Note).where(Note.id == note_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, user_id: UUID, note_data: dict) -> Note:
        db_note = Note(user_id=user_id, **note_data)
        self.db.add(db_note)
        await self.db.commit()
        await self.db.refresh(db_note)
        return db_note

    async def delete(self, note: Note) -> None:
        await self.db.delete(note)
        await self.db.commit()
