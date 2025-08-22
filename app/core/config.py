"""
Central place for configuration (env vars, secrets).
Later we’ll load from Railway env vars or .env file.
"""

import os
from databases import Database

class Settings:
    PROJECT_NAME: str = "LingAfriq API"
    ENV: str = os.getenv("ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/dev")  # Default for local dev

settings = Settings()

# Initialize async database connection
database = Database(settings.DATABASE_URL)
