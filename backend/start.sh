#!/bin/sh
set -e

# Wait for DB to be online
python -m app.wait_for_db

# Run alembic migrations
alembic upgrade head

# Start application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
