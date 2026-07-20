from fastapi import FastAPI

from app.database.db import engine
from app.database.base import Base

# Import models so SQLAlchemy knows about them
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Screener API")

@app.get("/")
def root():
    return {
        "message": "Backend Connected Successfully"
    }