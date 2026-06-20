# System Architecture

## High-Level Architecture

```text
User
  │
  ▼
Telegram Bot
  │
  ▼
FastAPI Backend
  │
  ├── AI Service
  ├── PostgreSQL
  ├── Redis
  └── Scheduler
        │
        ▼
   Notification Service
```

## Components

### Telegram Bot

Responsibilities:

* Menerima pesan
* Mengirim respons
* Autentikasi pengguna

Technology:

* python-telegram-bot

---

### Backend API

Responsibilities:

* Business logic
* Validasi data
* Otorisasi
* API dashboard

Technology:

* FastAPI

---

### AI Service

Responsibilities:

* Intent classification
* Entity extraction
* Summarization
* Recommendation

Technology:

* Ollama

Recommended models:

* Qwen3:4b
* Gemma3:4b
* Phi-4 Mini

---

### Database

Responsibilities:

* Menyimpan data pengguna
* Menyimpan transaksi
* Menyimpan catatan

Technology:

* PostgreSQL

---

### Cache Layer

Responsibilities:

* Session cache
* Rate limiting

Technology:

* Redis

---

### Scheduler

Responsibilities:

* Generate laporan
* Pengingat

Technology:

* APScheduler
