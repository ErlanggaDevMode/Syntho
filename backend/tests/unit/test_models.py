import uuid
from datetime import UTC, datetime

from app.core.database import Base
from app.models.models import Note, Reminder, Transaction, User
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker


# Compilation hooks to support Postgres-specific types on SQLite during tests
@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(element, compiler, **kw):
    return "JSON"


@compiles(UUID, "sqlite")
def compile_uuid_sqlite(element, compiler, **kw):
    return "VARCHAR(36)"


def test_models_schema():
    # Set up in-memory synchronous SQLite database
    engine = create_engine("sqlite:///:memory:")
    # Verify that metadata can create all tables on SQLite
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Create a test user
        user = User(
            id=uuid.uuid4(),
            telegram_id=123456789,
            username="testuser",
            full_name="Test User",
            timezone="Asia/Jakarta",
        )
        session.add(user)
        session.commit()

        # Create a transaction
        tx = Transaction(
            id=uuid.uuid4(),
            user_id=user.id,
            type="expense",
            amount=25000.00,
            category="Food",
            description="Lunch",
            payment_method="Cash",
            transaction_date=datetime.now(UTC).replace(tzinfo=None),
        )
        session.add(tx)

        # Create a note
        note = Note(
            id=uuid.uuid4(),
            user_id=user.id,
            title="Test Note",
            content="This is a test note content.",
            tags=["test", "pytest"],
            summary="Test summary",
        )
        session.add(note)

        # Create a reminder
        reminder = Reminder(
            id=uuid.uuid4(),
            user_id=user.id,
            title="Pay Electricity",
            due_date=datetime.now(UTC).replace(tzinfo=None),
            status="pending",
        )
        session.add(reminder)

        session.commit()

        # Queries to verify relationship populating
        db_user = session.query(User).filter_by(telegram_id=123456789).first()
        assert db_user is not None
        assert len(db_user.transactions) == 1
        assert db_user.transactions[0].amount == 25000.00
        assert len(db_user.notes) == 1
        assert db_user.notes[0].title == "Test Note"
        assert len(db_user.reminders) == 1
        assert db_user.reminders[0].status == "pending"

    finally:
        session.close()
