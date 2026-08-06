# Production Configuration Guide

## Environment Setup

The AI Resume Screener backend supports multiple environments through environment-specific configuration files.

### Environment Files

- `.env` - Local development (default)
- `.env.development` - Development environment
- `.env.testing` - Testing environment  
- `.env.production` - Production environment (template)

### Setting Environment

**Windows PowerShell:**
```powershell
$env:APP_ENV="production"
```

**Linux/Mac:**
```bash
export APP_ENV=production
```

**Docker:**
```yaml
env_file:
  - .env.development  # or .env.production
```

### Environment-Specific Settings

#### Development
- **Debug Mode**: Enabled
- **Log Level**: DEBUG
- **Database**: Local MySQL
- **CORS**: Local development origins
- **Rate Limit**: 100 requests/minute

#### Testing
- **Debug Mode**: Disabled
- **Log Level**: WARNING
- **Database**: Test database
- **CORS**: Local testing origins
- **Rate Limit**: 1000 requests/minute (relaxed for testing)

#### Production
- **Debug Mode**: Disabled
- **Log Level**: INFO
- **Database**: Production MySQL
- **CORS**: Production frontend domains
- **Rate Limit**: 60 requests/minute

### Security Notes

**Never commit actual secrets to repository:**
- ✅ Use `.env.example` as template
- ✅ Keep actual `.env.production` secure
- ❌ Never commit `.env.production` with real secrets
- ❌ Never hardcode secrets in code

### Required Environment Variables

```bash
APP_ENV=development                    # Environment type
DEBUG=True                             # Debug mode
LOG_LEVEL=DEBUG                        # Logging level
DATABASE_URL=...                       # Database connection
SECRET_KEY=...                         # JWT secret key
ALGORITHM=HS256                        # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30        # Token expiration
GEMINI_API_KEY=...                     # Gemini AI API key
CORS_ORIGINS=...                       # Comma-separated CORS origins
RATE_LIMIT_ENABLED=True                # Enable rate limiting
RATE_LIMIT_PER_MINUTE=100              # Rate limit
```

### Configuration System

All configuration is centralized in `app/core/config.py`:
- **Settings class**: Type-safe configuration using Pydantic
- **Environment-based loading**: Automatically loads correct .env file
- **Helper methods**: `is_development()`, `is_testing()`, `is_production()`
- **Property methods**: `cors_origins_list` for parsing complex values

### Docker Deployment

For production Docker deployment:
1. Copy `.env.production` to `.env` on the server
2. Update with actual production values
3. Update `docker-compose.yml` to use `.env.production`
4. Ensure secrets are not committed to Git
