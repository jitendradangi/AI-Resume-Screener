# Database Documentation

## Overview

The AI Resume Analyzer & Job Matching Platform uses MySQL 8.0 as its primary database. The database is designed to support user management, resume storage, job postings, ATS analysis, and job matching functionality.

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐
│      User       │       │     Resume      │
├─────────────────┤       ├─────────────────┤
│ public_id (PK)  │◄──────│ user_public_id  │
│ email           │       │ public_id (PK)  │
│ password_hash   │       │ file_name       │
│ full_name       │       │ file_type       │
│ role            │       │ file_size       │
│ created_at      │       │ uploaded_at     │
└─────────────────┘       │ extracted_data  │
                          └────────┬────────┘
                                   │
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
        ┌─────────────────────┐       ┌─────────────────────┐
        │  ResumeAnalysis     │       │    JobMatch         │
        ├─────────────────────┤       ├─────────────────────┤
        │ public_id (PK)      │       │ public_id (PK)      │
        │ resume_public_id    │       │ job_public_id       │
        │ overall_score       │       │ resume_public_id    │
        │ summary             │       │ overall_match       │
        │ strengths           │       │ match_level         │
        │ weaknesses          │       │ skill_match_score   │
        │ recommendations     │       │ experience_match_   │
        │ created_at          │       │   score             │
        └─────────────────────┘       │ education_match_    │
                                     │   score             │
        ┌─────────────────────┐       │ project_match_score │
        │      Job            │       │ semantic_match_    │
        ├─────────────────────┤       │   score             │
        │ public_id (PK)      │       │ ats_score          │
        │ title               │       │ created_at          │
        │ description         │       └─────────────────────┘
        │ requirements        │
        │ location            │       ┌─────────────────────┐
        │ salary_range        │       │    ATSReport        │
        │ company             │       ├─────────────────────┤
        │ created_at          │       │ public_id (PK)      │
        └─────────────────────┘       │ resume_public_id    │
                                     │ ats_score_id        │
        ┌─────────────────────┐       │ keyword_analysis    │
        │    ATSScore         │       │ format_analysis     │
        ├─────────────────────┤       │ experience_analysis │
        │ public_id (PK)      │       │ education_analysis  │
        │ resume_public_id    │       │ project_analysis    │
        │ overall_score       │       │ created_at          │
        │ content_quality     │       └─────────────────────┘
        │ skills_relevance    │
        │ experience_depth    │
        │ formatting_clarity  │
        │ created_at          │
        └─────────────────────┘
```

## Table Descriptions

### User

Stores user account information and authentication data.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Internal database ID |
| `public_id` | VARCHAR(36) | UNIQUE, NOT NULL | Public identifier for API |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `full_name` | VARCHAR(255) | NOT NULL | User's full name |
| `role` | ENUM('USER', 'ADMIN') | DEFAULT 'USER' | User role for authorization |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| `updated_at` | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE INDEX (`public_id`)
- UNIQUE INDEX (`email`)

**Relationships**:
- One-to-Many with Resume (user_public_id)

### Resume

Stores resume file information and extracted structured data.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Internal database ID |
| `public_id` | VARCHAR(36) | UNIQUE, NOT NULL | Public identifier for API |
| `user_public_id` | VARCHAR(36) | FK, NOT NULL | Reference to User |
| `file_name` | VARCHAR(255) | NOT NULL | Original file name |
| `file_type` | VARCHAR(100) | NOT NULL | MIME type (application/pdf, etc.) |
| `file_size` | INT | NOT NULL | File size in bytes |
| `file_path` | VARCHAR(500) | NOT NULL | Path to stored file |
| `extracted_data` | JSON | NULL | Extracted structured data |
| `uploaded_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Upload timestamp |
| `updated_at` | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE INDEX (`public_id`)
- INDEX (`user_public_id`)

**Relationships**:
- Many-to-One with User (user_public_id)
- One-to-One with ResumeAnalysis (resume_public_id)
- One-to-Many with JobMatch (resume_public_id)
- One-to-One with ATSReport (resume_public_id)
- One-to-One with ATSScore (resume_public_id)

### ResumeAnalysis

Stores AI-powered resume analysis results.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Internal database ID |
| `public_id` | VARCHAR(36) | UNIQUE, NOT NULL | Public identifier for API |
| `resume_public_id` | VARCHAR(36) | FK, UNIQUE, NOT NULL | Reference to Resume |
| `overall_score` | INT | NOT NULL, CHECK(0-100) | Overall quality score (0-100) |
| `summary` | TEXT | NULL | Professional summary |
| `strengths` | JSON | NULL | List of strengths |
| `weaknesses` | JSON | NULL | List of weaknesses |
| `recommendations` | JSON | NULL | List of recommendations |
| `missing_skills` | JSON | NULL | List of missing skills |
| `keyword_suggestions` | JSON | NULL | Suggested ATS keywords |
| `experience_level` | VARCHAR(50) | NULL | Experience level classification |
| `top_skills` | JSON | NULL | Top 5 skills |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Analysis timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE INDEX (`public_id`)
- UNIQUE INDEX (`resume_public_id`)

