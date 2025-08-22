from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="LingAfriq API",
    description="Backend for LingAfriq app (Delete Account, future endpoints)",
    version="1.0.0",
)

# Temporary in-memory users (replace with DB later)
fake_users_db = {
    "123": {"id": "123", "name": "Test User"},
    "456": {"id": "456", "name": "Another User"},
}

@app.delete("/account/{user_id}", summary="Delete user account")
async def delete_account(user_id: str):
    """
    Deletes a user account. In production, connect this to your real DB.
    """
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")

    deleted_user = fake_users_db.pop(user_id)
    return {"status": "success", "deleted_user": deleted_user}


@app.get("/", tags=["Health"])
async def root():
    return {"message": "LingAfriq API is live 🚀"}
