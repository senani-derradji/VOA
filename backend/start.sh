#!/bin/bash
set -e
echo "---------------------------------------- start .sh --------------------------------------------"

echo "Running alembic migrations..."
alembic upgrade head && sleep 5 && python db_test.py

cd /app && uvicorn app.main:app --host 0.0.0.0 --port 8000