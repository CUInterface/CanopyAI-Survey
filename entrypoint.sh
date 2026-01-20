#!/bin/bash
set -e

# Seed the database if it doesn't exist or is empty
python seed_questions.py

# Start gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 2 "app:create_app('production')"
