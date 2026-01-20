#!/bin/bash
set -e

# Seed the database if it doesn't exist or is empty
echo "Seeding database..."
python seed_questions.py
echo "Database seeded."

# Start gunicorn with single worker (SQLite on Azure Files needs this)
exec gunicorn --bind 0.0.0.0:8000 --workers 1 --timeout 120 "app:create_app('production')"
