#!/bin/bash
# Script para separar el backend del monorepo
# Uso: .\separate-backend.ps1

Write-Host "🚀 Iniciando separación del backend..." -ForegroundColor Green

# Verificar que estamos en el directorio correcto
if (!(Test-Path "app") -or !(Test-Path "requirements.txt")) {
    Write-Host "❌ Error: Este script debe ejecutarse desde el directorio del backend" -ForegroundColor Red
    exit 1
}

# Verificar estado de git
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  Advertencia: Hay cambios sin confirmar:" -ForegroundColor Yellow
    Write-Host $gitStatus
    $continue = Read-Host "¿Continuar de todos modos? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "❌ Operación cancelada" -ForegroundColor Red
        exit 1
    }
}

# Crear backup
$backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "📦 Creando backup en: $backupDir" -ForegroundColor Cyan
Copy-Item -Path "." -Destination "../$backupDir" -Recurse -Force

# Verificar que no tenemos remote origin configurado aún
$remoteOrigin = git remote get-url origin 2>$null
if ($remoteOrigin) {
    Write-Host "⚠️  Ya existe un remote origin: $remoteOrigin" -ForegroundColor Yellow
    $overwrite = Read-Host "¿Sobrescribir? (y/N)"
    if ($overwrite -eq "y" -or $overwrite -eq "Y") {
        git remote remove origin
    }
}

# Preguntar por el nombre del nuevo repositorio
$repoName = Read-Host "📝 Nombre del nuevo repositorio (por defecto: HarchaMAq-Backend)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "HarchaMAq-Backend"
}

$githubUser = Read-Host "👤 Usuario de GitHub (por defecto: panchoxgrande)"
if ([string]::IsNullOrWhiteSpace($githubUser)) {
    $githubUser = "panchoxgrande"
}

# Inicializar repo git si no existe
if (!(Test-Path ".git")) {
    Write-Host "🔧 Inicializando repositorio git..." -ForegroundColor Cyan
    git init
}

# Crear .gitignore específico para el backend si no existe
if (!(Test-Path ".gitignore")) {
    Write-Host "📝 Creando .gitignore para el backend..." -ForegroundColor Cyan
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Environment variables
.env
.env.local
.env.development
.env.test
.env.production
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite3
app.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Docker
.dockerignore

# Logs
*.log
logs/

# Testing
.coverage
.pytest_cache/
htmlcov/

# Backup files
backup_*/
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
}

# Crear README específico para el backend
Write-Host "📚 Creando README.md para el backend..." -ForegroundColor Cyan
@"
# HarchaMAq Backend

API backend para el sistema de gestión de maquinaria HarchaMAq.

## 🚀 Tecnologías

- **Framework**: Flask
- **Base de datos**: MySQL
- **Autenticación**: JWT
- **Containerización**: Docker
- **Deploy**: Railway/Fly.io

## 📦 Instalación

### Desarrollo Local

1. Clonar el repositorio:
``````bash
git clone https://github.com/$githubUser/$repoName.git
cd $repoName
``````

2. Crear entorno virtual:
``````bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
``````

3. Instalar dependencias:
``````bash
pip install -r requirements.txt
``````

4. Configurar variables de entorno:
``````bash
cp .env.example .env.development
# Editar .env.development con tus configuraciones
``````

5. Ejecutar la aplicación:
``````bash
python run.py
``````

### Con Docker

``````bash
# Desarrollo
docker-compose -f docker-compose.dev.yml up --build

# Producción
docker-compose -f docker-compose.prod.yml up --build
``````

## 🌐 API Endpoints

- **Documentación**: `http://localhost:5000/api`
- **Autenticación**: `POST /api/auth/login`
- **Máquinas**: `GET /api/maquinas`
- **Contratos**: `GET /api/contratos`
- **Recargas**: `GET /api/recargas`

## 🔧 Configuración

### Variables de Entorno

``````env
DATABASE_HOST=tu_host
DATABASE_USER=tu_usuario
DATABASE_PASSWORD=tu_password
DATABASE_NAME=tu_base_de_datos
DATABASE_PORT=3306
SECRET_KEY=tu_secret_key
JWT_SECRET_KEY=tu_jwt_secret
ALLOWED_ORIGINS=http://localhost:3000,https://tu-frontend.com
``````

## 🚀 Deploy

### Railway

``````bash
npm install -g @railway/cli
railway login
railway init
railway up
``````

### Fly.io

``````bash
fly launch
fly deploy
``````

## 🧪 Testing

``````bash
pytest
``````

## 📁 Estructura del Proyecto

``````
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   ├── auth/
│   ├── modules/
│   └── security/
├── tests/
├── Dockerfile
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── requirements.txt
└── run.py
``````

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
"@ | Out-File -FilePath "README.md" -Encoding UTF8

# Agregar todos los archivos
Write-Host "📁 Agregando archivos al repositorio..." -ForegroundColor Cyan
git add .

# Hacer commit inicial
Write-Host "💾 Creando commit inicial..." -ForegroundColor Cyan
git commit -m "feat: initial backend setup

- Flask API con autenticación JWT
- Módulos para maquinas, contratos, recargas
- Docker y docker-compose configurados
- Tests unitarios incluidos
- Documentación API con Flask-RESTX"

# Configurar rama main
git branch -M main

# Mostrar instrucciones finales
Write-Host ""
Write-Host "✅ ¡Separación del backend completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Crear el repositorio en GitHub: https://github.com/new" -ForegroundColor White
Write-Host "   - Nombre: $repoName" -ForegroundColor Gray
Write-Host "   - Descripción: Backend API para HarchaMAq" -ForegroundColor Gray
Write-Host "   - Público/Privado según tu preferencia" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Conectar y subir el código:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/$githubUser/$repoName.git" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Configurar deploy en Railway/Fly.io" -ForegroundColor White
Write-Host "4. Actualizar URLs en el frontend Flutter" -ForegroundColor White
Write-Host ""
Write-Host "💡 Backup creado en: ../$backupDir" -ForegroundColor Cyan
Write-Host "📚 Consulta BACKEND_SEPARATION.md para más detalles" -ForegroundColor Cyan