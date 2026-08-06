"""
Exceptions Module
================
Centralized exception handling and custom exception classes.
"""

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

from app.exceptions.handler import (
    app_exception_handler,
    http_exception_handler,
    general_exception_handler,
)

__all__ = [
    # Custom exceptions
    "AppException",
    "NotFoundException",
    "BadRequestException",
    "UnauthorizedException",
    "ConflictException",
    "ValidationException",
    "FileProcessingException",
    "ExternalServiceException",
    # Exception handlers
    "app_exception_handler",
    "http_exception_handler",
    "general_exception_handler",
]
