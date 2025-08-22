"""
Central place for configuration (env vars, secrets).
Later we’ll load from Railway env vars or .env file.
"""

import os

class Settings:
    PROJECT_NAME: str = "LingAfriq API"
    ENV: str = os.getenv("ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

settings = Settings()
