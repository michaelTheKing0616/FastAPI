from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
