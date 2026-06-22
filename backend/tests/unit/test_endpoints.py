from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
import uuid

from app.core.config import settings
from app.main import app
from app.models.models import Note, Transaction
from app.schemas.agents import ExpenseOutput, NoteOutput, ReminderOutput, RouterOutput
from httpx import ASGITransport, AsyncClient
import pytest


@pytest.mark.asyncio
async def test_transactions_endpoints():
    user_id = uuid.uuid4()
    mock_user = MagicMock()
    mock_user.id = user_id

    mock_tx = MagicMock(spec=Transaction)
    mock_tx.id = uuid.uuid4()
    mock_tx.user_id = user_id
    mock_tx.type = "expense"
    mock_tx.amount = 15000.0
    mock_tx.category = "Food"
    mock_tx.description = "Snack"
    mock_tx.payment_method = "Cash"
    mock_tx.transaction_date = datetime.now()
    mock_tx.created_at = datetime.now()

    # Create auth token for user_id
    from app.core.security import create_access_token

    token = create_access_token({"sub": str(user_id)})
    headers = {"Authorization": f"Bearer {token}"}

    with patch(
        "app.api.deps.UserRepository.get_by_id", new_callable=AsyncMock
    ) as mock_get_user, patch(
        "app.repositories.transaction.TransactionRepository.get_all_by_user_id",
        new_callable=AsyncMock,
    ) as mock_get_all, patch(
        "app.repositories.transaction.TransactionRepository.create",
        new_callable=AsyncMock,
    ) as mock_create, patch(
        "app.repositories.transaction.TransactionRepository.get_by_id",
        new_callable=AsyncMock,
    ) as mock_get_by_id, patch(
        "app.repositories.transaction.TransactionRepository.delete",
        new_callable=AsyncMock,
    ) as mock_delete:

        mock_get_user.return_value = mock_user
        mock_get_all.return_value = [mock_tx]
        mock_create.return_value = mock_tx
        mock_get_by_id.return_value = mock_tx

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            # 1. GET /transactions
            response = await ac.get("/api/v1/transactions", headers=headers)
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["amount"] == 15000.0

            # 2. POST /transactions
            new_tx_data = {
                "type": "expense",
                "amount": 15000.0,
                "category": "Food",
                "description": "Snack",
                "payment_method": "Cash",
            }
            response = await ac.post(
                "/api/v1/transactions", json=new_tx_data, headers=headers
            )
            assert response.status_code == 201
            assert response.json()["amount"] == 15000.0

            # 3. DELETE /transactions/{id}
            tx_id_str = str(mock_tx.id)
            response = await ac.delete(
                f"/api/v1/transactions/{tx_id_str}", headers=headers
            )
            assert response.status_code == 204
            mock_delete.assert_called_once()

            # 4. DELETE /transactions/{id} unauthorized or not found
            mock_get_by_id.return_value = None
            response = await ac.delete(
                f"/api/v1/transactions/{tx_id_str}", headers=headers
            )
            assert response.status_code == 404


@pytest.mark.asyncio
async def test_notes_endpoints():
    user_id = uuid.uuid4()
    mock_user = MagicMock()
    mock_user.id = user_id

    mock_note = MagicMock(spec=Note)
    mock_note.id = uuid.uuid4()
    mock_note.user_id = user_id
    mock_note.title = "Test Note"
    mock_note.content = "Content"
    mock_note.tags = ["test"]
    mock_note.summary = "Summary"
    mock_note.created_at = datetime.now()

    from app.core.security import create_access_token

    token = create_access_token({"sub": str(user_id)})
    headers = {"Authorization": f"Bearer {token}"}

    with patch(
        "app.api.deps.UserRepository.get_by_id", new_callable=AsyncMock
    ) as mock_get_user, patch(
        "app.repositories.note.NoteRepository.get_all_by_user_id",
        new_callable=AsyncMock,
    ) as mock_get_all, patch(
        "app.repositories.note.NoteRepository.create", new_callable=AsyncMock
    ) as mock_create, patch(
        "app.repositories.note.NoteRepository.get_by_id", new_callable=AsyncMock
    ) as mock_get_by_id, patch(
        "app.repositories.note.NoteRepository.delete", new_callable=AsyncMock
    ) as mock_delete:

        mock_get_user.return_value = mock_user
        mock_get_all.return_value = [mock_note]
        mock_create.return_value = mock_note
        mock_get_by_id.return_value = mock_note

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            # 1. GET /notes
            response = await ac.get("/api/v1/notes", headers=headers)
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["title"] == "Test Note"

            # 2. POST /notes
            new_note_data = {
                "title": "Test Note",
                "content": "Content",
                "tags": ["test"],
            }
            response = await ac.post(
                "/api/v1/notes", json=new_note_data, headers=headers
            )
            assert response.status_code == 201
            assert response.json()["title"] == "Test Note"

            # 3. DELETE /notes/{id}
            note_id_str = str(mock_note.id)
            response = await ac.delete(
                f"/api/v1/notes/{note_id_str}", headers=headers
            )
            assert response.status_code == 204
            mock_delete.assert_called_once()


