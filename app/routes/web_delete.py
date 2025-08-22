from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import database
from python_jose import jwt, JWTError
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

@router.get("/delete", response_class=HTMLResponse, tags=["Web"])
async def show_delete_form(request: Request):
    return templates.TemplateResponse("delete.html", {"request": request})

@router.post("/delete", response_class=HTMLResponse, tags=["Web"])
async def delete_via_form(request: Request, user_id: str = Form(...), token: str = Form(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not sub or sub != user_id:
            return templates.TemplateResponse("delete.html", {"request": request, "error": "Invalid token or user mismatch"})

        query = "DELETE FROM users WHERE id = :user_id RETURNING id, name"
        deleted_user = await database.fetch_one(query=query, values={"user_id": user_id})
        if not deleted_user:
            return templates.TemplateResponse("delete.html", {"request": request, "error": "User not found"})
        return templates.TemplateResponse("delete.html", {"request": request, "success": f"Deleted user {deleted_user['name']} ✅"})
    except JWTError:
        return templates.TemplateResponse("delete.html", {"request": request, "error": "Invalid token"})