**Relationships**:
- One-to-One with Resume (resume_public_id)

### Job

Stores job posting information.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Internal database ID |
| `public_id` | VARCHAR(36) | UNIQUE, NOT NULL | Public identifier for API |
| `title` | VARCHAR(255) | NOT NULL | Job title |
| `description` | TEXT | NOT NULL | Job description |
| `requirements` | TEXT | NOT NULL | Job requirements |
| `location` | VARCHAR(255) | NULL | Job location |
| `salary_range` | VARCHAR(100) | NULL | Salary range |
| `company` | VARCHAR(255) | NOT NULL | Company name |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE INDEX (`public_id`)
- INDEX (`title`)
- INDEX (`company`)

**Relationships**:
- One-to-Many with JobMatch (job_public_id)

### JobMatch

Stores job-resume matching results.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Internal database ID |
| `public_id` | VARCHAR(36) | UNIQUE, NOT NULL | Public identifier for API |
| `job_public_id` | VARCHAR(36) | FK, NOT NULL | Reference to Job |
| `resume_public_id` | VARCHAR(36) | FK, NOT NULL | Reference to Resume |
| `overall_match` | INT | NOT NULL, CHECK(0-100) | Overall match score (0-100) |
| `match_level` | VARCHAR(50) | NOT NULL | Match level classification |
| `skill_match_score` | INT | NULL | Skill match score (0-100) |
| `experience_match_score` | INT | NULL | Experience match score (0-100) |
| `education_match_score` | INT | NULL | Education match score (0-100) |
| `project_match_score` | INT | NULL | Project match score (0-100) |
| `semantic_match_score` | INT | NULL | Semantic match score (0-100) |
| `ats_score` | INT | NULL | ATS score (0-100) |
| `skill_match_breakdown` | JSON | NULL | Detailed skill match breakdown |
| `matched_skills` | JSON | NULL | List of matched skills |
| `missing_skills` | JSON | NULL | List of missing skills |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Match timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE INDEX (`public_id`)
- INDEX (`job_public_id`)
- INDEX (`resume_public_id`)
- INDEX (`overall_match`)

**Relationships**:
- Many-to-One with Job (job_public_id)
- Many-to-One with Resume (resume_public_id)

### ATSReport

Stores detailed ATS analysis reports.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Internal database ID |
| `public_id` | VARCHAR(36) | UNIQUE, NOT NULL | Public identifier for API |
| `resume_public_id` | VARCHAR(36) | FK, UNIQUE, NOT NULL | Reference to Resume |
| `ats_score_id` | VARCHAR(36) | FK, NULL | Reference to ATSScore |
| `keyword_analysis` | JSON | NULL | Keyword analysis results |
| `format_analysis` | JSON | NULL | Format analysis results |
| `experience_analysis` | JSON | NULL | Experience analysis results |
| `education_analysis` | JSON | NULL | Education analysis results |
| `project_analysis` | JSON | NULL | Project analysis results |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Report timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE INDEX (`public_id`)
- UNIQUE INDEX (`resume_public_id`)
- INDEX (`ats_score_id`)

**Relationships**:
- One-to-One with Resume (resume_public_id)
- Many-to-One with ATSScore (ats_score_id)

### ATSScore

Stores ATS scoring breakdown.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Internal database ID |
| `public_id` | VARCHAR(36) | UNIQUE, NOT NULL | Public identifier for API |
| `resume_public_id` | VARCHAR(36) | FK, UNIQUE, NOT NULL | Reference to Resume |
| `overall_score` | INT | NOT NULL, CHECK(0-100) | Overall ATS score (0-100) |
| `content_quality` | INT | NOT NULL, CHECK(0-25) | Content quality score (0-25) |
| `skills_relevance` | INT | NOT NULL, CHECK(0-25) | Skills relevance score (0-25) |
| `experience_depth` | INT | NOT NULL, CHECK(0-25) | Experience depth score (0-25) |
| `formatting_clarity` | INT | NOT NULL, CHECK(0-25) | Formatting clarity score (0-25) |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Score timestamp |

**Indexes**:
- PRIMARY KEY (`id`)
- UNIQUE INDEX (`public_id`)
- UNIQUE INDEX (`resume_public_id`)

**Relationships**:
- One-to-One with Resume (resume_public_id)
- One-to-Many with ATSReport (ats_score_id)

## Relationships

### User → Resume (One-to-Many)

- A user can have multiple resumes
- A resume belongs to exactly one user
- Foreign key: `Resume.user_public_id` → `User.public_id`

### Resume → ResumeAnalysis (One-to-One)

- A resume has one analysis
- An analysis belongs to exactly one resume
- Foreign key: `ResumeAnalysis.resume_public_id` → `Resume.public_id`

### Resume → ATSScore (One-to-One)

- A resume has one ATS score
- An ATS score belongs to exactly one resume
- Foreign key: `ATSScore.resume_public_id` → `Resume.public_id`

### Resume → ATSReport (One-to-One)

- A resume has one ATS report
- An ATS report belongs to exactly one resume
- Foreign key: `ATSReport.resume_public_id` → `Resume.public_id`

