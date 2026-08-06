# Testing Documentation

## Overview

The AI Resume Analyzer & Job Matching Platform uses pytest for testing. This document covers testing strategies, test structure, coverage requirements, and best practices.

## Testing Philosophy

- **Unit Tests**: Test individual functions and methods in isolation
- **Integration Tests**: Test interactions between components
- **End-to-End Tests**: Test complete user workflows
- **Fast Tests**: Tests should run quickly (< 1 second per test)
- **Independent Tests**: Each test should be independent of others
- **Clear Intent**: Test names should clearly describe what they test

## Test Structure

### Directory Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration and fixtures
│   ├── test_auth.py                # Authentication tests
│   ├── test_resume.py              # Resume tests
│   ├── test_jobs.py                # Job tests
│   ├── test_ats.py                 # ATS analysis tests
│   ├── test_job_match.py           # Job matching tests
│   ├── test_repositories.py        # Repository tests
│   ├── test_services.py            # Service tests
│   ├── test_matchers.py            # Matcher tests
│   └── test_api.py                 # API endpoint tests
```

### Test File Organization

Each test file should correspond to a module or feature:

- `test_auth.py` → `app/routers/auth.py`
- `test_resume.py` → `app/routers/resume.py`
- `test_matchers.py` → `app/matching/`

## Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-cov pytest-asyncio httpx
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run with coverage and show missing lines
pytest --cov=app --cov-report=term-missing
```

### Run Specific Tests

```bash
# Run specific test file
pytest tests/test_auth.py

# Run specific test function
pytest tests/test_auth.py::test_register_user

# Run tests matching pattern
pytest -k "test_register"

# Run tests in specific directory
pytest tests/test_matchers/
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only slow tests
pytest -m slow

# Skip slow tests
pytest -m "not slow"
```

## Test Configuration

### pytest.ini

Create `pytest.ini` in the backend directory:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --cov=app
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    api: API endpoint tests
```

### conftest.py

Configure pytest fixtures in `tests/conftest.py`:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.base import Base
from app.database.db import get_db

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    """Create a test client."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return headers."""
    # Register user
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "test123"
    })
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}
```

## Test Examples

### Unit Tests

```python
# tests/test_matchers.py
import pytest
from app.matching.skill_matcher import SkillMatcher

@pytest.mark.unit
def test_skill_matcher_basic():
    """Test basic skill matching."""
    job_skills = ["Python", "FastAPI", "MySQL"]
    resume_skills = ["Python", "FastAPI", "JavaScript"]
    
    result = SkillMatcher.match_skills(job_skills, resume_skills)
    
    assert result["matched_skills"] == ["Python", "FastAPI"]
    assert result["missing_skills"] == ["MySQL"]
    assert result["match_score"] > 0

@pytest.mark.unit
def test_skill_matcher_empty():
    """Test skill matching with empty lists."""
    result = SkillMatcher.match_skills([], [])
    
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["match_score"] == 0
```

### Integration Tests

```python
# tests/test_repositories.py
import pytest
from app.repositories.user import user_repository

@pytest.mark.integration
def test_create_user(db):
    """Test user creation in database."""
    user_data = {
        "email": "test@example.com",
        "password_hash": "hashed_password",
        "full_name": "Test User",
        "role": "USER"
    }
    
    user = user_repository.create(db, user_data)
    
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.role == "USER"

@pytest.mark.integration
def test_get_user_by_email(db):
    """Test retrieving user by email."""
    # Create user first
    user_data = {
        "email": "test@example.com",
        "password_hash": "hashed_password",
        "full_name": "Test User",
        "role": "USER"
    }
    user_repository.create(db, user_data)
    
    # Retrieve user
    user = user_repository.get_by_email(db, "test@example.com")
    
    assert user is not None
    assert user.email == "test@example.com"
```

### API Tests

```python
# tests/test_api.py
import pytest

@pytest.mark.api
def test_register_user(client):
    """Test user registration API."""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "public_id" in data

@pytest.mark.api
def test_login_user(client):
    """Test user login API."""
    # Register first
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "test123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.api
def test_protected_endpoint(client, auth_headers):
    """Test protected endpoint with authentication."""
    response = client.get("/profile", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

@pytest.mark.api
def test_protected_endpoint_without_auth(client):
    """Test protected endpoint without authentication."""
    response = client.get("/profile")
    
    assert response.status_code == 401
```

## Test Coverage

### Coverage Requirements

- **Overall Coverage**: Target 80%+
- **Critical Modules**: 90%+ coverage
- **New Features**: 100% coverage before merge

### Generate Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Generate terminal coverage report
pytest --cov=app --cov-report=term-missing

# Generate XML coverage report (for CI/CD)
pytest --cov=app --cov-report=xml
```

### View Coverage Report

```bash
# Open HTML report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Exclusions

Exclude certain files from coverage:

```python
# .coveragerc
[run]
omit =
    */tests/*
    */__init__.py
    */migrations/*
    */venv/*
```

## Test Markers

### Available Markers

- `@pytest.mark.unit`: Unit tests (fast, isolated)
- `@pytest.mark.integration`: Integration tests (slower, database)
- `@pytest.mark.slow`: Slow tests (network, external APIs)
- `@pytest.mark.api`: API endpoint tests

### Custom Markers

Define custom markers in `pytest.ini`:

```ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    api: API endpoint tests
    auth: Authentication tests
    resume: Resume tests
    jobs: Job tests
```

## Test Fixtures

### Common Fixtures

