from uuid import UUID
from app.models.models import Reminder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ReminderRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_user_id(self, user_id: UUID) -> list[Reminder]:
        stmt = (
            select(Reminder)
            .where(Reminder.user_id == user_id)
            .order_by(Reminder.due_date.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, reminder_id: UUID) -> Reminder | None:
        stmt = select(Reminder).where(Reminder.id == reminder_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, user_id: UUID, reminder_data: dict) -> Reminder:
        db_reminder = Reminder(user_id=user_id, **reminder_data)
        self.db.add(db_reminder)
        await self.db.commit()
        await self.db.refresh(db_reminder)
        return db_reminder

    async def delete(self, reminder: Reminder) -> None:
        await self.db.delete(reminder)
        await self.db.commit()
