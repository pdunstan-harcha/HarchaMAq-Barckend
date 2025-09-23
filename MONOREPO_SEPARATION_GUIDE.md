# Guía para Separar el Monorepo

## Situación Actual
- **Backend**: `C:\Users\patricio dunstan sae\HarchaMAq` (Flask/Python)
- **Frontend**: `C:\Users\patricio dunstan sae\HarchaMAq-Frontend` (Flutter)

## Pasos para Separar los Repositorios

### 1. Crear Repositorio Separado para Backend

```bash
# En el directorio del backend actual
cd "C:\Users\patricio dunstan sae\HarchaMAq"

# Inicializar nuevo repo git (si no existe)
git init

# Añadir todos los archivos
git add .
git commit -m "Initial commit: Backend Flask API"

# Crear repo en GitHub llamado "HarchaMAq-Backend"
# Conectar con el repo remoto
git remote add origin https://github.com/panchoxgrande/HarchaMAq-Backend.git
git branch -M main
git push -u origin main
```

### 2. Crear Repositorio Separado para Frontend

```bash
# En el directorio del frontend
cd "C:\Users\patricio dunstan sae\HarchaMAq-Frontend"

# Inicializar nuevo repo git (si no existe)
git init

# Añadir todos los archivos
git add .
git commit -m "Initial commit: Flutter Mobile App"

# Crear repo en GitHub llamado "HarchaMAq-Frontend"
# Conectar con el repo remoto
git remote add origin https://github.com/panchoxgrande/HarchaMAq-Frontend.git
git branch -M main
git push -u origin main
```

### 3. Actualizar Configuraciones

#### Backend - Actualizar URLs y CORS
- Actualizar `app/__init__.py` para permitir CORS desde el dominio del frontend
- Configurar variables de entorno para URLs de producción

#### Frontend - Actualizar URLs de API
- Actualizar archivos de configuración para apuntar a la nueva URL del backend
- Revisar archivos `.env` y configuraciones de API

### 4. Configuración de Deploy Independiente

#### Backend
- **Railway/Fly.io**: Para el backend Flask
- **Variables de entorno**: Base de datos, JWT secrets, etc.

#### Frontend
- **Vercel**: Para aplicación Flutter Web
- **Play Store/App Store**: Para aplicaciones móviles

### 5. Beneficios de la Separación

✅ **CI/CD independiente** - Cada proyecto puede tener su propio pipeline
✅ **Equipos separados** - Frontend y backend pueden ser desarrollados independientemente
✅ **Deploy independiente** - Actualizar uno sin afectar el otro
✅ **Versionado separado** - Cada proyecto tiene su propio ciclo de releases
✅ **Permisos granulares** - Control de acceso por proyecto

### 6. Estructura Recomendada Final

```
HarchaMAq-Backend/          # Repositorio independiente
├── app/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md

HarchaMAq-Frontend/         # Repositorio independiente
├── lib/
├── android/
├── ios/
├── pubspec.yaml
└── README.md
```

## Próximos Pasos

1. ✅ Revisar que no haya referencias hardcodeadas entre proyectos
2. ✅ Configurar CORS adecuadamente
3. ✅ Crear los repositorios en GitHub
4. ✅ Configurar deploy independiente
5. ✅ Actualizar documentación de cada proyecto