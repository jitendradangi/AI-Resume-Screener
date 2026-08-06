# Contributing to AI Resume Analyzer & Job Matching Platform

Thank you for your interest in contributing to our project! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Description**: A clear and concise description of the bug
- **Steps to Reproduce**: Steps to reproduce the behavior
- **Expected Behavior**: What you expected to happen
- **Screenshots**: If applicable, add screenshots
- **Environment**: 
  - OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
  - Python version: [e.g., 3.13]
  - Browser (if applicable): [e.g., Chrome 120]

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Description**: A clear and concise description of the enhancement
- **Motivation**: Why this enhancement would be useful
- **Alternatives**: Any alternative solutions or features you've considered

## 🛠 Development Setup

1. **Fork the repository**
```bash
# Fork the repository on GitHub
git clone https://github.com/yourusername/AI-Resume-Screener.git
cd AI-Resume-Screener
```

2. **Create a virtual environment**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

5. **Make your changes**
- Write clean, readable code
- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed

6. **Test your changes**
```bash
# Run tests
pytest tests/

# Run linting
flake8 app/
```

7. **Commit your changes**
```bash
git add .
git commit -m "feat: add your feature description"
```

8. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

9. **Create a Pull Request**
- Go to the original repository
- Click "New Pull Request"
- Select your feature branch
- Fill in the PR template
- Submit the PR

## 📝 Coding Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Commit Messages

Follow the Conventional Commits specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```bash
feat: add semantic matching algorithm
fix: resolve database connection timeout
docs: update API documentation
test: add unit tests for resume parser
```

### Code Review Process

- All contributions must be reviewed before merging
- Address review comments promptly
- Be respectful and constructive in reviews
- Request review from at least one maintainer

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_file.py

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Writing Tests

- Write unit tests for new features
- Test edge cases and error conditions
- Keep tests independent and fast
- Use descriptive test names

## 📚 Documentation

- Update README.md for user-facing changes
- Update code comments for complex logic
- Add docstrings to new functions
- Update API documentation for endpoint changes

## 🎯 Project Structure Guidelines

- **Models**: Define data models in `app/models/`
- **Schemas**: Define Pydantic schemas in `app/schemas/`
- **Repositories**: Database operations in `app/repositories/`
- **Services**: Business logic in `app/services/`
- **Routers**: API endpoints in `app/routers/`
- **Core**: Shared utilities in `app/core/`

## 🔒 Security

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Follow security best practices
- Report security vulnerabilities privately

## 📞 Getting Help

If you need help:

- Check existing issues and discussions
- Read the documentation
- Ask questions in GitHub Discussions
- Contact maintainers directly for urgent issues

## 🎉 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing! 🙏
