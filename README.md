# AI Resume Analyzer & Job Matching Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**An intelligent AI-powered platform for resume analysis, ATS scoring, and job matching**

</div>

## 📋 Overview

The AI Resume Analyzer & Job Matching Platform is a comprehensive system that leverages artificial intelligence to transform traditional recruitment processes. It provides intelligent resume parsing, automated ATS (Applicant Tracking System) scoring, quality analysis, and smart job matching capabilities.

### Key Capabilities

- **📄 Resume Parsing**: Extract structured data from PDF and DOCX resume files
- **🤖 AI Analysis**: Powered by Google Gemini AI for deep resume analysis
- **📊 ATS Scoring**: Generate comprehensive ATS scores with detailed breakdowns
- **🎯 Job Matching**: Intelligent matching between resumes and job descriptions
- **💡 Recommendations**: AI-powered job recommendations based on candidate profiles
- **🔒 Secure Authentication**: JWT-based user authentication and authorization

## ✨ Features

### Core Features
- **User Authentication (JWT)**: Secure user registration and login with JWT tokens
- **Resume Upload (PDF/DOCX)**: Support for multiple resume file formats
- **AI Resume Parsing**: Intelligent extraction of skills, experience, education, and projects
- **ATS Score Generation**: Comprehensive ATS scoring with detailed analysis
- **Resume Quality Analysis**: AI-powered strengths, weaknesses, and recommendations
- **Job Matching**: Multi-dimensional job-resume matching (skills, experience, semantic)
- **Job Recommendation Engine**: Personalized job recommendations based on candidate profiles
- **Docker Support**: Complete containerization for easy deployment
- **REST APIs**: Well-documented RESTful API endpoints
- **Production Ready**: Rate limiting, logging, error handling, and environment configuration

### Advanced Features
- **Semantic Matching**: AI-powered semantic analysis for job-resume fit
- **Project Matching**: Evaluation of project relevance and completeness
- **Education Matching**: Degree and field alignment analysis
- **Experience Matching**: Seniority and domain expertise evaluation
- **Overall Match Score**: Weighted scoring across multiple dimensions
- **Rate Limiting**: Protection against API abuse
- **Comprehensive Logging**: Professional logging with file rotation
- **Environment Configuration**: Separate configs for development, testing, and production

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.139.2
- **Language**: Python 3.13
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0.51
- **Authentication**: JWT (python-jose, passlib)
- **AI/ML**: Google Gemini AI (google-generativeai)
- **File Processing**: PyMuDF (PDF), python-docx (DOCX)
- **API Documentation**: FastAPI built-in Swagger UI

### DevOps & Infrastructure
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Version Control**: Git
- **Rate Limiting**: slowapi
- **Logging**: Python logging with rotation
- **Environment Management**: python-dotenv, pydantic-settings

### Development Tools
- **Testing**: pytest
- **Code Quality**: flake8
- **Package Management**: pip
- **Virtual Environment**: venv

## 📁 Project Structure

```
AI-Resume-Screener/
├── backend/
│   ├── app/
│   │   ├── ai/                    # AI-powered analysis
│   │   │   ├── information_extractor.py
│   │   │   └── resume_analyzer.py
│   │   ├── ats/                   # ATS scoring engine
│   │   │   ├── keyword_extractor.py
│   │   │   ├── format_scorer.py
│   │   │   ├── section_scorer.py
│   │   │   ├── experience_scorer.py
│   │   │   ├── education_scorer.py
│   │   │   ├── project_scorer.py
│   │   │   └── overall_scorer.py
│   │   ├── core/                  # Core functionality
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging_config.py
│   │   │   └── rate_limit.py
│   │   ├── database/              # Database configuration
│   │   │   ├── base.py
│   │   │   └── db.py
│   │   ├── dependencies.py        # FastAPI dependencies
│   │   ├── exceptions/            # Custom exceptions
│   │   │   ├── custom_exceptions.py
│   │   │   ├── handler.py
│   │   │   └── __init__.py
│   │   ├── matching/              # Job matching algorithms
│   │   │   ├── skill_matcher.py
│   │   │   ├── experience_matcher.py
│   │   │   ├── education_matcher.py
│   │   │   ├── project_matcher.py
│   │   │   ├── semantic_matcher.py
│   │   │   ├── overall_matcher.py
│   │   │   └── recommendation_engine.py
│   │   ├── models/                # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── resume_analysis.py
│   │   │   ├── job.py
│   │   │   ├── job_match.py
│   │   │   ├── ats_report.py
│   │   │   └── ats_score.py
│   │   ├── repositories/          # Database repositories
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── resume_analysis.py
│   │   │   ├── job.py
│   │   │   └── job_match.py
│   │   ├── routers/               # API routes
│   │   │   ├── auth.py
│   │   │   ├── resume.py
│   │   │   ├── jobs.py
│   │   │   ├── ats.py
│   │   │   └── job_match.py
│   │   ├── schemas/               # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── job.py
│   │   │   └── job_match.py
│   │   ├── services/              # Business logic
│   │   │   ├── resume.py
│   │   │   ├── ats.py
│   │   │   └── job_match.py
│   │   └── main.py                # FastAPI application
│   ├── tests/                     # Test files
│   ├── logs/                      # Application logs
│   ├── requirements.txt           # Python dependencies
│   ├── Dockerfile                 # Docker configuration
│   ├── docker-compose.yml         # Docker Compose configuration
│   ├── .env.development           # Development environment
│   ├── .env.testing               # Testing environment
│   ├── .env.production            # Production environment template
│   ├── .env.example               # Environment variables template
│   └── PRODUCTION_CONFIG.md       # Production deployment guide
├── .github/
│   └── workflows/
│       └── backend-ci.yml         # GitHub Actions CI/CD
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🏗 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                       │
│                    (Authentication Dashboard)                  │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Authentication (JWT + Authorization)         │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Resume Processing Layer                  │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │  │
│  │  │ File Parser  │  │ Information  │  │   AI       │  │  │
│  │  │ (PDF/DOCX)   │  │  Extractor   │  │  Analyzer  │  │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Analysis & Matching Layer                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │  │
│  │  │  ATS Engine  │  │  Job Matcher │  │Recommendation│  │  │
│  │  │              │  │              │  │   Engine    │  │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Rate Limiting & Logging                   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ SQLAlchemy ORM
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      MySQL Database                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │  Users   │ │ Resumes  │ │   Jobs   │ │  Job Matches  │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Services                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Google Gemini AI API                      │  │
│  │           (AI Analysis & Semantic Matching)           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔌 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Login and get JWT token | No |
| GET | `/profile` | Get current user profile | Yes |

### Resume Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/resume/upload` | Upload and parse resume | Yes |
| GET | `/resume/{public_id}` | Get resume details | Yes |
| GET | `/resume/` | Get all user resumes | Yes |
| DELETE | `/resume/{public_id}` | Delete resume | Yes |

