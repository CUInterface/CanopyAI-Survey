#!/bin/bash

# Azure App Service startup script
# This script runs when the app starts on Azure

# Ensure instance directory exists for SQLite database
mkdir -p /home/site/wwwroot/instance

# Run database seed if needed (only seeds if empty)
python seed_questions.py

# Start gunicorn
gunicorn --bind=0.0.0.0:8000 --workers=2 'app:create_app("production")'