@pytest.mark.asyncio
async def test_bot_message_static_commands():
    user_id = uuid.uuid4()
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.telegram_id = 12345
    mock_user.username = "testbot"
    mock_user.full_name = "Test Bot User"

    headers = {"X-Bot-Secret": settings.TELEGRAM_WEBHOOK_SECRET}

    with patch(
        "app.repositories.user.UserRepository.get_by_telegram_id",
        new_callable=AsyncMock,
    ) as mock_get_user:
        mock_get_user.return_value = mock_user

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            # 1. /start command
            payload = {
                "telegram_id": 12345,
                "username": "testbot",
                "full_name": "Test Bot User",
                "text": "/start",
            }
            response = await ac.post(
                "/api/v1/bot/message", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Selamat datang" in response.json()["response_text"]

            # 2. /help command
            payload["text"] = "/help"
            response = await ac.post(
                "/api/v1/bot/message", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Panduan Penggunaan" in response.json()["response_text"]

            # 3. /notes command
            payload["text"] = "/notes"
            with patch(
                "app.repositories.note.NoteRepository.get_all_by_user_id",
                new_callable=AsyncMock,
            ) as mock_get_notes:
                mock_note = MagicMock()
                mock_note.title = "Test Note"
                mock_note.content = "Content"
                mock_note.tags = ["test"]
                mock_note.summary = "Summary"
                mock_get_notes.return_value = [mock_note]

                response = await ac.post(
                    "/api/v1/bot/message", json=payload, headers=headers
                )
                assert response.status_code == 200
                assert "Catatan Terakhir Anda" in response.json()["response_text"]

            # 4. /transactions command
            payload["text"] = "/transactions"
            with patch(
                "app.repositories.transaction.TransactionRepository.get_all_by_user_id",
                new_callable=AsyncMock,
            ) as mock_get_txs:
                mock_tx = MagicMock()
                mock_tx.type = "expense"
                mock_tx.amount = 10000
                mock_tx.description = "kopi"
                mock_tx.category = "Makanan"
                mock_tx.transaction_date = datetime.now()
                mock_get_txs.return_value = [mock_tx]

                response = await ac.post(
                    "/api/v1/bot/message", json=payload, headers=headers
                )
                assert response.status_code == 200
                assert "Transaksi Terakhir Anda" in response.json()["response_text"]



@pytest.mark.asyncio
async def test_bot_message_ai_intents():
    user_id = uuid.uuid4()
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.telegram_id = 12345
    mock_user.username = "testbot"
    mock_user.full_name = "Test Bot User"

    headers = {"X-Bot-Secret": settings.TELEGRAM_WEBHOOK_SECRET}
    payload = {
        "telegram_id": 12345,
        "username": "testbot",
        "full_name": "Test Bot User",
        "text": "Beli kopi 20rb",
    }

    with patch(
        "app.repositories.user.UserRepository.get_by_telegram_id",
        new_callable=AsyncMock,
    ) as mock_get_user, patch(
        "app.repositories.transaction.TransactionRepository.create",
        new_callable=AsyncMock,
    ) as mock_tx_create, patch(
        "app.repositories.note.NoteRepository.create", new_callable=AsyncMock
    ) as mock_note_create, patch(
        "app.repositories.reminder.ReminderRepository.create",
        new_callable=AsyncMock,
    ) as mock_reminder_create, patch(
        "app.repositories.transaction.TransactionRepository.get_all_by_user_id",
        new_callable=AsyncMock,
    ) as mock_tx_get_all, patch(
        "app.agents.agents.RouterAgent.run", new_callable=AsyncMock
    ) as mock_router, patch(
        "app.agents.agents.ExpenseAgent.run", new_callable=AsyncMock
    ) as mock_expense, patch(
        "app.agents.agents.NoteAgent.run", new_callable=AsyncMock
    ) as mock_note, patch(
        "app.agents.agents.ReminderAgent.run", new_callable=AsyncMock
    ) as mock_reminder, patch(
        "app.agents.agents.ReportAgent.run", new_callable=AsyncMock
    ) as mock_report, patch(
        "app.agents.agents.FallbackAgent.run", new_callable=AsyncMock
    ) as mock_fallback:

        mock_get_user.return_value = mock_user

        # 1. Expense intent
        mock_router.return_value = RouterOutput(intent="expense")
        mock_expense.return_value = ExpenseOutput(
            intent="expense",
            amount=20000.0,
            category="Makanan",
            description="Beli kopi",
            payment_method="Tunai",
            transaction_date=None,
        )
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/api/v1/bot/message", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Transaksi Berhasil Dicatat" in response.json()["response_text"]
            mock_tx_create.assert_called_once()

            # 2. Note intent
            payload["text"] = "Catatan: ide kedai kopi harian"
            mock_router.return_value = RouterOutput(intent="note")
            mock_note.return_value = NoteOutput(
                title="Ide Bisnis",
                summary="Ide cafe kopi",
                tags=["kopi", "ide"],
            )
            response = await ac.post(
                "/api/v1/bot/message", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Catatan Disimpan" in response.json()["response_text"]
            mock_note_create.assert_called_once()

            # 3. Reminder intent
            payload["text"] = "Remind me bayar internet besok"
            mock_router.return_value = RouterOutput(intent="reminder")
            mock_reminder.return_value = ReminderOutput(
                title="Bayar internet", due_date=None
            )
            response = await ac.post(
                "/api/v1/bot/message", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Pengingat Diset" in response.json()["response_text"]
            mock_reminder_create.assert_called_once()

            # 4. Report intent
            payload["text"] = "/report"
            mock_tx_get_all.return_value = []
            mock_report.return_value = "Laporan mingguan aman"
            response = await ac.post(
                "/api/v1/bot/message", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Laporan Analisis AI" in response.json()["response_text"]

            # 5. Unknown intent
            payload["text"] = "Hmm?"
            mock_router.return_value = RouterOutput(intent="unknown")
            mock_fallback.return_value = "Bisa tolong ulangi?"
            response = await ac.post(
                "/api/v1/bot/message", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Bisa tolong ulangi?" in response.json()["response_text"]


@pytest.mark.asyncio
async def test_scheduler_due_reminders():
    mock_reminder = MagicMock()
    mock_reminder.title = "Tugas 1"
    mock_reminder.due_date = datetime.now() - timedelta(minutes=5)
    mock_reminder.status = "pending"
    mock_reminder.user = MagicMock()
    mock_reminder.user.telegram_id = 9999

    with patch("app.core.scheduler.SessionLocal") as mock_session_cls, patch(
        "app.core.scheduler.send_telegram_message", new_callable=AsyncMock
    ) as mock_send:

        mock_db = AsyncMock()
        mock_session_cls.return_value.__aenter__.return_value = mock_db

        mock_res = MagicMock()
        mock_res.scalars.return_value.all.return_value = [mock_reminder]
        mock_db.execute.return_value = mock_res

        from app.core.scheduler import process_due_reminders

        await process_due_reminders()

        mock_send.assert_called_once()
        assert mock_reminder.status == "completed"


@pytest.mark.asyncio
async def test_scheduler_daily_report():
    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_user.telegram_id = 8888

    mock_tx = MagicMock()
    mock_tx.type = "expense"
    mock_tx.amount = 10000.0
    mock_tx.description = "kopi"
    mock_tx.category = "Makanan"
    mock_tx.transaction_date = datetime.now()

    with patch("app.core.scheduler.SessionLocal") as mock_session_cls, patch(
        "app.core.scheduler.send_telegram_message", new_callable=AsyncMock
    ) as mock_send, patch(
        "app.agents.agents.ReportAgent.run", new_callable=AsyncMock
    ) as mock_report_agent:

        mock_db = AsyncMock()
        mock_session_cls.return_value.__aenter__.return_value = mock_db

        mock_user_res = MagicMock()
        mock_user_res.scalars.return_value.all.return_value = [mock_user]

        mock_tx_res = MagicMock()
        mock_tx_res.scalars.return_value.all.return_value = [mock_tx]

        # First query for users, second for transactions
        mock_db.execute.side_effect = [mock_user_res, mock_tx_res]
        mock_report_agent.return_value = "AI Insight"

        from app.core.scheduler import send_scheduled_report

        await send_scheduled_report("daily")

        mock_send.assert_called_once()
        assert "AI Insight" in mock_send.call_args[0][1]


@pytest.mark.asyncio
async def test_bot_chat_endpoint():
    user_id = uuid.uuid4()
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.full_name = "Test Chat User"

    # Create auth token for user_id
    from app.core.security import create_access_token
    token = create_access_token({"sub": str(user_id)})
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "text": "Beli kopi 20rb"
    }

    with patch(
        "app.api.deps.UserRepository.get_by_id", new_callable=AsyncMock
    ) as mock_get_user, patch(
        "app.repositories.transaction.TransactionRepository.create",
        new_callable=AsyncMock,
    ) as mock_tx_create, patch(
        "app.repositories.note.NoteRepository.create", new_callable=AsyncMock
    ) as mock_note_create, patch(
        "app.repositories.reminder.ReminderRepository.create",
        new_callable=AsyncMock,
    ) as mock_reminder_create, patch(
        "app.repositories.transaction.TransactionRepository.get_all_by_user_id",
        new_callable=AsyncMock,
    ) as mock_tx_get_all, patch(
        "app.repositories.note.NoteRepository.get_all_by_user_id",
        new_callable=AsyncMock,
    ) as mock_note_get_all, patch(
        "app.agents.agents.RouterAgent.run", new_callable=AsyncMock
    ) as mock_router, patch(
        "app.agents.agents.ExpenseAgent.run", new_callable=AsyncMock
    ) as mock_expense, patch(
        "app.agents.agents.NoteAgent.run", new_callable=AsyncMock
    ) as mock_note, patch(
        "app.agents.agents.ReminderAgent.run", new_callable=AsyncMock
    ) as mock_reminder, patch(
        "app.agents.agents.ReportAgent.run", new_callable=AsyncMock
    ) as mock_report, patch(
        "app.agents.agents.FallbackAgent.run", new_callable=AsyncMock
    ) as mock_fallback:

        mock_get_user.return_value = mock_user

        # 1. Expense intent
        mock_router.return_value = RouterOutput(intent="expense")
        mock_expense.return_value = ExpenseOutput(
            intent="expense",
            amount=20000.0,
            category="Makanan",
            description="Beli kopi",
            payment_method="Tunai",
            transaction_date=None,
        )
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/api/v1/bot/chat", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Transaksi Berhasil Dicatat" in response.json()["response_text"]
            mock_tx_create.assert_called_once()

            # 2. Static /help command
            payload["text"] = "/help"
            response = await ac.post(
                "/api/v1/bot/chat", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Panduan Penggunaan" in response.json()["response_text"]

            # 3. Static /notes command
            payload["text"] = "/notes"
            mock_note_item = MagicMock()
            mock_note_item.title = "Chat Note"
            mock_note_item.content = "Chat Content"
            mock_note_item.tags = ["chat"]
            mock_note_item.summary = "Chat Summary"
            mock_note_get_all.return_value = [mock_note_item]
            response = await ac.post(
                "/api/v1/bot/chat", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Catatan Terakhir Anda" in response.json()["response_text"]

            # 4. Static /transactions command
            payload["text"] = "/transactions"
            mock_tx_item = MagicMock()
            mock_tx_item.type = "expense"
            mock_tx_item.amount = 12000.0
            mock_tx_item.description = "siomay"
            mock_tx_item.category = "Makanan"
            mock_tx_item.transaction_date = datetime.now()
            mock_tx_get_all.return_value = [mock_tx_item]
            response = await ac.post(
                "/api/v1/bot/chat", json=payload, headers=headers
            )
            assert response.status_code == 200
            assert "Transaksi Terakhir Anda" in response.json()["response_text"]