```python
# conftest.py
@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User"
    }

@pytest.fixture
def sample_job_data():
    """Sample job data for testing."""
    return {
        "title": "Software Engineer",
        "description": "Job description",
        "requirements": "Python, FastAPI",
        "location": "Remote",
        "salary_range": "$80,000 - $120,000",
        "company": "Tech Company"
    }

@pytest.fixture
def sample_resume_data():
    """Sample resume data for testing."""
    return {
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
```

## Async Testing

### Async Test Support

For testing async functions:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await some_async_function()
    assert result is not None
```

### Async API Tests

```python
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    """Test async API endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
```

## Mocking and Patching

### Mock External Services

```python
from unittest.mock import patch, MagicMock

@pytest.mark.unit
@patch('app.ai.resume_analyzer.genai.GenerativeModel')
def test_resume_analyzer_with_mock(mock_model):
    """Test resume analyzer with mocked Gemini API."""
    # Configure mock
    mock_response = MagicMock()
    mock_response.text = '{"overall_score": 85}'
    mock_model.return_value.generate_content.return_value = mock_response
    
    # Test function
    result = ResumeAnalyzer.analyze_resume("resume text", {})
    
    assert result["overall_score"] == 85
    mock_model.assert_called_once()
```

### Mock Database

```python
from unittest.mock import Mock

@pytest.mark.unit
def test_repository_with_mock_db():
    """Test repository with mocked database."""
    mock_db = Mock()
    mock_user = Mock()
    mock_user.email = "test@example.com"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    user = user_repository.get_by_email(mock_db, "test@example.com")
    
    assert user.email == "test@example.com"
```

## CI/CD Integration

### GitHub Actions

Configure GitHub Actions to run tests:

```yaml
# .github/workflows/backend-ci.yml
- name: Run Tests
  working-directory: ./backend
  run: |
    pytest tests/ -v --cov=app --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./backend/coverage.xml
```

### Pre-commit Hooks

Run tests before committing:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

## Best Practices

### Test Organization

1. **One Test per Function**: Each test should test one thing
2. **Descriptive Names**: Test names should describe what they test
3. **AAA Pattern**: Arrange, Act, Assert
4. **Independent Tests**: Tests should not depend on each other
5. **Fast Tests**: Keep tests fast and focused

### Test Data

1. **Use Fixtures**: Create reusable test data fixtures
2. **Factory Pattern**: Use factories for complex objects
3. **Cleanup**: Clean up test data after tests
4. **Isolation**: Use test database, not production

### Test Coverage

1. **Aim for High Coverage**: Target 80%+ coverage
2. **Focus on Critical Paths**: Prioritize important code
3. **Don't Chase 100%**: Some code is hard to test
4. **Review Coverage Reports**: Regularly review coverage

### Error Testing

1. **Test Error Cases**: Test how code handles errors
2. **Edge Cases**: Test boundary conditions
3. **Invalid Input**: Test with invalid data
4. **Network Failures**: Test network error handling

## Troubleshooting

### Common Issues

**Tests Fail in CI but Pass Locally**:
- Check environment variables
- Verify database configuration
- Check for timing issues
- Review CI logs

**Tests are Slow**:
- Use mocks for external services
- Optimize database queries
- Use fixtures for setup
- Run tests in parallel

**Flaky Tests**:
- Add retries for network tests
- Use deterministic test data
- Avoid time-dependent tests
- Isolate test dependencies

### Debugging Tests

```bash
# Run with debugger
pytest --pdb

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Verbose output
pytest -vv
```

## Continuous Testing

### Watch Mode

Run tests automatically when files change:

```bash
pip install pytest-xdist
pytest-watch
```

### Parallel Testing

Run tests in parallel:

```bash
pip install pytest-xdist
pytest -n auto
```

## Performance Testing

### Load Testing

Use tools like Locust for load testing:

```python
# locustfile.py
from locust import HttpUser, task

class ResumeUser(HttpUser):
    @task
    def upload_resume(self):
        self.client.post("/resume/upload", files={"file": open("resume.pdf", "rb")})
```

## Test Documentation

### Docstrings

Add docstrings to test functions:

```python
def test_user_registration():
    """
    Test user registration with valid data.
    
    Should create user and return 201 status.
    """
    pass
```

### Test Documentation

Document test requirements and expected behavior:

```python
"""
Test Module: Authentication

Requirements:
- Users can register with email and password
- Users can login with valid credentials
- Invalid credentials should return 401
"""
```

## Test Metrics

### Key Metrics to Track

- **Test Count**: Number of tests
- **Coverage Percentage**: Code coverage
- **Test Duration**: How long tests take
- **Flaky Test Rate**: Percentage of flaky tests
- **Pass Rate**: Percentage of passing tests

### Improving Metrics

- **Add More Tests**: Increase test count
- **Improve Coverage**: Add tests for uncovered code
- **Optimize Tests**: Make tests faster
- **Fix Flaky Tests**: Improve test reliability
- **Review Failures**: Understand why tests fail

## Resources

### Documentation

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

### Tools

- **Pytest**: Testing framework
- **Coverage.py**: Code coverage
- **Pytest-xdist**: Parallel testing
- **Pytest-cov**: Coverage plugin
- **Locust**: Load testing
- **Mock**: Mocking library

## Support

For testing-related issues:
- Documentation: `/docs/testing.md`
- Email: test-support@example.com
- GitHub Issues: https://github.com/yourusername/AI-Resume-Screener/issues
