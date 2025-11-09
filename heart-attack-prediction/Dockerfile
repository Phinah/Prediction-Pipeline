# Dockerfile for Heart Attack Prediction API
# This allows the FastAPI application to be deployed to cloud platforms
# (Render, Railway, Google Cloud Run, AWS ECS, etc.)

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY mongodb/ ./mongodb/
COPY heart_project/ ./heart_project/

# Expose port (Render and most platforms use PORT env var)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

# Run the application
# Use environment variable PORT if available (required by Render), default to 8000
CMD uvicorn mongodb.main:app --host 0.0.0.0 --port ${PORT:-8000}
