"""
Exception Handler
=================
Centralized exception handling for consistent error responses.
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.core.logging_config import get_logger

from app.exceptions.custom_exceptions import (
    AppException,
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ConflictException,
    ValidationException,
    FileProcessingException,
    ExternalServiceException,
)

logger = get_logger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle application exceptions and return consistent error responses.
    
    Args:
        request: FastAPI request
        exc: Application exception
    
    Returns:
        JSON response with error details
    """
    # Log the error
    logger.error(
        f"Application error: {exc.__class__.__name__} - {exc.message}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "details": exc.details,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "details": exc.details,
                "type": exc.__class__.__name__,
            }
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions and return consistent error responses.
    
    Args:
        request: FastAPI request
        exc: HTTP exception
    
    Returns:
        JSON response with error details
    """
    # Log the error
    logger.warning(
        f"HTTP error: {exc.status_code} - {exc.detail}",
        extra={
            "path": request.url.path,
            "method": request.method,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "HTTPException",
            }
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions and return consistent error responses.
    
    Args:
        request: FastAPI request
        exc: Unexpected exception
    
    Returns:
        JSON response with error details
    """
    # Log the error with full traceback
    logger.exception(
        f"Unexpected error: {exc.__class__.__name__} - {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method,
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "An unexpected error occurred",
                "type": "InternalServerError",
            }
        },
    )
