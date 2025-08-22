# Use official Python runtime
FROM python:3.11-slim

# Install build dependencies for cryptography and psycopg
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment
ENV PYTHONPATH=/app

# Start FastAPI (DB init is already inside lifespan in main.py)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
