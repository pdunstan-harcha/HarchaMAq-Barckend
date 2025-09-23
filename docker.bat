@echo off
REM Script de comandos para HarchaMAq Flask Backend en Windows

if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="local" goto local
if "%1"=="build" goto build
if "%1"=="run" goto run
if "%1"=="dev" goto dev
if "%1"=="prod" goto prod
if "%1"=="clean" goto clean
if "%1"=="stop" goto stop
if "%1"=="" goto help

:help
echo Comandos disponibles:
echo   docker.bat install   - Instalar dependencias Python
echo   docker.bat local     - Ejecutar localmente (sin Docker)
echo   docker.bat build     - Construir imagen Docker
echo   docker.bat run       - Ejecutar contenedor Docker
echo   docker.bat dev       - Desarrollo con docker-compose
echo   docker.bat prod      - Producción con docker-compose
echo   docker.bat clean     - Limpiar sistema Docker
echo   docker.bat stop      - Parar contenedores
goto end

:install
pip install -r requirements.txt
goto end

:local
python run.py
goto end

:build
docker build -t harchamaq-backend .
goto end

:run
docker run --rm -p 5000:5000 --env-file .env.example harchamaq-backend
goto end

:dev
docker-compose up --build
goto end

:prod
docker-compose -f docker-compose.prod.yml up --build
goto end

:clean
docker system prune -f
docker-compose down --volumes --remove-orphans
goto end

:stop
docker-compose down
goto end

:end