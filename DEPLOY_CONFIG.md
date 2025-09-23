# Deploy Configuration

Este archivo contiene las configuraciones específicas para diferentes proveedores de hosting.

## Railway

### 1. Configuración Automática

Railway detecta automáticamente proyectos Flask y configura el build.

### 2. Variables de Entorno Requeridas

```env
DATABASE_HOST
DATABASE_USER
DATABASE_PASSWORD
DATABASE_NAME
DATABASE_PORT=3306
SECRET_KEY
JWT_SECRET_KEY
ALLOWED_ORIGINS
FLASK_ENV=production
```

### 3. railway.json (Opcional)

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "gunicorn -c gunicorn.conf.py run:app",
    "healthcheckPath": "/api",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

## Fly.io

### 1. fly.toml

```toml
app = "harchamaq-backend"
primary_region = "mia"

[build]
  dockerfile = "Dockerfile"

[env]
  FLASK_ENV = "production"

[http_service]
  internal_port = 5000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/api"

[[services]]
  protocol = "tcp"
  internal_port = 5000

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

### 2. Comandos de Deploy

```bash
# Instalar Fly CLI
winget install flyio.flyctl

# Login y configuración inicial
fly auth login
fly launch
fly deploy
```

## Render

### 1. Configuración

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -c gunicorn.conf.py run:app`
- **Environment**: Python 3

### 2. render.yaml (Opcional)

```yaml
services:
  - type: web
    name: harchamaq-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -c gunicorn.conf.py run:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_HOST
        sync: false
      - key: DATABASE_USER
        sync: false
      - key: DATABASE_PASSWORD
        sync: false
      - key: DATABASE_NAME
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
```

## Variables de Entorno por Provider

| Variable | Railway | Fly.io | Render |
|----------|---------|--------|--------|
| DATABASE_HOST | ✅ | ✅ | ✅ |
| DATABASE_USER | ✅ | ✅ | ✅ |
| DATABASE_PASSWORD | ✅ | ✅ | ✅ |
| DATABASE_NAME | ✅ | ✅ | ✅ |
| DATABASE_PORT | ✅ | ✅ | ✅ |
| SECRET_KEY | ✅ | ✅ | Auto |
| JWT_SECRET_KEY | ✅ | ✅ | Auto |
| ALLOWED_ORIGINS | ✅ | ✅ | ✅ |
| FLASK_ENV | ✅ | ✅ | ✅ |

## Base de Datos Externa

Si no usas la base de datos del proveedor, puedes usar:

### PlanetScale (MySQL)
- Plan gratuito disponible
- Compatible con MySQL
- Dashboard web intuitivo

### Railway MySQL
- Incluido en Railway
- Configuración automática

### Aiven (MySQL)
- Plan gratuito limitado
- Soporte completo MySQL

## Health Checks

Todos los proveedores usan el endpoint `/api` para verificar el estado:

```python
# En app/__init__.py
@api.route('/')
class HealthCheck(Resource):
    def get(self):
        return {'status': 'healthy', 'version': '1.0.0'}
```

## SSL/HTTPS

Todos los proveedores proporcionan SSL automático:
- Railway: Automático
- Fly.io: Let's Encrypt automático
- Render: SSL automático

## Logs y Monitoreo

```bash
# Railway
railway logs

# Fly.io
fly logs

# Render
# Ver en el dashboard web
```

## Estimación de Costos

| Provider | Plan Gratuito | Límites |
|----------|---------------|---------|
| Railway | $5 créditos/mes | 500h CPU, 1GB RAM |
| Fly.io | Gratuito | 3 apps pequeñas |
| Render | Gratuito | 750h/mes, sleep después de 15min |

**Recomendación**: Railway para proyectos que necesitan estar siempre activos, Render para proyectos de prueba.