from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to DB
    await database.connect()
    try:
        # Create table if not exists
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """
        await database.execute(query=query)

        # Insert demo data (safe if already exists)
        await database.execute_many(
            query="INSERT INTO users (id, name) VALUES (:id, :name) ON CONFLICT DO NOTHING",
            values=[
                {"id": "123", "name": "Test User"},
                {"id": "456", "name": "Another User"},
            ],
        )

        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
    yield
    # Disconnect DB
    await database.disconnect()

# Create app with lifespan
app = FastAPI(lifespan=lifespan)
