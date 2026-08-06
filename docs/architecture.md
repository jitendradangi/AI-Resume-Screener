# System Architecture

## Overview

The AI Resume Analyzer & Job Matching Platform follows a layered architecture pattern with clear separation of concerns. The system is designed to be scalable, maintainable, and secure.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│                   (FastAPI + REST API)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Services   │  │   Matchers   │  │    ATS       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer                         │
│                    (Repositories + ORM)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Storage Layer                         │
│                       (MySQL Database)                       │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. API Layer (FastAPI)

**Purpose**: Handle HTTP requests, authentication, and response formatting

**Components**:
- **Routers**: API endpoint definitions
  - `auth.py`: Authentication endpoints
  - `resume.py`: Resume management endpoints
  - `jobs.py`: Job posting endpoints
  - `ats.py`: ATS analysis endpoints
  - `job_match.py`: Job matching endpoints

- **Middleware**: Cross-cutting concerns
  - CORS handling
  - Rate limiting
  - Request logging
  - Exception handling

- **Dependencies**: FastAPI dependency injection
  - `get_db()`: Database session management
  - `get_current_user()`: Authentication
  - `get_current_admin()`: Authorization

### 2. Business Logic Layer

**Purpose**: Implement core business rules and algorithms

**Components**:

#### Services
- **Resume Service**: Resume upload, parsing, and management
- **ATS Service**: ATS scoring and analysis orchestration
- **Job Match Service**: Job matching and recommendation orchestration

#### Matchers
- **Skill Matcher**: Skills-based job-resume matching
- **Experience Matcher**: Experience and seniority matching
- **Education Matcher**: Degree and field matching
- **Project Matcher**: Project relevance and completeness matching
- **Semantic Matcher**: AI-powered semantic analysis
- **Overall Matcher**: Weighted score aggregation
- **Recommendation Engine**: Job recommendation generation

#### ATS Engine
- **Keyword Extractor**: Extract and match keywords
- **Format Scorer**: Score resume formatting
- **Section Scorer**: Score resume sections
- **Experience Scorer**: Score experience quality
- **Education Scorer**: Score education quality
- **Project Scorer**: Score project quality
- **Overall Scorer**: Aggregate ATS scores

#### AI Components
- **Information Extractor**: Extract structured data from resumes
- **Resume Analyzer**: AI-powered resume analysis using Gemini

### 3. Data Access Layer

**Purpose**: Manage database operations and data persistence

**Components**:
- **Repositories**: Database operations abstraction
  - `user_repository.py`: User data operations
  - `resume_repository.py`: Resume data operations
  - `resume_analysis_repository.py`: Analysis data operations
  - `job_repository.py`: Job data operations
  - `job_match_repository.py`: Match data operations

- **ORM**: SQLAlchemy models
  - `User`: User accounts and authentication
  - `Resume`: Resume metadata and content
  - `ResumeAnalysis`: AI analysis results
  - `Job`: Job postings and requirements
  - `JobMatch`: Job-resume matching results
  - `ATSReport`: ATS analysis reports
  - `ATSScore`: ATS scoring breakdown

### 4. Data Storage Layer

**Purpose**: Persistent data storage

**Components**:
- **MySQL Database**: Relational data storage
- **File Storage**: Resume file storage (local/uploads)

### 5. Cross-Cutting Concerns

**Purpose**: Provide shared functionality across layers

**Components**:
- **Security**: JWT authentication, password hashing
- **Logging**: Comprehensive logging with rotation
- **Rate Limiting**: API rate limiting and abuse prevention
- **Configuration**: Environment-based configuration management
- **Exception Handling**: Centralized error handling

## Request Flow

### 1. Authentication Flow

```
User Request
    │
    ▼
POST /auth/login
    │
    ▼
Validate Credentials
    │
    ▼
Generate JWT Token
    │
    ▼
Return Token to Client
    │
    ▼
Client stores token
    │
    ▼
Subsequent requests include token
    │
    ▼
FastAPI validates token
    │
    ▼
Access granted/denied
```

### 2. Resume Upload Flow

