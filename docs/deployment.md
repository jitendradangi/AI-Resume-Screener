# Deployment Documentation

## Overview

This document covers deployment strategies for the AI Resume Analyzer & Job Matching Platform, including Railway deployment, environment configuration, and production setup.

## Deployment Options

### 1. Railway (Recommended)

Railway is a cloud platform that simplifies deployment with built-in database, file storage, and CI/CD.

### 2. Traditional VPS

Deploy to traditional VPS providers (DigitalOcean, AWS EC2, etc.)

### 3. Kubernetes

Deploy to Kubernetes clusters for enterprise-scale deployments

### 4. Docker

Deploy using Docker containers on any platform

## Railway Deployment

### Prerequisites

- Railway account (free tier available)
- GitHub account
- Railway CLI (optional)

### Step 1: Prepare Repository

1. **Fork the repository** to your GitHub account
2. **Update environment variables** in Railway dashboard
3. **Configure Railway** to connect to your repository

### Step 2: Railway Project Setup

1. **Create new Railway project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"

2. **Connect repository**
   - Select your forked repository
   - Choose the branch to deploy (main/develop)

3. **Configure services**

### Step 3: Database Service

1. **Add MySQL service**
   - Click "New Service"
   - Select "Database"
   - Choose "MySQL"
   - Railway will provide connection details

2. **Get database URL**
   - Click on MySQL service
   - Copy the DATABASE_URL from the "Variables" tab
   - Format: `mysql://user:password@host:port/database`

### Step 4: Backend Service

1. **Add backend service**
   - Click "New Service"
   - Select "GitHub Repo"
   - Select the same repository
   - Choose the `backend/` directory as root

2. **Configure build settings**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Add environment variables**
   - Click on backend service
   - Go to "Variables" tab
   - Add the following variables:

```bash
# App Configuration
APP_ENV=production
DEBUG=False
LOG_LEVEL=INFO

# Database (from Railway MySQL service)
DATABASE_URL=${{MYSQL.DATABASE_URL}}

# JWT Configuration
SECRET_KEY=your-secure-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key

# CORS Configuration
CORS_ORIGINS=https://your-frontend-domain.com,https://your-frontend-domain.com

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
```

### Step 5: File Storage (Optional)

Railway provides temporary file storage. For production, consider:

1. **Railway Volume** (for smaller deployments)
2. **AWS S3** (recommended for production)
3. **Google Cloud Storage** (alternative to S3)

### Step 6: Deploy

1. **Trigger deployment**
   - Railway will automatically deploy on push
   - Or click "Deploy" button manually

2. **Monitor deployment**
   - View logs in Railway dashboard
   - Check build status
   - Verify service health

3. **Get deployment URL**
   - Railway provides a public URL
   - Configure custom domain (optional)

### Step 7: Verify Deployment

1. **Check API health**
   ```bash
   curl https://your-app.railway.app/
   ```

2. **Access API documentation**
   - Swagger UI: `https://your-app.railway.app/docs`
   - ReDoc: `https://your-app.railway.app/redoc`

3. **Test authentication**
   ```bash
   curl -X POST https://your-app.railway.app/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'
   ```

## Traditional VPS Deployment

### Prerequisites

- VPS with Ubuntu 20.04+ or similar
- Domain name (optional)
- SSL certificate (recommended)

### Step 1: Server Setup

1. **Update system**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install dependencies**
```bash
sudo apt install -y python3 python3-pip python3-venv mysql-server nginx
```

3. **Install Docker** (optional, for containerized deployment)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Step 2: Application Setup

1. **Clone repository**
```bash
git clone https://github.com/yourusername/AI-Resume-Screener.git
cd AI-Resume-Screener/backend
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.production .env
nano .env
```

### Step 3: Database Setup

1. **Secure MySQL**
```bash
sudo mysql_secure_installation
```

2. **Create database**
```sql
CREATE DATABASE ai_resume_screener;
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON ai_resume_screener.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;
```

3. **Update .env file**
```bash
DATABASE_URL=mysql+pymysql://appuser:secure_password@localhost:3306/ai_resume_screener
```

### Step 4: Application Service

1. **Create systemd service**
```bash
sudo nano /etc/systemd/system/ai-resume.service
```

2. **Service configuration**
```ini
[Unit]
Description=AI Resume Screener API
After=network.target mysql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/AI-Resume-Screener/backend
Environment="PATH=/var/www/AI-Resume-Screener/backend/.venv/bin"
ExecStart=/var/www/AI-Resume-Screener/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

3. **Enable and start service**
```bash
sudo systemctl enable ai-resume
sudo systemctl start ai-resume
sudo systemctl status ai-resume
```

### Step 5: Nginx Configuration

1. **Create Nginx config**
```bash
sudo nano /etc/nginx/sites-available/ai-resume
```

2. **Nginx configuration**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. **Enable site**
```bash
sudo ln -s /etc/nginx/sites-available/ai-resume /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: SSL Configuration (Recommended)

1. **Install Certbot**
```bash
sudo apt install certbot python3-certbot-nginx
```

2. **Obtain SSL certificate**
```bash
sudo certbot --nginx -d your-domain.com
```

3. **Auto-renewal**
```bash
sudo certbot renew --dry-run
```

## Docker Deployment

### Step 1: Prepare Environment

1. **Clone repository**
```bash
git clone https://github.com/yourusername/AI-Resume-Screener.git
cd AI-Resume-Screener/backend
```

2. **Configure environment**
```bash
cp .env.production .env
nano .env
```

### Step 2: Docker Compose Production

1. **Use production compose file**
```bash
docker compose -f docker-compose.prod.yml up -d
```

