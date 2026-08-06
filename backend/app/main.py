from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from slowapi.errors import RateLimitExceeded

from app.database.base import Base
from app.database.db import engine
from app.core.logging_config import setup_logging, get_logger
from app.core.rate_limit import limiter, on_rate_limit_exceeded
from app.core.config import settings
from app.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    general_exception_handler,
)

# Setup logging
setup_logging(log_level=settings.LOG_LEVEL)
logger = get_logger(__name__)

# Import all models so SQLAlchemy registers them with Base.metadata
from app.models.user import User
from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.models.job import Job
from app.models.job_match import JobMatch
from app.models.ats_report import ATSReport
from app.models.ats_score import ATSScore

from app.routers import auth, resume as resume_router, jobs, ats, job_match
from app.dependencies import get_current_user

# Database connection with retry logic for Railway
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Database connection error: {e}")
    # Continue startup even if DB fails (it might be available later)

app = FastAPI(
    title="AI Resume Screener API",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, on_rate_limit_exceeded)

# Add exception handlers
app.add_exception_handler(RateLimitExceeded, on_rate_limit_exceeded)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resume_router.router)
app.include_router(jobs.router)
app.include_router(ats.router)
app.include_router(job_match.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests with timing information."""
    start_time = time.time()
    
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"Response: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url.path} - "
            f"Error: {str(e)} - "
            f"Time: {process_time:.3f}s"
        )
        raise


@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info("AI Resume Screener API starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    logger.info("AI Resume Screener API shutting down...")


@app.get("/")
@limiter.limit("100/minute")
def root(request: Request):
    logger.info("Root endpoint accessed")
    return {
        "message": "Backend Running"
    }


@app.get("/profile")
@limiter.limit("60/minute")
def profile(request: Request, current_user=Depends(get_current_user)):
    logger.info(f"Profile endpoint accessed by user: {current_user.email}")
    return {
        "logged_in_user": current_user
    }