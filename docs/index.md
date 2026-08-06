# Documentation Index

Welcome to the AI Resume Analyzer & Job Matching Platform documentation. This index provides an overview of all available documentation.

## Documentation Files

### Main Documentation

- **[README.md](../README.md)**: Project overview, features, installation, and quick start guide
- **[CONTRIBUTING.md](../CONTRIBUTING.md)**: Contribution guidelines and development setup
- **[LICENSE](../LICENSE)**: MIT License for the project
- **[CHANGELOG.md](../CHANGELOG.md)**: Version history and changelog

### Technical Documentation

- **[architecture.md](architecture.md)**: System architecture, request flows, and module interactions
- **[api.md](api.md)**: Complete API documentation with endpoints and examples
- **[database.md](database.md)**: Database schema, ER diagrams, and data management
- **[docker.md](docker.md)**: Docker setup, commands, and best practices
- **[deployment.md](deployment.md)**: Deployment strategies and production setup
- **[testing.md](testing.md)**: Testing guidelines, coverage, and best practices

### Backend Documentation

- **[PRODUCTION_CONFIG.md](../backend/PRODUCTION_CONFIG.md)**: Production configuration guide

## Quick Links

### For Developers

- [Getting Started](../README.md#installation-guide)
- [Development Setup](../CONTRIBUTING.md#development-setup)
- [API Documentation](api.md)
- [Testing Guide](testing.md)
- [Architecture Overview](architecture.md)

### For DevOps Engineers

- [Docker Guide](docker.md)
- [Deployment Guide](deployment.md)
- [Production Configuration](../backend/PRODUCTION_CONFIG.md)
- [Database Management](database.md)

### For New Contributors

- [Contribution Guidelines](../CONTRIBUTING.md)
- [Code Standards](../CONTRIBUTING.md#coding-standards)
- [Testing Requirements](testing.md)
- [Project Structure](../README.md#project-structure)

## Documentation by Topic

### Architecture & Design

- [System Architecture](architecture.md)
- [Database Schema](database.md)
- [API Design](api.md)
- [Module Interactions](architecture.md#module-interactions)

### Development

- [Installation Guide](../README.md#installation-guide)
- [Development Setup](../CONTRIBUTING.md#development-setup)
- [Testing](testing.md)
- [API Development](api.md)

### Deployment

- [Docker Deployment](docker.md)
- [Railway Deployment](deployment.md#railway-deployment)
- [VPS Deployment](deployment.md#traditional-vps-deployment)
- [Production Setup](deployment.md#production-checklist)

### Operations

- [Database Management](database.md)
- [Monitoring](deployment.md#monitoring-and-logging)
- [Backup & Recovery](database.md#backup-and-recovery)
- [Troubleshooting](deployment.md#troubleshooting)

## Documentation Standards

### Format

- All documentation uses Markdown format
- Code blocks include syntax highlighting
- Tables and diagrams for complex information
- Consistent structure across all files

### Maintenance

- Documentation is updated with each release
- API documentation reflects current endpoints
- Architecture docs match current implementation
- Examples are tested and verified

### Contributions

- Documentation contributions are welcome
- Follow the [Contributing Guidelines](../CONTRIBUTING.md)
- Update relevant docs when making changes
- Keep examples current and accurate

## Getting Help

### Documentation Issues

If you find issues in the documentation:
1. Check for updates in the latest version
2. Search [GitHub Issues](https://github.com/yourusername/AI-Resume-Screener/issues)
3. Create a new issue with clear description
4. Suggest improvements via pull requests

### Technical Support

For technical support:
- **Email**: support@example.com
- **GitHub Issues**: https://github.com/yourusername/AI-Resume-Screener/issues
- **Discussions**: https://github.com/yourusername/AI-Resume-Screener/discussions

## Documentation Roadmap

### Planned Additions

- [ ] Frontend documentation (when developed)
- [ ] API versioning guide
- [ ] Performance tuning guide
- [ ] Security best practices
- [ ] Migration guides
- [ ] Video tutorials
- [ ] Interactive API playground

### Improvements

- [ ] More code examples
- [ ] Architecture diagrams
- [ ] Troubleshooting guides
- [ ] Performance benchmarks
- [ ] Case studies

## Quick Reference

### Common Commands

**Local Development**:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Docker**:
```bash
cd backend
docker compose up --build
```

**Testing**:
```bash
cd backend
pytest tests/ --cov=app
```

**Database**:
```bash
mysql -u root -p ai_resume_screener
```

### Key Files

- **Main App**: `backend/app/main.py`
- **Config**: `backend/app/core/config.py`
- **Database**: `backend/app/database/db.py`
- **Requirements**: `backend/requirements.txt`
- **Docker**: `backend/Dockerfile`
- **Docker Compose**: `backend/docker-compose.yml`

### Environment Variables

Required environment variables are documented in:
- [Environment Variables](../README.md#environment-variables)
- [Production Configuration](../backend/PRODUCTION_CONFIG.md)

## Documentation License

Documentation is licensed under the same MIT License as the project.

## Documentation Team

Documentation is maintained by the project team. Contributions are welcome from the community.

---

**Last Updated**: 2026-08-06  
**Documentation Version**: 1.0.0  
**Project Version**: 1.0.0