2. **Production compose file** (docker-compose.prod.yml)
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

### Step 3: Reverse Proxy

Configure Nginx or Traefik as reverse proxy for Docker containers.

## Environment Variables

### Required Variables

```bash
# Application
APP_ENV=production
DEBUG=False
LOG_LEVEL=INFO

# Database
DATABASE_URL=mysql+pymysql://user:password@host:3306/database

# Authentication
SECRET_KEY=your-secure-random-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services
GROQ_API_KEY=your-groq-api-key

# CORS
CORS_ORIGINS=https://your-frontend-domain.com

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
```

### Security Guidelines

1. **SECRET_KEY**: Use a secure random string (32+ characters)
2. **Database Password**: Use strong, unique passwords
3. **API Keys**: Never commit API keys to repository
4. **CORS**: Only allow trusted domains
5. **Rate Limiting**: Enable to prevent abuse

### Generating Secure Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate database password
openssl rand -base64 32
```

## Production Checklist

### Security

- [ ] Change default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor for vulnerabilities

### Performance

- [ ] Enable caching (Redis)
- [ ] Configure database connection pooling
- [ ] Use production web server (Gunicorn)
- [ ] Enable gzip compression
- [ ] Optimize database queries
- [ ] Monitor resource usage
- [ ] Set up CDN for static files

### Monitoring

- [ ] Set up application logging
- [ ] Configure error tracking (Sentry)
- [ ] Monitor uptime (UptimeRobot)
- [ ] Set up alerts (PagerDuty)
- [ ] Monitor database performance
- [ ] Track API response times
- [ ] Monitor disk space

### Backup

- [ ] Database backup strategy
- [ ] File backup strategy
- [ ] Automated backup schedule
- [ ] Backup retention policy
- [ ] Disaster recovery plan
- [ ] Test backup restoration

### CI/CD

- [ ] Automated testing
- [ ] Automated deployment
- [ ] Rollback strategy
- [ ] Staging environment
- [ ] Blue-green deployment
- [ ] Feature flags

## Monitoring and Logging

### Application Monitoring

1. **Health Check Endpoint**
```bash
curl https://your-domain.com/
```

2. **Log Monitoring**
```bash
# View application logs
tail -f /var/www/AI-Resume-Screener/backend/logs/app.log

# View error logs
tail -f /var/www/AI-Resume-Screener/backend/logs/error.log
```

3. **System Monitoring**
```bash
# CPU and memory
htop

# Disk usage
df -h

# Network connections
netstat -tulpn
```

### Error Tracking

Consider using error tracking services:

- **Sentry**: Error tracking and performance monitoring
- **Rollbar**: Error monitoring and alerting
- **Bugsnag**: Error monitoring for production apps

### Uptime Monitoring

Set up uptime monitoring:

- **UptimeRobot**: Free uptime monitoring
- **Pingdom**: Website monitoring
- **StatusCake**: Website and API monitoring

## Scaling

### Horizontal Scaling

1. **Load Balancer**
   - Use Nginx or HAProxy
   - Distribute traffic across multiple instances

2. **Multiple Instances**
   - Deploy multiple backend instances
   - Use shared database storage
   - Use shared file storage (S3)

### Vertical Scaling

1. **Increase Resources**
   - More CPU cores
   - More RAM
   - Faster storage (SSD)

2. **Database Optimization**
   - Increase connection pool size
   - Add read replicas
   - Use database caching

## Troubleshooting

### Common Issues

**Application won't start**:
```bash
# Check logs
sudo journalctl -u ai-resume -f

# Check service status
sudo systemctl status ai-resume

# Restart service
sudo systemctl restart ai-resume
```

**Database connection issues**:
```bash
# Check MySQL status
sudo systemctl status mysql

# Test connection
mysql -u appuser -p -h localhost ai_resume_screener

# Check logs
tail -f /var/log/mysql/error.log
```

**Nginx issues**:
```bash
# Test Nginx config
sudo nginx -t

# Check Nginx status
sudo systemctl status nginx

# View Nginx logs
tail -f /var/log/nginx/error.log
```

**Performance issues**:
```bash
# Check resource usage
htop

# Check database performance
mysql -u appuser -p -e "SHOW PROCESSLIST;"

# Check slow queries
mysql -u appuser -p -e "SHOW VARIABLES LIKE 'slow_query_log';"
```

## Maintenance

### Regular Tasks

**Daily**:
- Monitor application logs
- Check error rates
- Verify backup completion

**Weekly**:
- Review system performance
- Check disk space
- Review security updates

**Monthly**:
- Update dependencies
- Review and optimize database
- Test backup restoration
- Security audit

### Updates

**Application Updates**:
```bash
cd /var/www/AI-Resume-Screener
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart ai-resume
```

**System Updates**:
```bash
sudo apt update
sudo apt upgrade -y
sudo reboot
```

## Cost Optimization

### Railway Cost

- **Free Tier**: $5/month credit
- **MySQL**: ~$10/month
- **Backend**: ~$5/month
- **Total**: ~$15/month (small deployment)

### VPS Cost

- **DigitalOcean**: $5-40/month
- **AWS EC2**: $10-100/month
- **Google Cloud**: $6-50/month

### Optimization Tips

1. **Use appropriate instance sizes**
2. **Enable auto-scaling**
3. **Use reserved instances for long-term**
4. **Monitor and optimize resource usage
5. **Use CDN for static content**
6. **Compress and optimize assets**

## Support

For deployment issues:
- Documentation: `/docs/deployment.md`
- Email: deploy-support@example.com
- GitHub Issues: https://github.com/yourusername/AI-Resume-Screener/issues
