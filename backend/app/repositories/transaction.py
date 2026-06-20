from uuid import UUID
from app.models.models import Transaction
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class TransactionRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_user_id(self, user_id: UUID) -> list[Transaction]:
        stmt = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.transaction_date.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, tx_id: UUID) -> Transaction | None:
        stmt = select(Transaction).where(Transaction.id == tx_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, user_id: UUID, tx_data: dict) -> Transaction:
        db_tx = Transaction(user_id=user_id, **tx_data)
        self.db.add(db_tx)
        await self.db.commit()
        await self.db.refresh(db_tx)
        return db_tx

    async def delete(self, tx: Transaction) -> None:
        await self.db.delete(tx)
        await self.db.commit()
