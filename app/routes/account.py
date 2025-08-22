from fastapi import APIRouter, HTTPException

router = APIRouter()

# Temporary in-memory users (replace with DB later)
fake_users_db = {
    "123": {"id": "123", "name": "Test User"},
    "456": {"id": "456", "name": "Another User"},
}

@router.delete("/{user_id}", summary="Delete user account")
async def delete_account(user_id: str):
    """
    Deletes a user account.
    In production, this will connect to your database.
    """
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")

    deleted_user = fake_users_db.pop(user_id)
    return {"status": "success", "deleted_user": deleted_user}
