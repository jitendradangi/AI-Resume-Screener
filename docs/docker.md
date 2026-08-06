# Docker Documentation

## Overview

The AI Resume Analyzer & Job Matching Platform supports Docker containerization for easy deployment and development. This document covers Docker setup, usage, and best practices.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space minimum

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AI-Resume-Screener.git
cd AI-Resume-Screener/backend
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your actual values
```

3. **Start the application**
```bash
docker compose up --build
```

4. **Access the application**
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- MySQL: localhost:3307

5. **Stop the application**
```bash
docker compose down
```

## Dockerfile

The Dockerfile is located in the `backend/` directory:

```dockerfile
# Use official Python image
FROM python:3.13-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Print logs immediately
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Create logs directory
RUN mkdir -p logs

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile Breakdown

- **Base Image**: Python 3.13 slim (lightweight)
- **Environment Variables**: Python optimization settings
- **Working Directory**: `/app` inside container
- **Dependencies**: Install from requirements.txt
- **Port**: Expose 8000 for FastAPI
- **Command**: Start uvicorn server

## Docker Compose

The docker-compose.yml file orchestrates the application services:

```yaml
version: "3.9"

services:
  mysql:
    image: mysql:8.0
    container_name: ai-resume-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: Jitu@2003
      MYSQL_DATABASE: ai_resume_screener
    ports:
      - "3307:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: .
    container_name: ai-resume-backend
    depends_on:
      - mysql
    ports:
      - "8000:8000"
    env_file:
      - .env.development
    environment:
      - DATABASE_URL=mysql+pymysql://root:Jitu%402003@mysql:3306/ai_resume_screener
    restart: always

volumes:
  mysql_data:
```

### Services

#### MySQL Service

- **Image**: mysql:8.0
- **Port**: 3307 (host) → 3306 (container)
- **Volume**: mysql_data for persistent storage
- **Health Check**: Ensures MySQL is ready before backend starts
- **Environment Variables**:
  - `MYSQL_ROOT_PASSWORD`: Root password
  - `MYSQL_DATABASE**: Database name

#### Backend Service

- **Build**: Builds from Dockerfile
- **Port**: 8000 (host) → 8000 (container)
- **Depends On**: MySQL service
- **Environment File**: .env.development
- **Environment Variables**: Override DATABASE_URL for Docker
- **Restart Policy**: Always restart on failure

## Docker Commands

### Building Images

```bash
# Build backend image
docker build -t ai-resume-backend .

# Build with tag
docker build -t ai-resume-backend:v1.0 .

# Build without cache
docker build --no-cache -t ai-resume-backend .
```

### Running Containers

```bash
# Start all services
docker compose up

# Start in detached mode
docker compose up -d

# Start specific service
docker compose up backend

# Start with build
docker compose up --build
```

### Stopping Containers

```bash
# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# Stop specific service
docker compose stop backend
```

### Viewing Logs

```bash
# View all logs
docker compose logs

# View logs for specific service
docker compose logs backend

# Follow logs in real-time
docker compose logs -f

# View last 100 lines
docker compose logs --tail=100
```

### Managing Containers

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Inspect container
docker inspect ai-resume-backend

# Execute command in container
docker exec -it ai-resume-backend bash

# Restart container
docker restart ai-resume-backend

# Remove container
docker rm ai-resume-backend
```

### Managing Images

```bash
# List images
docker images

# Remove image
docker rmi ai-resume-backend

# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a
```

### Managing Volumes

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect ai-resume-screener_mysql_data

# Remove volume
docker volume rm ai-resume-screener_mysql_data

# Remove unused volumes
docker volume prune
```

## Environment Configuration

### Docker Environment Files

The application uses different environment files for Docker:

- **.env.development**: For local Docker development
- **.env.testing**: For Docker testing
- **.env.production**: For Docker production

### Docker-Specific Variables

```bash
# Database URL for Docker (container hostname)
DATABASE_URL=mysql+pymysql://root:password@mysql:3306/ai_resume_screener