```
POST /resume/upload
    │
    ▼
Authentication (JWT)
    │
    ▼
File Validation (PDF/DOCX)
    │
    ▼
Store File
    │
    ▼
Information Extractor
    │
    ▼
Parse and Extract Data
    │
    ▼
Resume Analyzer (AI)
    │
    ▼
Generate Analysis
    │
    ▼
Store in Database
    │
    ▼
Return Results
```

### 3. Job Matching Flow

```
POST /matches/skill/{job_id}
    │
    ▼
Authentication (JWT)
    │
    ▼
Retrieve Job & Resume
    │
    ▼
Skill Matcher
    │
    ▼
Experience Matcher
    │
    ▼
Education Matcher
    │
    ▼
Project Matcher
    │
    ▼
Semantic Matcher (AI)
    │
    ▼
Overall Matcher
    │
    ▼
Calculate Weighted Score
    │
    ▼
Store Match Results
    │
    ▼
Return Match Data
```

### 4. ATS Analysis Flow

```
POST /ats/analyze/{resume_id}
    │
    ▼
Authentication (JWT)
    │
    ▼
Retrieve Resume
    │
    ▼
Keyword Extractor
    │
    ▼
Format Scorer
    │
    ▼
Section Scorer
    │
    ▼
Experience Scorer
    │
    ▼
Education Scorer
    │
    ▼
Project Scorer
    │
    ▼
Overall Scorer
    │
    ▼
Generate ATS Report
    │
    ▼
Store Results
    │
    ▼
Return ATS Score
```

## Module Interactions

### Authentication Module

**Interactions**:
- Uses **Security Module** for password hashing and JWT generation
- Interacts with **User Repository** for user data operations
- Provides authentication to **API Layer** via dependency injection

### Resume Processing Module

**Interactions**:
- Uses **Information Extractor** for structured data extraction
- Uses **Resume Analyzer** for AI-powered analysis
- Interacts with **Resume Repository** for data persistence
- Provides data to **Job Matching Module**

### Job Matching Module

**Interactions**:
- Uses **Skill Matcher** for skills-based matching
- Uses **Experience Matcher** for experience matching
- Uses **Education Matcher** for education matching
- Uses **Project Matcher** for project matching
- Uses **Semantic Matcher** for AI semantic analysis
- Uses **Overall Matcher** for score aggregation
- Uses **Recommendation Engine** for job recommendations
- Interacts with **Job Repository** and **Resume Repository**
- Provides results to **API Layer**

### ATS Engine Module

**Interactions**:
- Uses **Keyword Extractor** for keyword analysis
- Uses **Format Scorer** for format evaluation
- Uses **Section Scorer** for section evaluation
- Uses **Experience Scorer** for experience evaluation
- Uses **Education Scorer** for education evaluation
- Uses **Project Scorer** for project evaluation
- Uses **Overall Scorer** for score aggregation
- Interacts with **Resume Repository** for data access
- Provides results to **API Layer**

### AI Integration Module

**Interactions**:
- Uses **Google Gemini API** for AI processing
- Provides analysis to **Resume Analyzer**
- Provides semantic analysis to **Semantic Matcher**
- Interacts with **Configuration Module** for API keys

## Technology Stack Mapping

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Presentation | FastAPI | Web framework and API |
| Business Logic | Python | Core application logic |
| AI/ML | Google Gemini AI | AI-powered analysis |
| Data Access | SQLAlchemy | ORM and database operations |
| Data Storage | MySQL | Relational database |
| Authentication | JWT (python-jose) | Token-based authentication |
| Security | bcrypt | Password hashing |
| Rate Limiting | slowapi | API rate limiting |
| Logging | Python logging | Application logging |
| Configuration | pydantic-settings | Configuration management |
| Containerization | Docker | Application containerization |

## Scalability Considerations

### Horizontal Scaling

- **API Layer**: Can be scaled horizontally using load balancers
- **Database**: Use read replicas for read-heavy operations
- **AI Processing**: Can be offloaded to separate services
- **File Storage**: Can use cloud storage (S3, etc.)

### Performance Optimization

