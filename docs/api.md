# API Documentation

## Overview

The AI Resume Analyzer & Job Matching Platform provides a RESTful API built with FastAPI. All endpoints return JSON responses and follow REST conventions.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.yourdomain.com`

## Authentication

### JWT Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Getting a Token

1. **Register**: `POST /auth/register`
2. **Login**: `POST /auth/login` - Returns JWT token

### Token Expiration

- **Expiration Time**: 30 minutes (configurable)
- **Refresh**: Client must re-login to get a new token

## Rate Limiting

- **Public Endpoints**: 100 requests/minute
- **Authenticated Endpoints**: 60 requests/minute
- **Rate Limit Headers**: 
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset time

## Response Format

### Success Response

```json
{
  "data": {
    // Response data
  },
  "message": "Success message"
}
```

### Error Response

```json
{
  "error": {
    "message": "Error message",
    "type": "ErrorType",
    "details": {
      // Additional error details
    }
  }
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Endpoints

### Authentication Endpoints

#### POST /auth/register

Register a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Response** (201):
```json
{
  "public_id": "usr_abc123",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "USER",
  "created_at": "2026-08-06T10:00:00Z"
}
```

**Error Response** (400):
```json
{
  "error": {
    "message": "Email already registered",
    "type": "ValidationError"
  }
}
```

#### POST /auth/login

Login and receive JWT token.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "public_id": "usr_abc123",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "USER"
  }
}
```

**Error Response** (401):
```json
{
  "error": {
    "message": "Invalid email or password",
    "type": "AuthenticationError"
  }
}
```

#### GET /profile

Get current user profile (requires authentication).

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "public_id": "usr_abc123",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "USER",
  "created_at": "2026-08-06T10:00:00Z"
}
```

**Error Response** (401):
```json
{
  "error": {
    "message": "Invalid or expired token",
    "type": "AuthenticationError"
  }
}
```

### Resume Endpoints

#### POST /resume/upload

Upload and parse a resume file.

**Authentication**: Required

**Content-Type**: `multipart/form-data`

**Request**:
```
file: <resume_file.pdf or .docx>
```

**Response** (201):
```json
{
  "public_id": "res_xyz789",
  "user_public_id": "usr_abc123",
  "file_name": "resume.pdf",
  "file_type": "application/pdf",
  "file_size": 245789,
  "uploaded_at": "2026-08-06T10:05:00Z",
  "extracted_data": {
    "skills": ["Python", "FastAPI", "MySQL"],
    "experience": [
      {
        "company": "Tech Company",
        "position": "Software Engineer",
        "duration": "2 years"
      }
    ],
    "education": [
      {
        "degree": "Bachelor of Science",
        "field": "Computer Science",
        "institution": "University"
      }
    ],
    "projects": [
      {
        "name": "Project Name",
        "description": "Project description",
        "technologies": ["Python", "React"]
      }
    ]
  }
}
```

**Error Response** (400):
```json
{
  "error": {
    "message": "Invalid file type. Only PDF and DOCX are supported.",
    "type": "ValidationError"
  }
}
```

#### GET /resume/{public_id}

Get resume details by public ID.

**Authentication**: Required

**Response** (200):
```json
{
  "public_id": "res_xyz789",
  "user_public_id": "usr_abc123",
  "file_name": "resume.pdf",
  "file_type": "application/pdf",
  "file_size": 245789,
  "uploaded_at": "2026-08-06T10:05:00Z",
  "extracted_data": {
    "skills": ["Python", "FastAPI", "MySQL"],
    "experience": [...],
    "education": [...],
    "projects": [...]
  },
  "analysis": {
    "overall_score": 85,
    "summary": "Strong technical profile with relevant experience",
    "strengths": ["Strong Python skills", "Good project experience"],
    "weaknesses": ["Limited leadership experience"],
    "recommendations": ["Add more quantified achievements"]
  }
}
```

**Error Response** (404):
```json
{
  "error": {
    "message": "Resume not found",
    "type": "NotFoundError"
  }
}
```

#### GET /resume/

Get all resumes for the current user.

**Authentication**: Required

**Query Parameters**:
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 10)

