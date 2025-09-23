# HarchaMAq Backend

Backend API## API Docs

- Local: http://localhost:5000/docs
- Health: http://localhost:5000/health

## 🐳 Docker Support

### Development
```bash
# Con docker-compose (incluye MySQL)
docker-compose up --build

# Solo la app
docker build -t harchamaq-backend .
docker run -p 5000:5000 --env-file .env harchamaq-backend
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up --build
```

### Comandos disponibles

**Linux/Mac (Makefile):**
```bash
make build      # Construir imagen Docker
make dev        # Desarrollo con docker-compose
make local      # Ejecutar sin Docker
```

**Windows (Batch script):**
```batch
docker.bat build     # Construir imagen Docker
docker.bat dev       # Desarrollo con docker-compose
docker.bat local     # Ejecutar sin Docker  
```

## 🔒 Security & CI/CD

### Security Scanning
- **Trivy**: Vulnerability scanning of dependencies and Docker images
- **SARIF reports**: Security findings uploaded to GitHub Security tab

### CI/CD Pipeline
1. **Build & Test**: Docker image build and health check
2. **Security Scan**: Trivy scans filesystem and Docker image  
3. **Deploy**: Automatic deployment to Railway (main branch only)

## Configuration

### GitHub Secrets Required
```bash
RAILWAY_TOKEN - Railway deployment token
```a sistema de gestión de maquinaria. Listo para Railway con análisis de seguridad y calidad.

## Stack

- Flask + MySQL + JWT + Docker
- Trivy (security scanning)
- SonarQube (code quality)

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

## Security & Quality

- **Trivy**: Vulnerability scanning en Docker images y filesystem
- **SonarQube**: Análisis de calidad de código
- **GitHub Security**: Reports automáticos de vulnerabilidades

## API Docs

- Local: <http://localhost:5000/docs>
- Health: <http://localhost:5000/health>

## CI/CD Pipeline

1. **Security & Quality Analysis**:
   - Validation de estructura del proyecto
   - SonarQube code quality scan
   - Trivy security vulnerability scan
   - Upload results a GitHub Security tab

2. **Deploy**: Automático a Railway en push a main branch