# For local development (localhost)
DATABASE_URL=mysql+pymysql://root:password@localhost:3307/ai_resume_screener
```

### Updating docker-compose.yml

To use different environment files:

```yaml
backend:
  env_file:
    - .env.production  # Change to desired environment
```

## Docker Health Checks

### MySQL Health Check

```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Backend Health Check (Optional)

Add to docker-compose.yml:

```yaml
backend:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/"]
    interval: 30s
    timeout: 10s
    retries: 3
```

## Docker Networking

### Default Network

Docker Compose creates a default network for services:

```bash
# View networks
docker network ls

# Inspect network
docker network inspect ai-resume-screener_default
```

### Custom Network

Define custom network in docker-compose.yml:

```yaml
networks:
  app-network:
    driver: bridge

services:
  backend:
    networks:
      - app-network
```

## Docker Volumes

### MySQL Data Volume

Persistent storage for MySQL data:

```yaml
volumes:
  mysql_data:
    driver: local
```

### Backup Volume

Add volume for backups:

```yaml
volumes:
  mysql_data:
  backups:
    driver: local

services:
  backend:
    volumes:
      - backups:/app/backups
```

## Docker Optimization

### Multi-Stage Build

Optimize image size with multi-stage build:

```dockerfile
# Build stage
FROM python:3.13-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Layer Caching

Optimize Dockerfile for layer caching:

```dockerfile
# Copy requirements first (changes less frequently)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code (changes more frequently)
COPY . .
```

### .dockerignore

Create `.dockerignore` to exclude unnecessary files:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
.venv
venv/
.env
.env.*
.git
.gitignore
README.md
logs/
*.log
tests/
.pytest_cache/
.coverage
htmlcov/
```

## Docker Debugging

### View Container Logs

```bash
# Real-time logs
docker compose logs -f backend

# Last 50 lines
docker compose logs --tail=50 backend
```

### Execute Commands in Container

```bash
# Open shell
docker exec -it ai-resume-backend bash

# Run Python
docker exec -it ai-resume-backend python

# Run tests
docker exec -it ai-resume-backend pytest tests/
```

### Inspect Container

```bash
# View container details
docker inspect ai-resume-backend

# View container processes
docker top ai-resume-backend

# View container stats
docker stats ai-resume-backend
```

## Docker Production Deployment

### Production Dockerfile

Optimized for production:

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install only production dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Use production server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Production docker-compose.yml

```yaml
version: "3.9"

services:
  mysql:
    image: mysql:8.0
    container_name: ai-resume-mysql-prod
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./backups:/backups
    networks:
      - app-network

  backend:
    build: .
    container_name: ai-resume-backend-prod
    restart: always
    depends_on:
      - mysql
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    environment:
      - DATABASE_URL=mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@mysql:3306/${MYSQL_DATABASE}
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  app-network:
    driver: bridge

volumes:
  mysql_data:
```

## Docker Security

### Security Best Practices

1. **Use Non-Root User**: Run containers as non-root user
2. **Scan Images**: Use Docker Scout or Trivy for vulnerability scanning
3. **Minimal Base Image**: Use slim/alpine images
4. **Secrets Management**: Use Docker secrets or environment variables
5. **Network Isolation**: Use custom networks
6. **Resource Limits**: Set container resource limits

### Resource Limits

Add to docker-compose.yml:

```yaml
backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Image Scanning

```bash
# Scan with Docker Scout
docker scout quickview ai-resume-backend

# Scan with Trivy
trivy image ai-resume-backend
```

## Docker Troubleshooting

### Common Issues

**Container Won't Start**:
```bash
# Check logs
docker compose logs backend

# Check if port is in use
netstat -tulpn | grep 8000