**Response** (200):
```json
{
  "resumes": [
    {
      "public_id": "res_xyz789",
      "file_name": "resume.pdf",
      "uploaded_at": "2026-08-06T10:05:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

#### DELETE /resume/{public_id}

Delete a resume by public ID.

**Authentication**: Required

**Response** (200):
```json
{
  "message": "Resume deleted successfully"
}
```

**Error Response** (404):
```json
{
  "error": {
    "message": "Resume not found",
    "type": "NotFoundError"
  }
}
```

### ATS Analysis Endpoints

#### POST /ats/analyze/{resume_public_id}

Generate ATS analysis for a resume.

**Authentication**: Required

**Response** (201):
```json
{
  "public_id": "ats_def456",
  "resume_public_id": "res_xyz789",
  "overall_score": 78,
  "score_breakdown": {
    "content_quality": 20,
    "skills_relevance": 18,
    "experience_depth": 22,
    "formatting_clarity": 18
  },
  "summary": "Well-structured resume with good technical content",
  "strengths": [
    "Clear technical skills section",
    "Good experience descriptions",
    "Professional formatting"
  ],
  "weaknesses": [
    "Could use more quantified achievements",
    "Missing some key keywords"
  ],
  "missing_skills": [
    "Docker",
    "Kubernetes"
  ],
  "recommendations": [
    "Add specific metrics to achievements",
    "Include industry-specific keywords",
    "Quantify project impacts"
  ],
  "keyword_suggestions": [
    "Agile",
    "CI/CD",
    "Microservices"
  ],
  "experience_level": "Mid-level",
  "top_skills": [
    "Python",
    "FastAPI",
    "MySQL",
    "JavaScript",
    "React"
  ],
  "created_at": "2026-08-06T10:10:00Z"
}
```

#### GET /ats/report/{resume_public_id}

Get detailed ATS report for a resume.

**Authentication**: Required

**Response** (200):
```json
{
  "resume_public_id": "res_xyz789",
  "ats_score": {
    "overall_score": 78,
    "content_quality": 20,
    "skills_relevance": 18,
    "experience_depth": 22,
    "formatting_clarity": 18
  },
  "keyword_analysis": {
    "matched_keywords": ["Python", "FastAPI", "MySQL"],
    "missing_keywords": ["Docker", "Kubernetes"],
    "keyword_score": 75
  },
  "format_analysis": {
    "ats_friendly": true,
    "section_completeness": 85,
    "format_score": 80
  },
  "experience_analysis": {
    "total_years": 5,
    "relevance_score": 85,
    "progression_score": 80
  },
  "education_analysis": {
    "degree_match": true,
    "field_relevance": 90,
    "education_score": 85
  },
  "project_analysis": {
    "total_projects": 4,
    "relevance_score": 80,
    "completeness_score": 75
  }
}
```

#### GET /ats/score/{resume_public_id}

Get ATS score for a resume.

**Authentication**: Required

**Response** (200):
```json
{
  "resume_public_id": "res_xyz789",
  "overall_score": 78,
  "content_quality": 20,
  "skills_relevance": 18,
  "experience_depth": 22,
  "formatting_clarity": 18,
  "created_at": "2026-08-06T10:10:00Z"
}
```

### Job Endpoints

#### POST /jobs/

Create a new job posting.

**Authentication**: Required

**Request**:
```json
{
  "title": "Senior Software Engineer",
  "description": "We are looking for a senior software engineer...",
  "requirements": "Python, FastAPI, MySQL, 5+ years experience",
  "location": "Remote",
  "salary_range": "$100,000 - $150,000",
  "company": "Tech Company"
}
```

**Response** (201):
```json
{
  "public_id": "job_ghi012",
  "title": "Senior Software Engineer",
  "description": "We are looking for a senior software engineer...",
  "requirements": "Python, FastAPI, MySQL, 5+ years experience",
  "location": "Remote",
  "salary_range": "$100,000 - $150,000",
  "company": "Tech Company",
  "created_at": "2026-08-06T10:15:00Z"
}
```

#### GET /jobs/

Get all job postings.

**Authentication**: Not required

**Query Parameters**:
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 10)

**Response** (200):
```json
{
  "jobs": [
    {
      "public_id": "job_ghi012",
      "title": "Senior Software Engineer",
      "company": "Tech Company",
      "location": "Remote",
      "salary_range": "$100,000 - $150,000",
      "created_at": "2026-08-06T10:15:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

#### GET /jobs/{public_id}

Get job details by public ID.

**Authentication**: Not required

**Response** (200):
```json
{
  "public_id": "job_ghi012",
  "title": "Senior Software Engineer",
  "description": "We are looking for a senior software engineer...",
  "requirements": "Python, FastAPI, MySQL, 5+ years experience",
  "location": "Remote",
  "salary_range": "$100,000 - $150,000",
  "company": "Tech Company",
  "created_at": "2026-08-06T10:15:00Z"
}
```

**Error Response** (404):
```json
{
  "error": {
    "message": "Job not found",
    "type": "NotFoundError"
  }
}
```

#### DELETE /jobs/{public_id}

Delete a job posting.

**Authentication**: Required

**Response** (200):
```json
{
  "message": "Job deleted successfully"
}
```

### Job Matching Endpoints

#### POST /matches/skill/{job_public_id}

Generate skill-based match for a job.

**Authentication**: Required

**Request**:
```json
{
  "resume_public_id": "res_xyz789"
}
```

**Response** (201):
```json
{
  "public_id": "match_jkl345",
  "job_public_id": "job_ghi012",
  "resume_public_id": "res_xyz789",
  "skill_match_score": 85,
  "matched_skills": ["Python", "FastAPI", "MySQL"],
  "missing_skills": ["Docker", "Kubernetes"],
  "skill_match_breakdown": {
    "technical_skills": 40,
    "soft_skills": 20,
    "domain_knowledge": 25
  },
  "created_at": "2026-08-06T10:20:00Z"
}
```

#### POST /matches/semantic/{job_public_id}

Generate semantic match for a job using AI.

**Authentication**: Required

**Request**:
```json
{
  "resume_public_id": "res_xyz789"
}
```

**Response** (201):
```json
{
  "public_id": "match_mno678",
  "job_public_id": "job_ghi012",
  "resume_public_id": "res_xyz789",
  "semantic_score": 88,
  "semantic_strengths": [
    "Strong technical background relevant to role",
    "Good project experience with similar technologies",
    "Clear career progression"
  ],
  "semantic_weaknesses": [
    "Limited experience with cloud technologies",
    "Could benefit from more leadership examples"
  ],
  "semantic_reason": "Candidate shows strong alignment with technical requirements and has relevant experience. Some gaps in cloud technologies but overall good fit.",
  "created_at": "2026-08-06T10:25:00Z"
}
```

#### GET /matches/recommendations/{resume_public_id}

Get job recommendations for a resume.

**Authentication**: Required

**Query Parameters**:
- `top_n` (optional): Number of recommendations to return (default: 5)
- `min_match` (optional): Minimum match score (default: 50)

**Response** (200):
```json
{
  "resume_public_id": "res_xyz789",
  "recommendations": [
    {
      "job_public_id": "job_ghi012",
      "title": "Senior Software Engineer",
      "company": "Tech Company",
      "overall_match": 82,
      "match_level": "Strong",
      "skill_match_score": 85,
      "experience_match_score": 80,
      "education_match_score": 75,
      "project_match_score": 78,
      "semantic_match_score": 88,
      "ats_score": 78
    }
  ],
  "total_jobs_analyzed": 15,
  "average_match_score": 72,
  "top_match_score": 82
}
```

#### GET /matches/{public_id}

Get match details by public ID.

**Authentication**: Required

**Response** (200):
```json
{
  "public_id": "match_jkl345",
  "job_public_id": "job_ghi012",
  "resume_public_id": "res_xyz789",
  "overall_match": 82,
  "match_level": "Strong",
  "skill_match_score": 85,
  "experience_match_score": 80,
  "education_match_score": 75,
  "project_match_score": 78,
  "semantic_match_score": 88,
  "ats_score": 78,
  "skill_match_breakdown": {
    "technical_skills": 40,
    "soft_skills": 20,
    "domain_knowledge": 25
  },
  "matched_skills": ["Python", "FastAPI", "MySQL"],
  "missing_skills": ["Docker", "Kubernetes"],
  "created_at": "2026-08-06T10:20:00Z"
}
```

## API Documentation UI

### Swagger UI

Interactive API documentation available at:
- **Development**: `http://localhost:8000/docs`
- **Production**: `https://api.yourdomain.com/docs`

### ReDoc

Alternative API documentation available at:
- **Development**: `http://localhost:8000/redoc`
- **Production**: `https://api.yourdomain.com/redoc`

## Error Handling

### Common Error Types

- `ValidationError`: Invalid request data
- `AuthenticationError`: Authentication failed
- `AuthorizationError`: Insufficient permissions
- `NotFoundError`: Resource not found
- `RateLimitExceeded`: Rate limit exceeded
- `InternalServerError`: Server error

### Error Response Format

All errors follow this format:

```json
{
  "error": {
    "message": "Human-readable error message",
    "type": "ErrorType",
    "details": {
      "field": "Additional error details"
    }
  }
}
```

## Pagination

List endpoints support pagination using `skip` and `limit` parameters:

```
GET /resume/?skip=0&limit=10
```

**Response includes**:
- `total`: Total number of records
- `skip`: Number of records skipped
- `limit`: Number of records returned

## Versioning

The API is currently at version 1.0. Future versions will be indicated in the URL:

```
https://api.yourdomain.com/v1/...
```

## Webhooks (Future)

Webhook support for real-time notifications:

- Resume analysis completed
- Job match generated
- New job posting matching profile

## SDKs (Future)

Official SDKs will be provided for:

- Python
- JavaScript/TypeScript
- Go

## Support

For API support and questions:
- Documentation: `/docs`
- Email: support@example.com
- GitHub Issues: https://github.com/yourusername/AI-Resume-Screener/issues
