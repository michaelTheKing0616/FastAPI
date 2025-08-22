# Use official Python runtime
FROM python:3.11-slim

# Install build dependencies for cryptography
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip show python-jose || { echo "python-jose not installed"; exit 1; } && \
    pip show cryptography || { echo "cryptography not installed"; exit 1; } && \
    pip show sqlalchemy || { echo "sqlalchemy not installed"; exit 1; }

# Copy project files
COPY . .

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app

# Run database initialization and app
CMD ["/bin/sh", "-c", "python app/db/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
