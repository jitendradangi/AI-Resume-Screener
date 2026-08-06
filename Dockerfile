# Railway-specific Dockerfile for backend deployment
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
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend project files
COPY backend/ .

# Expose FastAPI port (Railway uses PORT environment variable)
EXPOSE 8000

# Start FastAPI (Railway sets PORT environment variable)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