### ATS Analysis Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/ats/analyze/{resume_public_id}` | Generate ATS analysis | Yes |
| GET | `/ats/report/{resume_public_id}` | Get ATS report | Yes |
| GET | `/ats/score/{resume_public_id}` | Get ATS score | Yes |

### Job Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/jobs/` | Create new job posting | Yes |
| GET | `/jobs/` | Get all jobs | No |
| GET | `/jobs/{public_id}` | Get job details | No |
| DELETE | `/jobs/{public_id}` | Delete job | Yes |

### Job Matching Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/matches/skill/{job_public_id}` | Generate skill match | Yes |
| POST | `/matches/semantic/{job_public_id}` | Generate semantic match | Yes |
| GET | `/matches/recommendations/{resume_public_id}` | Get job recommendations | Yes |
| GET | `/matches/{public_id}` | Get match details | Yes |

### Rate Limits

- **Public endpoints**: 100 requests/minute
- **Authenticated endpoints**: 60 requests/minute

## 🚀 Installation Guide

### Prerequisites

- Python 3.13+
- MySQL 8.0+
- pip (Python package manager)

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AI-Resume-Screener.git
cd AI-Resume-Screener/backend
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your actual values
```

6. **Set up MySQL database**
```sql
CREATE DATABASE ai_resume_screener;
```

7. **Run the application**
```bash
uvicorn app.main:app --reload
```

8. **Access API documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🐳 Docker Guide

### Using Docker Compose

1. **Build and start containers**
```bash
cd backend
docker compose up --build
```

2. **Access the application**
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

3. **Stop containers**
```bash
docker compose down
```

4. **View logs**
```bash
docker compose logs -f
```

### Docker Commands

```bash
# Build only
docker compose build

# Start in detached mode
docker compose up -d

# Restart services
docker compose restart

# Remove containers and volumes
docker compose down -v
```

## 🔐 Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```bash
# Application Environment
APP_ENV=development
DEBUG=True
LOG_LEVEL=DEBUG

# Database Configuration
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ai_resume_screener

# JWT Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Groq AI Configuration
GROQ_API_KEY=your-groq-api-key-here

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=100
```

### Environment-Specific Files

- **Development**: `.env.development`
- **Testing**: `.env.testing`
- **Production**: `.env.production`

For detailed production configuration, see [PRODUCTION_CONFIG.md](backend/PRODUCTION_CONFIG.md)

## 📸 Screenshots

*Note: Screenshots will be added when the frontend is developed*

- Login Screen
- User Dashboard
- Resume Upload Interface
- ATS Analysis Report
- Job Matching Results
- Job Recommendations Panel

## 🔮 Future Enhancements

### Planned Features

- **LinkedIn Profile Analysis**: Integrate LinkedIn API for profile enrichment
- **Multi-language Resume Parsing**: Support for resumes in multiple languages
- **AI Interview Preparation**: Generate interview questions based on job requirements
- **Resume Version Comparison**: Track and compare resume versions over time
- **Cover Letter Generation**: AI-powered cover letter generation
- **Video Resume Support**: Analyze video resumes with AI
- **Advanced Analytics**: Recruitment analytics and insights dashboard
- **Email Notifications**: Automated email notifications for job matches
- **Mobile App**: Native mobile applications for iOS and Android
- **Integration APIs**: API integrations with popular ATS systems

### Technical Improvements

- **Caching Layer**: Redis caching for improved performance
- **Message Queue**: Celery for background task processing
- **Microservices Architecture**: Split into microservices for scalability
- **GraphQL API**: Alternative GraphQL API for flexible queries
- **Webhook Support**: Webhooks for real-time notifications
- **Advanced Search**: Elasticsearch for advanced resume search
- **Machine Learning Models**: Custom ML models for better matching accuracy

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions and support, please contact [your-email@example.com]

## 🙏 Acknowledgments

- Google Gemini AI for powering the AI analysis
- FastAPI for the excellent web framework
- The open-source community for amazing tools and libraries

---

<div align="center">

**Built with ❤️ for the recruitment industry**

</div>
