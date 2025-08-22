from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.core.config import database
from python-jose import jwt, JWTError
import os

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")  # Load from env var
ALGORITHM = "HS256"

class DeleteRequest(BaseModel):
    user_id: str

async def verify_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        query = "SELECT id, name FROM users WHERE id = :user_id"
        user = await database.fetch_one(query=query, values={"user_id": user_id})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/delete", summary="Delete user account")
async def delete_account(request: DeleteRequest, user_id: str = Depends(verify_user)):
    """
    Deletes a user account for Play Store compliance.
    Uses PostgreSQL and JWT authentication.
    """
    if request.user_id != user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    query = "DELETE FROM users WHERE id = :user_id RETURNING id, name"
    deleted_user = await database.fetch_one(query=query, values={"user_id": user_id})
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "deleted_user": {"id": deleted_user["id"], "name": deleted_user["name"]}}
