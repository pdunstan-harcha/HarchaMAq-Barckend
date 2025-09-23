# Backend Dockerfile (multi-stage) for Flask API
# Stage 1: Base image with system deps
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system packages (add build tools only if needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Leverage Docker layer caching: copy requirements first
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose API port
EXPOSE 5000

# Default command is production-ready (Gunicorn)
# For development, override in docker-compose to `python run.py`
CMD ["gunicorn", "-c", "gunicorn.conf.py", "run:app"]
