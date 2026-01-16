FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create instance directory for SQLite
RUN mkdir -p /app/instance

# Seed the database
RUN python seed_questions.py

# Expose port
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:create_app('production')"]
