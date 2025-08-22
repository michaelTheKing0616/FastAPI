import asyncio
from app.core.config import database

async def init_db():
    try:
        await database.connect()
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """
        await database.execute(query=query)
        await database.execute(
            query="INSERT INTO users (id, name) VALUES (:id, :name) ON CONFLICT DO NOTHING",
            values=[{"id": "123", "name": "Test User"}, {"id": "456", "name": "Another User"}]
        )
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise
    finally:
        await database.disconnect()

if __name__ == "__main__":
    asyncio.run(init_db())
