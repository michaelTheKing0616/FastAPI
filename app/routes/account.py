from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.core.config import database  # Import the database instance

router = APIRouter()

class DeleteRequest(BaseModel):
    user_id: str

# Mock authentication (replace with JWT or API key in production)
async def verify_user(user_id: str):
    # Query the database to verify user exists
    query = "SELECT id, name FROM users WHERE id = :user_id"
    user = await database.fetch_one(query=query, values={"user_id": user_id})
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized or user not found")
    return user_id

@router.post("/delete", summary="Delete user account")
async def delete_account(request: DeleteRequest, user_id: str = Depends(verify_user)):
    """
    Deletes a user account for Play Store compliance.
    Uses PostgreSQL for persistent storage.
    """
    query = "DELETE FROM users WHERE id = :user_id RETURNING id, name"
    deleted_user = await database.fetch_one(query=query, values={"user_id": user_id})
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "deleted_user": {"id": deleted_user["id"], "name": deleted_user["name"]}}
