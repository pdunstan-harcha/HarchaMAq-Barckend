# GitHub Secrets Configuration Guide

## 🔐 Repository Secrets (Sensitive Data)
Go to: **GitHub repo → Settings → Secrets and variables → Actions → Repository secrets**

Add these secrets:

```
SECRET_KEY = replace-with-strong-random-32-chars-here
DATABASE_PASSWORD = &83E6u;CJYCl
JWT_SECRET_KEY = replace-with-strong-random-jwt-key-here
RAILWAY_TOKEN = your_railway_deployment_token_here
```

## 📋 Repository Variables (Non-sensitive Data)  
Go to: **GitHub repo → Settings → Secrets and variables → Actions → Repository variables**

Add these variables:

```
FLASK_ENV = production
DATABASE_USER = deve
DATABASE_HOST = 163.172.82.28
DATABASE_PORT = 3306
DATABASE_NAME = APP_HARCHA_MAQUINARIA
ALLOWED_ORIGINS = https://app.harcha.example.com
LOG_LEVEL = INFO
```

## 🚀 Railway Environment Variables
Also configure these same variables in Railway dashboard:

1. Go to your Railway project
2. Click on your service  
3. Go to "Variables" tab
4. Add all the variables above (both secrets and non-secrets)

## 🔑 How to Generate Strong Keys

### SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### JWT_SECRET_KEY  
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## ✅ Verification
After adding all secrets and variables, the GitHub Actions workflow will:
1. Build Docker image with your real configuration
2. Test the container can start and respond to health checks
3. Run security scans
4. Deploy to Railway automatically on main branch pushes