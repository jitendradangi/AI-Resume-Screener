from fastapi import FastAPI, Depends

from app.database.base import Base
from app.database.db import engine
from app.models.user import User
from app.models.resume import Resume
from app.routers import resume

from app.routers import auth
from app.core.dependencies import get_current_user
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Screener API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resume.router)


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