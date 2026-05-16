#!/bin/bash
# Run in WSL from project root: bash database/setup_postgres.sh

set -e
echo "Updating packages..."
sudo apt-get update -qq
echo "Installing PostgreSQL..."
sudo apt-get install -y postgresql postgresql-contrib
echo "Starting PostgreSQL..."
sudo service postgresql start
echo "Creating database and user..."
sudo -u postgres psql -c "CREATE DATABASE diet_recommendation_db;" 2>/dev/null || true
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
echo "Done. Then run: cd backend && alembic upgrade head && uvicorn app.main:app --reload"
