# HarchaMAq Backend API

Backend API para el sistema de gestión de maquinaria HarchaMAq.

## 🚀 Tecnologías

- **Framework**: Flask
- **Base de datos**: MySQL
- **Autenticación**: JWT
- **Containerización**: Docker
- **Deploy**: Railway/Fly.io/Render

## 📦 Instalación Local

### 1. Clonar y configurar
```bash
git clone https://github.com/panchoxgrande/HarchaMAq-Backend.git
cd HarchaMAq-Backend
```

### 2. Entorno virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env.development
# Editar .env.development con tus configuraciones
```

### 5. Ejecutar
```bash
python run.py
```

## 🐳 Docker

### Desarrollo
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Producción
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## 📚 API Endpoints

- **Base URL**: http://localhost:5000/api
- **Documentación**: http://localhost:5000/api (Swagger UI)
- **Health Check**: GET /api

### Autenticación
- POST /api/auth/login - Login de usuario
- POST /api/auth/refresh - Renovar token

### Recursos
- GET /api/maquinas - Listar máquinas
- GET /api/contratos - Listar contratos
- GET /api/recargas - Listar recargas
- GET /api/obras - Listar obras
- GET /api/clientes - Listar clientes

## 🔧 Variables de Entorno

```env
# Base de datos
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=password
DATABASE_NAME=APP_HARCHA_MAQUINARIA
DATABASE_PORT=3306

# Flask
FLASK_ENV=development
SECRET_KEY=tu-secret-key
JWT_SECRET_KEY=tu-jwt-secret

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://tu-frontend.com
```

## 🚀 Deploy

### Railway
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Fly.io
```bash
fly launch
fly deploy
```

## 🧪 Testing

```bash
pytest
```

## 📁 Estructura

```
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   ├── auth/
│   ├── modules/
│   └── security/
├── tests/
├── .github/workflows/
├── Dockerfile
├── docker-compose.*.yml
├── requirements.txt
└── run.py
```

## 🔄 Separado del Monorepo

Este proyecto fue separado del monorepo original para:
- Deploy independiente
- CI/CD separado
- Desarrollo paralelo con el frontend
- Escalabilidad independiente

**Frontend Flutter**: https://github.com/panchoxgrande/HarchaMAq-Frontend

---
*Backend API desarrollado con ❤️ para HarchaMAq*
