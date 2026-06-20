import logging
from datetime import datetime

from app.agents.ollama_client import query_ollama
from app.schemas.agents import ExpenseOutput, NoteOutput, ReminderOutput, RouterOutput

logger = logging.getLogger(__name__)


class RouterAgent:

    @staticmethod
    async def run(text: str) -> RouterOutput:
        system_prompt = (
            "Anda adalah asisten AI router pesan. Tugas Anda adalah mengklasifikasikan intent dari pesan pengguna.\n"
            "Intent yang didukung:\n"
            "- expense: transaksi pengeluaran uang (contoh: 'beli kopi 20rb', 'makan siang 25k')\n"
            "- income: transaksi pemasukan uang (contoh: 'gaji masuk 3 juta', 'terima transfer 50rb')\n"
            "- note: catatan pribadi, tulisan bebas, ide, memo (contoh: 'ide konten instagram', 'catatan rapat hari ini')\n"
            "- report: permintaan laporan atau ringkasan keuangan (contoh: 'laporan minggu ini', 'laporan bulanan', 'summary')\n"
            "- reminder: pengingat tugas atau tagihan dengan target waktu tertentu (contoh: 'remind me bayar listrik jumat depan', 'ingatkan beli susu besok pagi')\n"
            "- unknown: jika input tidak cocok dengan di atas atau tidak jelas.\n\n"
            "Selalu keluarkan JSON valid dengan kunci 'intent'. Jangan tambahkan penjelasan."
        )
        prompt = f'Pesan: "{text}"'
        try:
            result = await query_ollama(
                prompt=prompt,
                system_prompt=system_prompt,
                response_model=RouterOutput,
            )
            return result
        except Exception as e:
            logger.error(f"RouterAgent failed: {e}")
            return RouterOutput(intent="unknown")


class ExpenseAgent:

    @staticmethod
    async def run(text: str) -> ExpenseOutput:
        system_prompt = (
            "Anda adalah parser transaksi keuangan. Ekstrak data transaksi dari input pengguna.\n"
            "Selalu keluarkan JSON valid dengan skema:\n"
            "{\n"
            '  "intent": "expense" atau "income",\n'
            '  "amount": angka nominal,\n'
            '  "category": "kategori (contoh: Makanan, Transportasi, Belanja, dll)",\n'
            '  "description": "deskripsi barang/transaksi",\n'
            '  "payment_method": "metode pembayaran jika ada (contoh: Tunai, QRIS, GoPay, Debit)",\n'
            '  "transaction_date": null\n'
            "}\n"
            "Waktu saat ini (sekarang): " + datetime.now().isoformat() + "\n"
            "Gunakan Bahasa Indonesia. Jangan tambahkan penjelasan."
        )
        prompt = f'Pesan: "{text}"'
        return await query_ollama(
            prompt=prompt,
            system_prompt=system_prompt,
            response_model=ExpenseOutput,
        )


class NoteAgent:

    @staticmethod
    async def run(text: str) -> NoteOutput:
        system_prompt = (
            "Analisis catatan pengguna. Buat judul yang ringkas dan informatif ('title'), "
            "buat ringkasan singkat ('summary'), dan tambahkan maksimal 5 tag yang relevan ('tags').\n"
            "Selalu keluarkan JSON valid dengan skema:\n"
            "{\n"
            '  "title": "Judul Catatan",\n'
            '  "summary": "Ringkasan isi catatan",\n'
            '  "tags": ["tag1", "tag2"]\n'
            "}\n"
            "Jangan tambahkan penjelasan."
        )
        prompt = f'Catatan: "{text}"'
        return await query_ollama(
            prompt=prompt, system_prompt=system_prompt, response_model=NoteOutput
        )


class ReminderAgent:

    @staticmethod
    async def run(text: str) -> ReminderOutput:
        now_str = datetime.now().isoformat()
        system_prompt = (
            "Anda adalah parser pengingat. Ekstrak judul tugas/pengingat ('title') dan waktu jatuh tempo ('due_date').\n"
            f"Waktu sekarang adalah: {now_str}. Hitung due_date relatif terhadap waktu sekarang.\n"
            "due_date harus berupa string ISO-8601 (YYYY-MM-DDTHH:MM:SS) jika disebutkan, jika tidak null.\n"
            "Selalu keluarkan JSON valid dengan skema:\n"
            "{\n"
            '  "title": "Judul Pengingat",\n'
            '  "due_date": "format-iso-atau-null"\n'
            "}\n"
            "Jangan tambahkan penjelasan."
        )
        prompt = f'Pesan: "{text}"'
        return await query_ollama(
            prompt=prompt,
            system_prompt=system_prompt,
            response_model=ReminderOutput,
        )


class ReportAgent:

    @staticmethod
    async def run(transactions_summary: str) -> str:
        system_prompt = (
            "Anda adalah analis keuangan pribadi. Analisis ringkasan transaksi berikut dan berikan laporan insight singkat "
            "berisi tren pengeluaran dan rekomendasi praktis untuk menghemat keuangan.\n"
            "Fokus pada efisiensi anggaran harian/bulanan. Gunakan Bahasa Indonesia yang sopan dan lugas langsung ke poin utama."
        )
        prompt = f"Ringkasan Transaksi:\n{transactions_summary}"
        return await query_ollama(
            prompt=prompt, system_prompt=system_prompt, json_mode=False
        )


class FallbackAgent:

    @staticmethod
    async def run(text: str) -> str:
        system_prompt = (
            "Anda adalah Fallback Agent untuk asisten pribadi. Tangani input pengguna yang tidak jelas atau ambigu.\n"
            "Buat pertanyaan klarifikasi singkat, santun, dan tepat dalam Bahasa Indonesia untuk memperjelas maksud pengguna.\n"
            "Contoh: jika input 'Makan 20', tanyakan 'Apakah Rp20.000 atau Rp20?'"
        )
        prompt = f'Input Ambigu: "{text}"'
        return await query_ollama(
            prompt=prompt, system_prompt=system_prompt, json_mode=False
        )
