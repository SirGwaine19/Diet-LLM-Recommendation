#!/bin/sh
set -e

echo "Running database migrations..."
alembic upgrade head

if [ "${SEED_FOODS:-false}" = "true" ]; then
  echo "Seeding food database..."
  python scripts/seed_foods.py
fi

echo "Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
