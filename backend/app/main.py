from fastapi import FastAPI, Depends

from app.database.base import Base
from app.database.db import engine
from app.models.user import User

from app.routers import auth
from app.core.dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Screener API")

app.include_router(auth.router)


@app.get("/")
def root():
    return {
        "message": "Backend Running"
    }


@app.get("/profile")
def profile(current_user=Depends(get_current_user)):
    return {
        "logged_in_user": current_user
    }