### Resume → JobMatch (One-to-Many)

- A resume can have multiple job matches
- A job match belongs to exactly one resume
- Foreign key: `JobMatch.resume_public_id` → `Resume.public_id`

### Job → JobMatch (One-to-Many)

- A job can have multiple matches
- A job match belongs to exactly one job
- Foreign key: `JobMatch.job_public_id` → `Job.public_id`

### ATSScore → ATSReport (One-to-Many)

- An ATS score can have multiple reports
- An ATS report belongs to exactly one ATS score
- Foreign key: `ATSReport.ats_score_id` → `ATSScore.public_id`

## Database Initialization

### Create Database

```sql
CREATE DATABASE ai_resume_screener
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### Create Tables

Tables are automatically created by SQLAlchemy when the application starts:

```python
from app.database.base import Base
from app.database.db import engine

Base.metadata.create_all(bind=engine)
```

## Data Integrity

### Constraints

- **Primary Keys**: All tables have auto-incrementing primary keys
- **Foreign Keys**: Referential integrity enforced
- **Unique Constraints**: Public IDs are unique across tables
- **Check Constraints**: Scores are validated to be within valid ranges
- **NOT NULL**: Required fields are enforced

### Transactions

All database operations use transactions to ensure data consistency:

```python
from sqlalchemy.orm import Session

def create_user(db: Session, user_data: dict):
    try:
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e
```

## Backup and Recovery

### Backup

```bash
# Full database backup
mysqldump -u root -p ai_resume_screener > backup.sql

# Compressed backup
mysqldump -u root -p ai_resume_screener | gzip > backup.sql.gz
```

### Restore

```bash
# Restore from backup
mysql -u root -p ai_resume_screener < backup.sql

# Restore from compressed backup
gunzip < backup.sql.gz | mysql -u root -p ai_resume_screener
```

## Performance Optimization

### Indexes

- All foreign keys are indexed
- Public IDs have unique indexes
- Frequently queried fields are indexed
- Composite indexes for common query patterns

### Query Optimization

- Use joins instead of multiple queries
- Select only required columns
- Use pagination for large result sets
- Implement query caching for frequently accessed data

### Connection Pooling

SQLAlchemy connection pooling is configured:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

## Security

### Access Control

- Database access restricted to application user
- No direct database access from outside
- Credentials stored in environment variables

### Data Encryption

- Passwords hashed with bcrypt
- Sensitive data not stored in plain text
- Consider encryption for PII in production

### SQL Injection Prevention

- SQLAlchemy ORM prevents SQL injection
- Parameterized queries used throughout
- Input validation via Pydantic schemas

## Maintenance

### Regular Tasks

- **Daily**: Monitor database performance
- **Weekly**: Review slow query logs
- **Monthly**: Analyze storage usage and growth
- **Quarterly**: Review and optimize indexes

### Cleanup

Remove old data periodically:

```sql
-- Delete matches older than 90 days
DELETE FROM job_match 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);

-- Delete old ATS reports
DELETE FROM ats_report 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 180 DAY);
```

## Monitoring

### Key Metrics

- Database connection pool usage
- Query execution times
- Table sizes and growth rates
- Index efficiency
- Slow query frequency

### Alerts

Set up alerts for:
- High connection pool usage
- Slow queries (> 1 second)
- Database connection failures
- Disk space threshold

## Future Enhancements

### Planned Improvements

- **Read Replicas**: For read-heavy operations
- **Partitioning**: For large tables (JobMatch)
- **Full-Text Search**: For job and resume search
- **Caching Layer**: Redis for frequently accessed data
- **Data Archiving**: Move old data to cold storage
- **Migration Scripts**: Automated schema migrations

### Scalability

- **Sharding**: Horizontal scaling for large datasets
- **Multi-Region**: Geographic distribution
- **Disaster Recovery**: High availability setup
- **Load Balancing**: Database load balancing

## Troubleshooting

### Common Issues

**Connection Issues**:
- Check DATABASE_URL in environment variables
- Verify MySQL service is running
- Check network connectivity

**Performance Issues**:
- Review slow query logs
- Check index usage
- Analyze query execution plans

**Storage Issues**:
- Monitor table sizes
- Implement data archival
- Clean up old data

### Debug Queries

Enable query logging:

```python
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

## Migration Strategy

### Schema Changes

When modifying the schema:

1. Create migration script
2. Test on development database
3. Backup production database
4. Apply migration during maintenance window
5. Verify data integrity

### Migration Tools

Consider using Alembic for database migrations:

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Data Export/Import

### Export Data

```sql
-- Export specific table
SELECT * FROM users INTO OUTFILE '/tmp/users.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

### Import Data

```sql
-- Import data
LOAD DATA INFILE '/tmp/users.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

## Database Version

- **MySQL Version**: 8.0+
- **Character Set**: utf8mb4
- **Collation**: utf8mb4_unicode_ci
- **Engine**: InnoDB (all tables)

## Support

For database-related issues:
- Documentation: `/docs/database.md`
- Email: db-support@example.com
- GitHub Issues: https://github.com/yourusername/AI-Resume-Screener/issues
