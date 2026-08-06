"""
Rate Limiting Configuration
===========================
Rate limiting setup to protect API from abuse and brute-force attacks.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from app.core.logging_config import get_logger
from app.core.config import settings

logger = get_logger(__name__)

# Create limiter instance with settings from config
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"] if settings.RATE_LIMIT_ENABLED else None
)


def on_rate_limit_exceeded(request: Request, exc: RateLimitExceeded):
    """
    Handle rate limit exceeded events with logging.
    
    Args:
        request: FastAPI request
        exc: Rate limit exceeded exception
    
    Returns:
        JSON response with 429 status
    """
    # Log the rate limit violation
    logger.warning(
        f"Rate limit exceeded: {request.method} {request.url.path} from {get_remote_address(request)}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "client_ip": get_remote_address(request),
        }
    )
    
    return {
        "error": {
            "message": "Rate limit exceeded. Please try again later.",
            "type": "RateLimitExceeded",
            "details": {
                "limit": exc.detail,
            }
        }
    }
