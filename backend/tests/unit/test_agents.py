from unittest.mock import AsyncMock, patch

import pytest
from app.agents.agents import (
    ExpenseAgent,
    FallbackAgent,
    NoteAgent,
    ReminderAgent,
    ReportAgent,
    RouterAgent,
)
from app.schemas.agents import ExpenseOutput, NoteOutput, ReminderOutput, RouterOutput


@pytest.mark.asyncio
async def test_router_agent_mock():
    with patch("app.agents.agents.query_ollama", new_callable=AsyncMock) as mock_query:
        mock_query.return_value = RouterOutput(intent="expense")
        result = await RouterAgent.run("Bought coffee")
        assert result.intent == "expense"
        mock_query.assert_called_once()


@pytest.mark.asyncio
async def test_expense_agent_mock():
    with patch("app.agents.agents.query_ollama", new_callable=AsyncMock) as mock_query:
        mock_query.return_value = ExpenseOutput(
            intent="expense",
            amount=20000,
            category="Makanan",
            description="kopi",
            payment_method="Tunai",
            transaction_date=None,
        )
        result = await ExpenseAgent.run("beli kopi 20rb")
        assert result.intent == "expense"
        assert result.amount == 20000
        assert result.category == "Makanan"
        mock_query.assert_called_once()


@pytest.mark.asyncio
async def test_note_agent_mock():
    with patch("app.agents.agents.query_ollama", new_callable=AsyncMock) as mock_query:
        mock_query.return_value = NoteOutput(
            title="Ide Bisnis",
            summary="Membuat ide kedai kopi harian",
            tags=["bisnis", "kopi"],
        )
        result = await NoteAgent.run("Catatan: ide kedai kopi harian")
        assert result.title == "Ide Bisnis"
        assert len(result.tags) == 2
        mock_query.assert_called_once()


@pytest.mark.asyncio
async def test_reminder_agent_mock():
    with patch("app.agents.agents.query_ollama", new_callable=AsyncMock) as mock_query:
        mock_query.return_value = ReminderOutput(
            title="Bayar listrik", due_date="2026-06-25T00:00:00"
        )
        result = await ReminderAgent.run("Bayar listrik minggu depan")
        assert result.title == "Bayar listrik"
        assert result.due_date == "2026-06-25T00:00:00"
        mock_query.assert_called_once()


@pytest.mark.asyncio
async def test_report_agent_mock():
    with patch("app.agents.agents.query_ollama", new_callable=AsyncMock) as mock_query:
        mock_query.return_value = "Ini adalah laporan insight bulanan..."
        result = await ReportAgent.run("Transaksi: kopi 20rb")
        assert "insight" in result
        mock_query.assert_called_once()


@pytest.mark.asyncio
async def test_fallback_agent_mock():
    with patch("app.agents.agents.query_ollama", new_callable=AsyncMock) as mock_query:
        mock_query.return_value = "Apakah Rp20.000 atau Rp20?"
        result = await FallbackAgent.run("Makan 20")
        assert "?" in result
        mock_query.assert_called_once()
