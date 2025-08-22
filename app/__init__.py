"""
LingAfriq API package.
Assembles FastAPI app and includes all routers.
"""

from fastapi import FastAPI
from .routes import account
from .routes import account, web_delete


# Create FastAPI instance
app = FastAPI(
    title="LingAfriq API",
    description="Backend for LingAfriq app (Delete Account, future endpoints)",
    version="1.0.0",
)

# Routers
app.include_router(account.router, prefix="/account", tags=["Account"])
app.include_router(web_delete.router)

@app.get("/", tags=["Health"])
async def root():
    return {"message": "LingAfriq API is live 🚀"}