- **Caching**: Implement Redis caching for frequently accessed data
- **Database Indexing**: Proper indexing on frequently queried fields
- **Connection Pooling**: SQLAlchemy connection pooling
- **Async Processing**: Use Celery for background tasks

### Security Considerations

- **Authentication**: JWT-based authentication with expiration
- **Authorization**: Role-based access control (USER, ADMIN)
- **Rate Limiting**: Prevent API abuse and DDoS attacks
- **Input Validation**: Pydantic schemas for request validation
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
- **Secret Management**: Environment variables for sensitive data

## Monitoring and Observability

### Logging

- **Application Logs**: Comprehensive logging of all operations
- **Error Logs**: Separate error logging for troubleshooting
- **Request Logging**: HTTP request/response logging
- **Log Rotation**: Automatic log file rotation

### Metrics (Future)

- **API Response Times**: Track API performance
- **Error Rates**: Monitor error occurrences
- **User Activity**: Track user engagement
- **AI Processing Times**: Monitor AI service performance

## Deployment Architecture

### Development Environment

```
Developer Machine
    │
    ▼
Local MySQL
    │
    ▼
FastAPI (uvicorn)
    │
    ▼
Local File Storage
```

### Production Environment

```
Load Balancer
    │
    ▼
Multiple FastAPI Instances
    │
    ▼
MySQL Database (with replicas)
    │
    ▼
Cloud File Storage (S3)
    │
    ▼
Redis Cache (optional)
```

## Data Flow Diagram

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│   FastAPI   │
└──────┬──────┘
       │
       ├─────────────┬─────────────┬─────────────┐
       ▼             ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Auth    │  │  Resume  │  │   Jobs   │  │   ATS    │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │             │
     ▼             ▼             ▼             ▼
┌──────────────────────────────────────────────────────┐
│              SQLAlchemy Repositories                  │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                   MySQL Database                      │
└──────────────────────────────────────────────────────┘
```

## External Service Integration

### Google Gemini AI

**Purpose**: AI-powered resume analysis and semantic matching

**Integration Points**:
- Resume Analyzer: AI-powered resume quality analysis
- Semantic Matcher: AI-powered job-resume semantic analysis

**Error Handling**:
- Graceful degradation when AI service is unavailable
- Retry logic for transient failures
- Fallback to rule-based matching when AI fails

### File Storage

**Current**: Local file storage
**Future**: Cloud storage (AWS S3, Google Cloud Storage)

**Integration Points**:
- Resume upload and storage
- File retrieval for analysis

## Security Architecture

### Authentication Flow

```
1. User Login
   │
   ▼
2. Validate Credentials
   │
   ▼
3. Generate JWT Token
   │
   ▼
4. Return Token to Client
   │
   ▼
5. Client includes token in requests
   │
   ▼
6. FastAPI validates token
   │
   ▼
7. Access granted/denied
```

### Authorization Flow

```
1. Authenticated Request
   │
   ▼
2. Check User Role
   │
   ▼
3. Validate Permissions
   │
   ▼
4. Allow/Deny Access
```

### Data Protection

- **Passwords**: Hashed with bcrypt
- **JWT Tokens**: Signed with secret key, have expiration
- **API Keys**: Stored in environment variables
- **Database**: Connection via environment variables
- **Files**: Secure file upload and storage

## Future Architecture Enhancements

### Microservices

- **Split into microservices**: Separate services for different domains
- **API Gateway**: Central API gateway for routing
- **Service Discovery**: Service discovery mechanism
- **Message Queue**: Event-driven architecture with message queues

### Caching Layer

- **Redis**: Implement Redis for caching
- **Cache Invalidation**: Proper cache invalidation strategies
- **Distributed Caching**: Support for distributed caching

### Advanced AI

- **Custom ML Models**: Train custom ML models for better accuracy
- **Model Versioning**: Model versioning and A/B testing
- **Feature Store**: Feature store for ML features

### Advanced Monitoring

- **APM Tools**: Application Performance Monitoring
- **Distributed Tracing**: Distributed tracing for microservices
- **Real-time Monitoring**: Real-time monitoring and alerting
