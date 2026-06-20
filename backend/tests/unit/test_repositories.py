import uuid

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repositories.user import UserRepository
from app.repositories.transaction import TransactionRepository
from app.repositories.note import NoteRepository
from app.repositories.reminder import ReminderRepository


@pytest.mark.asyncio
async def test_user_repository_mock():
    mock_db = AsyncMock()
    mock_res = MagicMock()
    mock_res.scalars.return_value.first.return_value = "mock_user"
    mock_db.execute.return_value = mock_res

    repo = UserRepository(mock_db)

    # 1. get_by_telegram_id
    user = await repo.get_by_telegram_id(12345)
    assert user == "mock_user"

    # 2. get_by_id
    user_by_id = await repo.get_by_id(uuid.uuid4())
    assert user_by_id == "mock_user"

    # 3. create
    created = await repo.create(
        telegram_id=12345, username="test", full_name="Test"
    )
    assert created.telegram_id == 12345
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_transaction_repository_mock():
    mock_db = AsyncMock()
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = ["tx1", "tx2"]
    mock_res.scalars.return_value.first.return_value = "tx_first"
    mock_db.execute.return_value = mock_res

    repo = TransactionRepository(mock_db)

    # 1. get_all_by_user_id
    txs = await repo.get_all_by_user_id(uuid.uuid4())
    assert len(txs) == 2
    assert txs[0] == "tx1"

    # 2. get_by_id
    tx = await repo.get_by_id(uuid.uuid4())
    assert tx == "tx_first"

    # 3. create
    created = await repo.create(user_id=uuid.uuid4(), tx_data={"amount": 10.0})
    assert created.amount == 10.0
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    # 4. delete
    await repo.delete(created)
    mock_db.delete.assert_called_once_with(created)
    mock_db.commit.assert_called()


@pytest.mark.asyncio
async def test_note_repository_mock():
    mock_db = AsyncMock()
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = ["note1"]
    mock_res.scalars.return_value.first.return_value = "note_first"
    mock_db.execute.return_value = mock_res

    repo = NoteRepository(mock_db)

    # 1. get_all_by_user_id
    notes = await repo.get_all_by_user_id(uuid.uuid4())
    assert len(notes) == 1

    # 2. get_by_id
    note = await repo.get_by_id(uuid.uuid4())
    assert note == "note_first"

    # 3. create
    created = await repo.create(
        user_id=uuid.uuid4(), note_data={"title": "Test Title"}
    )
    assert created.title == "Test Title"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    # 4. delete
    await repo.delete(created)
    mock_db.delete.assert_called_once_with(created)
    mock_db.commit.assert_called()


@pytest.mark.asyncio
async def test_reminder_repository_mock():
    mock_db = AsyncMock()
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = ["rem1"]
    mock_res.scalars.return_value.first.return_value = "rem_first"
    mock_db.execute.return_value = mock_res

    repo = ReminderRepository(mock_db)

    # 1. get_all_by_user_id
    reminders = await repo.get_all_by_user_id(uuid.uuid4())
    assert len(reminders) == 1

    # 2. get_by_id
    reminder = await repo.get_by_id(uuid.uuid4())
    assert reminder == "rem_first"

    # 3. create
    created = await repo.create(
        user_id=uuid.uuid4(), reminder_data={"title": "Reminder Title"}
    )
    assert created.title == "Reminder Title"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    # 4. delete
    await repo.delete(created)
    mock_db.delete.assert_called_once_with(created)
    mock_db.commit.assert_called()
