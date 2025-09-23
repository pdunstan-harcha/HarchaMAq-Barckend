# HarchaMAq Backend

Backend API para sistema de gestión de maquinaria. Listo para Railway.

## Stack

- Flask + MySQL + JWT + Docker

## Local Development

```bash
pip install -r requirements.txt
cp .env.example .env
# Configurar variables en .env
python run.py
```

## Railway Deployment

1. Conectar repo a Railway
2. Agregar MySQL service
3. Configurar variables de entorno:
   - `DATABASE_HOST`, `DATABASE_USER`, `DATABASE_PASSWORD`
   - `SECRET_KEY`, `JWT_SECRET_KEY`
   - `FLASK_ENV=production`

## API Docs

- Local: http://localhost:5000/docs
- Health: http://localhost:5000/health