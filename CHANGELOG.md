# Changelog

All notable changes to the AI Resume Analyzer & Job Matching Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Professional README.md with comprehensive documentation
- CONTRIBUTING.md with contribution guidelines
- LICENSE file (MIT License)
- Production configuration system with environment-specific files
- Centralized configuration management with Pydantic Settings
- GitHub Actions CI/CD pipeline
- Rate limiting with slowapi
- Comprehensive logging system with file rotation
- Custom exception handling framework
- Environment-based configuration (development, testing, production)
- Docker containerization with health checks
- Security improvements with environment variable management

### Changed
- Updated Docker configuration to use environment-specific files
- Refactored security module to use centralized configuration
- Updated logging to support environment-based log levels
- Improved CORS configuration with environment variable support
- Enhanced rate limiting with configurable limits per environment

### Fixed
- Docker database connection issues with proper health checks
- Environment variable loading for different deployment scenarios
- Rate limiting decorator issues with request parameter handling

### Security
- Removed hardcoded secrets from source code
- Added environment-specific configuration files
- Implemented secure secret management
- Added .gitignore rules for sensitive files

## [1.0.0] - 2026-08-06

### Added
- Initial release of AI Resume Analyzer & Job Matching Platform
- User authentication with JWT tokens
- Resume upload and parsing (PDF/DOCX)
- AI-powered resume analysis with Google Gemini
- ATS scoring engine with comprehensive analysis
- Job matching algorithms (skills, experience, semantic)
- Job recommendation engine
- Project matching functionality
- Education matching functionality
- Overall match score calculation
- RESTful API with FastAPI
- MySQL database with SQLAlchemy ORM
- Docker support with docker-compose
- API documentation with Swagger UI
- Rate limiting and logging
- Custom exception handling

### Features
- **Authentication**: JWT-based user authentication and authorization
- **Resume Processing**: 
  - PDF and DOCX file parsing
  - Information extraction (skills, experience, education, projects)
  - AI-powered quality analysis
- **ATS Engine**:
  - Keyword extraction and matching
  - Format scoring
  - Section scoring
  - Experience scoring
  - Education scoring
  - Project scoring
  - Overall ATS score calculation
- **Job Matching**:
  - Skill matching with weighted scoring
  - Experience matching (seniority, domain)
  - Education matching (degree, field)
  - Project matching (relevance, completeness)
  - Semantic matching with AI
  - Overall match score calculation
  - Job recommendation engine
- **Infrastructure**:
  - Rate limiting for API protection
  - Comprehensive logging with file rotation
  - Custom exception handling
  - Environment-based configuration
  - Docker containerization
  - CI/CD with GitHub Actions

### Security
- Password hashing with bcrypt
- JWT token authentication
- Environment variable management
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy

## [0.1.0] - 2026-07-15

### Added
- Project initialization
- Basic FastAPI setup
- Database schema design
- User authentication system
- Resume upload functionality
- Basic ATS scoring

---

## Version Format

- **Major**: Breaking changes or major new features
- **Minor**: New features in a backwards-compatible manner
- **Patch**: Bug fixes in a backwards-compatible manner