# Try different port
docker compose up -p 8001:8000
```

**Database Connection Issues**:
```bash
# Check MySQL container
docker compose logs mysql

# Test MySQL connection
docker exec -it ai-resume-mysql mysql -u root -p

# Check network
docker network inspect ai-resume-screener_default
```

**Build Failures**:
```bash
# Clean build
docker compose down
docker system prune -a
docker compose up --build
```

### Docker System Cleanup

```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune -a

# Remove all unused volumes
docker volume prune

# Remove all unused networks
docker network prune

# Complete cleanup
docker system prune -a --volumes
```

## Docker Monitoring

### Container Monitoring

```bash
# View container stats
docker stats

# View specific container stats
docker stats ai-resume-backend
```

### Log Monitoring

```bash
# Follow logs
docker compose logs -f

# View logs with timestamps
docker compose logs -t

# Export logs
docker compose logs > app.log
```

## Docker Backup and Restore

### Backup Containers

```bash
# Backup MySQL data
docker exec ai-resume-mysql mysqldump -u root -p ai_resume_screener > backup.sql

# Backup volume
docker run --rm -v ai-resume-screener_mysql_data:/data -v $(pwd):/backup alpine tar czf /backup/mysql-backup.tar.gz /data
```

### Restore Containers

```bash
# Restore MySQL data
docker exec -i ai-resume-mysql mysql -u root -p ai_resume_screener < backup.sql

# Restore volume
docker run --rm -v ai-resume-screener_mysql_data:/data -v $(pwd):/backup alpine tar xzf /backup/mysql-backup.tar.gz -C /
```

## Docker CI/CD Integration

### GitHub Actions

The project includes GitHub Actions workflow for Docker:

```yaml
# .github/workflows/backend-ci.yml
- name: Build Docker Image
  working-directory: ./backend
  run: |
    docker build -t ai-resume-screener-backend:latest .
```

### Automated Building

Configure GitHub Actions to build and push images:

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}

- name: Push to Docker Hub
  run: |
    docker push ai-resume-screener-backend:latest
```

## Docker Compose Profiles

Use profiles for different environments:

```yaml
services:
  backend:
    profiles:
      - development
      - production

  backend-dev:
    extends: backend
    profiles:
      - development

  backend-prod:
    extends: backend
    profiles:
      - production
```

Run with specific profile:

```bash
docker compose --profile development up
docker compose --profile production up
```

## Docker Performance Tuning

### MySQL Performance

Add MySQL configuration to docker-compose.yml:

```yaml
mysql:
    command: --default-authentication-plugin=mysql_native_password --innodb-buffer-pool-size=1G
```

### Backend Performance

Add worker configuration:

```yaml
backend:
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Docker Advanced Topics

### Docker Swarm

Deploy with Docker Swarm:

```bash
docker swarm init
docker stack deploy -c docker-compose.yml ai-resume
```

### Kubernetes

Convert to Kubernetes deployment:

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-resume-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-resume-backend
  template:
    metadata:
      labels:
        app: ai-resume-backend
    spec:
      containers:
      - name: backend
        image: ai-resume-backend:latest
        ports:
        - containerPort: 8000
```

## Docker Best Practices

1. **Use Specific Image Tags**: Avoid `latest` tag
2. **Minimize Layers**: Combine RUN commands
3. **Cache Dependencies**: Copy requirements.txt first
4. **Use .dockerignore**: Exclude unnecessary files
5. **Scan for Vulnerabilities**: Regular security scanning
6. **Monitor Resources**: Set resource limits
7. **Log Rotation**: Prevent disk space issues
8. **Health Checks**: Implement health checks
9. **Non-Root User**: Run as non-root user
10. **Secrets Management**: Never commit secrets

## Docker Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)

## Support

For Docker-related issues:
- Documentation: `/docs/docker.md`
- Email: docker-support@example.com
- GitHub Issues: https://github.com/yourusername/AI-Resume-Screener/issues
