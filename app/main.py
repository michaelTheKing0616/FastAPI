"""
Entrypoint for running the FastAPI app.
This is what uvicorn will point to.
"""

from app import app

# Nothing else needed — uvicorn will import `app` from here.
# Example: uvicorn app.main:app --reload
