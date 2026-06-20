# Environment Variables

POSTGRES_DB=notes_expense
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/notes_expense
Redis
REDIS_URL=redis://redis:6379/0
Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_WEBHOOK_SECRET=
AI
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=kwangsuklee/Qwen3.5-4B-Claude-4.6-Opus-Reasoning-Distilled-GGUF
AI_TIMEOUT=60
Frontend
VITE_API_URL=http://localhost:8000/api/v1
Security Notes
Jangan commit file .env
Simpan .env.example di repository
Rotasi secret secara berkala