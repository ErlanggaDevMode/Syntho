up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

build:
	docker compose build

ps:
	docker compose ps

backend:
	docker compose exec backend sh

bot:
	docker compose exec bot sh

db:
	docker compose exec postgres psql -U postgres

test:
	docker compose exec backend pytest

lint:
	docker compose exec backend ruff check .

format:
	docker compose exec backend black .

pull-model:
	docker compose exec ollama ollama pull qwen3:4b