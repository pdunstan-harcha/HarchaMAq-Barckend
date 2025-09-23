# Backend Deployment Guide

This document explains how to run the Flask API in development and how to deploy to a VPS using Docker Compose + Nginx.

## Structure
- Dockerfile
- docker-compose.dev.yml (development)
- docker-compose.prod.yml (production with Nginx)
- deploy/nginx/default.conf (reverse proxy)
- .env (local dev), .env.development, .env.qa, .env.production (templates)
- gunicorn.conf.py

## Environment Variables
Use one of the provided files as a template and put the real values:
- `.env` for local development (used by `docker-compose.dev.yml`)
- `.env.qa` for QA/staging
- `.env.production` for production on the VPS

Variables to set:
- DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
- SECRET_KEY, JWT_SECRET_KEY
- ALLOWED_ORIGINS (comma-separated, e.g. `https://app.example.com`)

## Development
Requirements: Docker and Docker Compose.

```bash
# From backend/
# Copy a template to .env (or edit .env directly)
cp .env.development .env

# Start DB + API (hot-reload via volume mount)
docker compose -f docker-compose.dev.yml up --build
# API available at http://127.0.0.1:5000
```

Alternatively (without Docker):
```bash
python -m venv .venv
. .venv/bin/activate  # (Windows PowerShell: .venv\\Scripts\\Activate.ps1)
pip install -r requirements.txt
# Ensure backend/.env exists with DB settings
python run.py
```

## Production on VPS
Assumes Docker is installed on the VPS.

```bash
# From backend/
# Put real secrets in .env.production
# Build and start API + Nginx
docker compose -f docker-compose.prod.yml --env-file .env.production up -d --build

# Logs
docker compose -f docker-compose.prod.yml logs -f

# Stop
docker compose -f docker-compose.prod.yml down
```

Nginx will listen on port 80 and reverse proxy to the `api` service on port 5000.
If you need TLS, terminate at Nginx (mount certs and update `default.conf`).

## Notes
- CORS origins are read from `ALLOWED_ORIGINS`.
- Gunicorn defaults can be tuned via `GUNICORN_*` env vars.
- Database migrations (Alembic) can be added later to version schema.
