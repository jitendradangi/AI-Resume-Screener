from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import Base
from app.database.db import engine

# Import all models so SQLAlchemy registers them with Base.metadata
from app.models.user import User
from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.models.job import Job
from app.models.job_match import JobMatch
from app.models.ats_report import ATSReport

from app.routers import auth, resume as resume_router
from app.core.dependencies import get_current_user

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
app.include_router(resume_router.router)


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