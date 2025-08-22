from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()

# Temporary in-memory users (replace with DB later)
fake_users_db = {
    "123": {"id": "123", "name": "Test User"},
    "456": {"id": "456", "name": "Another User"},
}

class DeleteRequest(BaseModel):
    user_id: str

# Mock authentication (replace with JWT or API key in production)
async def verify_user(user_id: str):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=401, detail="Unauthorized or user not found")
    return user_id

@router.post("/delete", summary="Delete user account")
async def delete_account(request: DeleteRequest, user_id: str = Depends(verify_user)):
    """
    Deletes a user account for Play Store compliance.
    In production, connect to a database and validate auth.
    """
    deleted_user = fake_users_db.pop(user_id)
    return {"status": "success", "deleted_user": deleted_user}
