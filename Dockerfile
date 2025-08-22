# Use official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run app with dynamic $PORT
CMD ["/bin/sh", "-c", "python app/db/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
