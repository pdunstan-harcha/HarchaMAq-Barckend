# Separación del Monorepo - Backend

Este documento contiene los pasos específicos para separar el backend del monorepo actual.

## ⚠️ Antes de Empezar

1. **Haz backup de tus archivos actuales**
2. **Asegúrate de que no hay cambios sin confirmar** (`git status`)
3. **Documenta las URLs actuales** que usa el frontend para conectar al backend

## 🔧 Configuraciones a Actualizar

### 1. Variables de Entorno para Producción

Crear archivo `.env.production` con configuración para deploy:

```env
# Base de datos en producción (ej: Railway MySQL)
DATABASE_HOST="railway.app"
DATABASE_USER="root"
DATABASE_PASSWORD="tu_password_de_produccion"
DATABASE_NAME="railway"
DATABASE_PORT="3306"

# Flask en producción
FLASK_ENV="production"
SECRET_KEY="tu_secret_key_super_seguro_para_produccion"
JWT_SECRET_KEY="tu_jwt_secret_super_seguro"

# CORS - Permitir solo el dominio del frontend
ALLOWED_ORIGINS="https://tu-frontend.vercel.app,https://tu-dominio.com"

# URLs del backend (para logging y referencias)
API_BASE_URL="https://tu-backend.railway.app"
```

### 2. Dockerfile Optimizado para Producción

El `Dockerfile` actual está bien configurado para producción con Gunicorn.

### 3. Scripts de Deploy

#### Para Railway
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login y deploy
railway login
railway init
railway up
```

#### Para Fly.io
```bash
# Instalar Fly CLI
# Después ejecutar:
fly launch
fly deploy
```

### 4. CI/CD con GitHub Actions

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy Backend to Railway

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Railway
      uses: railway-app/cli@v3
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      with:
        command: up
```

## 🚀 Pasos de Separación

### 1. Crear Nuevo Repositorio

```bash
# En el directorio actual del backend
git init
git add .
git commit -m "feat: initial backend setup"

# Conectar al nuevo repo (crear primero en GitHub)
git remote add origin https://github.com/panchoxgrande/HarchaMAq-Backend.git
git branch -M main
git push -u origin main
```

### 2. Configurar Variables de Entorno en el Provider

**Railway:**
- Variables → Add Variable
- Agregar todas las variables del `.env.production`

**Fly.io:**
- `fly secrets set DATABASE_HOST=tu_host`
- `fly secrets set DATABASE_PASSWORD=tu_password`
- etc.

### 3. Deploy Inicial

```bash
# Railway
railway up

# Fly.io
fly deploy
```

### 4. Probar Endpoints

Una vez desplegado, probar que los endpoints funcionen:

```bash
# Salud del API
curl https://tu-backend.railway.app/api

# Login (ejemplo)
curl -X POST https://tu-backend.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'
```

## 📱 Actualizar Frontend

Una vez el backend esté desplegado, actualizar el frontend:

1. **Cambiar la URL base** del API en el frontend
2. **Actualizar configuraciones de CORS** si es necesario
3. **Probar la comunicación** entre frontend y backend

## 🔍 Verificaciones Finales

- ✅ Backend funciona independientemente
- ✅ Base de datos se conecta correctamente
- ✅ CORS configurado para el dominio del frontend
- ✅ Endpoints responden correctamente
- ✅ Autenticación JWT funciona
- ✅ Variables de entorno están seguras

## 📞 URLs de Ejemplo

Después de la separación:

- **Backend**: `https://harchamaq-backend.railway.app`
- **Frontend**: `https://harchamaq-frontend.vercel.app`
- **Documentación API**: `https://harchamaq-backend.railway.app/api`

---

**Próximo paso**: Una vez que el backend esté funcionando independientemente, podrás actualizar las URLs en el frontend Flutter.