# Railway Deployment Guide

## Overview

This guide explains how to deploy the AI Resume Screener backend to Railway using Docker.

## Prerequisites

- Railway account (free tier available)
- GitHub account with the project repository
- MySQL database service on Railway

## Step 1: Prepare GitHub Repository

1. **Push changes to GitHub**
   ```bash
   git add .
   git commit -m "Add Railway deployment configuration"
   git push origin main
   ```

2. **Ensure repository structure**
   ```
   AI-Resume-Screener/
   ├── Dockerfile              # Root Dockerfile for Railway
   ├── .dockerignore          # Docker ignore file
   ├── backend/
   │   ├── requirements.txt
   │   ├── app/
   │   └── nixpacks.toml      # Railway build configuration
   ├── frontend/
   └── docs/
   ```

## Step 2: Create Railway Project

1. **Go to [railway.app](https://railway.app)**
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Connect your GitHub account**
5. **Select the AI-Resume-Screener repository**

## Step 3: Add MySQL Service

1. **In your Railway project, click "New Service"**
2. **Select "Database"**
3. **Choose "MySQL"**
4. **Railway will create a MySQL instance**
5. **Note the connection details** (available in the "Variables" tab)

## Step 4: Configure Backend Service

1. **Add Backend Service**
   - Click "New Service"
   - Select "GitHub Repo"
   - Choose the same repository
   - **Root Directory**: `backend/`
   - **Dockerfile Path**: Leave empty (Railway will use root Dockerfile)
   - **Build Command**: Leave empty (Railway auto-detects)

2. **Configure Build Settings**
   - **Environment**: Select "Docker"
   - **Context**: `/` (root directory)
   - **Dockerfile**: `Dockerfile` (in root directory)

## Step 5: Set Environment Variables

Click on the backend service and go to the "Variables" tab. Add these variables:

### Required Variables

```bash
# Application Configuration
APP_ENV=production
DEBUG=False
LOG_LEVEL=INFO

# Database (Railway MySQL - get from MySQL service Variables tab)
DATABASE_URL=mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}

# JWT Configuration
SECRET_KEY=your-secure-random-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key

# CORS Configuration (use your Railway app URL)
CORS_ORIGINS=https://your-railway-app-url.railway.app

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
```

### Railway MySQL Variables

Railway automatically provides these variables. You'll see them in the MySQL service's "Variables" tab:

- `MYSQL_ROOT_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`

## Step 6: Docker Configuration

The root `Dockerfile` is configured for Railway:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Key points:
- Copies from `backend/` directory
- Uses Railway's PORT environment variable automatically
- Exposes port 8000
- Uses uvicorn to serve the FastAPI app

## Step 7: Health Check

Add a health check to Railway:

1. **Go to backend service settings**
2. **Add Health Check**
3. **Path**: `/`
4. **Interval**: 30 seconds
5. **Timeout**: 10 seconds
6. **Retries**: 3

## Step 8: Deploy

1. **Railway will automatically deploy on push**
2. **Or click "Deploy" button manually**
3. **Monitor deployment logs** in the "Deployments" tab
4. **Wait for deployment to complete**

## Step 9: Verify Deployment

1. **Get your Railway app URL** (from service page)
2. **Test root endpoint**:
   ```bash
   curl https://your-app-url.railway.app/
   ```
3. **Test API documentation**:
   ```
   https://your-app-url.railway.app/docs
   ```
4. **Test health**:
   ```bash
   curl https://your-app-url.railway.app/docs
   ```

## Step 10: Database Connection

The application will automatically connect to Railway MySQL using:

```python
DATABASE_URL=mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}
```

Railway replaces the `${...}` variables with actual values from the MySQL service.

## Troubleshooting

### Database Connection Issues

**Error**: `Access denied for user 'root'@'localhost'`

**Solution**: 
- Ensure you're using Railway's MySQL variables
- Check that DATABASE_URL uses Railway's host, not localhost
- Verify MYSQL_ROOT_PASSWORD is set correctly

### Port Issues

**Error**: Service won't start

**Solution**:
- Railway automatically sets PORT environment variable
- Ensure your app listens on 0.0.0.0
- Check the start command in nixpacks.toml

### Build Failures

**Error**: Build fails during deployment

**Solution**:
- Check deployment logs
- Verify Dockerfile paths are correct
- Ensure requirements.txt is in the right location
- Check for missing dependencies

### API Documentation Not Accessible

**Error**: `/docs` returns 404

**Solution**:
- Ensure docs_url="/docs" is set in FastAPI app
- Check that FastAPI is starting correctly
- Verify no middleware is blocking the endpoint

## Monitoring

### Railway Dashboard

- **Deployments Tab**: View deployment history and logs
- **Metrics Tab**: Monitor CPU, memory, and network usage
- **Logs Tab**: View application logs in real-time

### Application Logs

Logs are available in the Railway dashboard under the "Logs" tab. You can also:

```bash
# View logs via Railway CLI
railway logs
```

## Scaling

### Horizontal Scaling

1. **Go to service settings**
2. **Add instances**
3. **Railway will load balance across instances**

### Vertical Scaling

1. **Go to service settings**
2. **Change plan** (CPU/RAM allocation)

## Cost Optimization

### Free Tier Limits

- **MySQL**: Free tier available
- **Backend**: Free tier with limited resources
- **Total**: Approximately $5/month after free credits

### Optimization Tips

- Use appropriate instance sizes
- Enable caching (Redis)
- Optimize database queries
- Monitor resource usage

## Environment-Specific Configuration

### Development

- Use local MySQL
- Debug mode enabled
- Local file storage

### Production (Railway)

- Use Railway MySQL
- Debug mode disabled
- Consider cloud storage for files

## Security

### Best Practices

1. **Never commit secrets** to Git
2. **Use Railway's variables** for sensitive data
3. **Enable HTTPS** (Railway provides this automatically)
4. **Set strong passwords** for database
5. **Enable rate limiting** (already configured)
6. **Use environment-specific** CORS origins

### Railway Security

- **Automatic HTTPS** provided
- **Private network** for service-to-service communication
- **Secrets management** built-in
- **Access control** via Railway accounts

## Support

For Railway-specific issues:
- [Railway Documentation](https://docs.railway.app/)
- [Railway Support](https://railway.app/support)
- Email: Railway support team

## Updates and Maintenance

### Redeploying

1. **Push changes to GitHub**
2. **Railway auto-deploys** on push
3. **Or trigger manual deployment**

### Database Migrations

For schema changes:
1. **Create migration script**
2. **Run migration in Railway console**
3. **Or use Alembic for automated migrations**

## Backup and Recovery

### Database Backup

Railway provides automatic backups:
- **Daily backups** are automatic
- **Manual backups** can be created
- **Point-in-time recovery** available

### Backup Restoration

1. **Go to MySQL service**
2. **Click "Backups" tab**
3. **Select backup to restore**
4. **Click "Restore"**

## CI/CD Integration

### GitHub Actions

The project includes GitHub Actions that can be configured to:
- Run tests on push
- Build Docker images
- Deploy to Railway on merge to main

## Success Criteria

Your deployment is successful when:

- ✅ Railway deployment completes without errors
- ✅ Root endpoint returns 200 status
- ✅ `/docs` endpoint is accessible
- ✅ Database connection works
- ✅ API endpoints respond correctly
- ✅ Health checks pass

## Rollback

If deployment fails:

1. **Go to "Deployments" tab**
2. **Select previous successful deployment**
3. **Click "Redeploy"**
4. **Or revert GitHub commit**

## Next Steps

After successful deployment:

1. **Test all API endpoints**
2. **Monitor performance metrics**
3. **Set up error tracking** (Sentry, etc.)
4. **Configure custom domain** (optional)
5. **Set up monitoring alerts**
