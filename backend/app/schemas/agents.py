from typing import Literal

from pydantic import BaseModel, Field


class RouterOutput(BaseModel):
    intent: Literal["expense", "income", "note", "report", "reminder", "unknown"]


class ExpenseOutput(BaseModel):
    intent: Literal["expense", "income"]
    amount: float = Field(description="Nominal transaksi, harus berupa angka.")
    category: str | None = Field(
        default=None,
        description="Kategori transaksi (contoh: Makanan, Transportasi, Hiburan, dll).",
    )
    description: str | None = Field(
        default=None, description="Deskripsi singkat transaksi."
    )
    payment_method: str | None = Field(
        default=None, description="Metode pembayaran (contoh: Tunai, QRIS, Debit, dll)."
    )
    transaction_date: str | None = Field(
        default=None,
        description="Tanggal transaksi dalam format ISO (YYYY-MM-DDTHH:MM:SS) jika disebutkan, jika tidak null.",
    )


class NoteOutput(BaseModel):
    title: str = Field(description="Judul catatan yang ringkas dan informatif.")
    summary: str = Field(description="Ringkasan singkat isi catatan.")
    tags: list[str] = Field(
        default_factory=list, description="Maksimal 5 tag/label yang relevan."
    )


class ReminderOutput(BaseModel):
    title: str = Field(description="Judul pengingat yang ringkas.")
    due_date: str | None = Field(
        default=None,
        description="Waktu jatuh tempo dalam format ISO (YYYY-MM-DDTHH:MM:SS) jika ada, jika tidak null.",
    )
