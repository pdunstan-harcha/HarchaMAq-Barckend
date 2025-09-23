# Checklist para Separación del Monorepo

## ✅ Pre-separación (Completado)

- [x] **Backup creado** - Los archivos originales están seguros
- [x] **Documentación generada** - Guías detalladas disponibles
- [x] **Scripts de automatización** - Script PowerShell para separación
- [x] **Configuraciones de deploy** - Railway, Fly.io, Render configurados
- [x] **CI/CD configurado** - GitHub Actions listo
- [x] **Health checks** - Endpoints de monitoreo implementados

## 🚀 Ejecución de la Separación

### Paso 1: Ejecutar Script de Separación
```powershell
# En PowerShell, desde el directorio del backend
.\separate-backend.ps1
```

### Paso 2: Crear Repositorio en GitHub
- [ ] Ir a https://github.com/new
- [ ] Nombre: `HarchaMAq-Backend`
- [ ] Descripción: `Backend API para HarchaMAq - Sistema de gestión de maquinaria`
- [ ] Configurar como público/privado según preferencia
- [ ] **NO** inicializar con README (ya tienes uno)

### Paso 3: Conectar y Subir Código
```bash
git remote add origin https://github.com/panchoxgrande/HarchaMAq-Backend.git
git push -u origin main
```

### Paso 4: Configurar Secrets en GitHub (para CI/CD)
En GitHub → Settings → Secrets and variables → Actions:

- [ ] `RAILWAY_TOKEN` (si usas Railway)
- [ ] `FLY_API_TOKEN` (si usas Fly.io)

## 🌐 Deploy del Backend

### Opción A: Railway (Recomendado)
- [ ] Instalar Railway CLI: `npm install -g @railway/cli`
- [ ] Login: `railway login`
- [ ] Conectar repo: `railway init`
- [ ] Configurar variables de entorno en Railway dashboard
- [ ] Deploy: `railway up`

### Opción B: Fly.io
- [ ] Instalar Fly CLI: `winget install flyio.flyctl`
- [ ] Login: `fly auth login`
- [ ] Launch: `fly launch`
- [ ] Configurar secrets: `fly secrets set DATABASE_HOST=...`
- [ ] Deploy: `fly deploy`

### Opción C: Render
- [ ] Conectar repositorio en Render dashboard
- [ ] Configurar variables de entorno
- [ ] Deploy automático activado

## 🔧 Configuración de Variables de Entorno

En tu proveedor de hosting, configurar:

```env
DATABASE_HOST=tu_host_de_mysql
DATABASE_USER=tu_usuario
DATABASE_PASSWORD=tu_password_seguro
DATABASE_NAME=APP_HARCHA_MAQUINARIA
DATABASE_PORT=3306
SECRET_KEY=tu_secret_key_super_largo_y_seguro
JWT_SECRET_KEY=tu_jwt_secret_diferente_y_seguro
FLASK_ENV=production
ALLOWED_ORIGINS=https://tu-frontend.vercel.app,https://tu-dominio.com
```

## 📱 Actualizar Frontend

Una vez el backend esté desplegado:

- [ ] Obtener URL del backend desplegado (ej: `https://harchamaq-backend.railway.app`)
- [ ] Actualizar configuración del frontend Flutter
- [ ] Probar conexión frontend → backend
- [ ] Verificar que CORS funciona correctamente

## 🧪 Verificaciones

### Backend Funcionando
- [ ] `curl https://tu-backend.railway.app/api` responde con `{"status": "healthy"}`
- [ ] Endpoints de autenticación funcionan
- [ ] Base de datos se conecta correctamente
- [ ] Logs no muestran errores críticos

### Integración Frontend-Backend
- [ ] Frontend puede hacer login
- [ ] Frontend puede obtener datos de las APIs
- [ ] No hay errores de CORS
- [ ] Autenticación JWT funciona end-to-end

## 📈 Post-separación

### Desarrollo
- [ ] Actualizar documentación del equipo
- [ ] Configurar entornos de desarrollo separados
- [ ] Establecer workflows de desarrollo independientes

### Monitoreo
- [ ] Configurar alertas de salud del backend
- [ ] Monitorear logs de producción
- [ ] Establecer métricas de performance

### Mantenimiento
- [ ] Backups automáticos de la base de datos
- [ ] Plan de updates y security patches
- [ ] Documentar procedimientos de rollback

## 🆘 Troubleshooting

### Si el deploy falla:
1. Revisar logs del proveedor
2. Verificar variables de entorno
3. Comprobar que el Dockerfile funciona localmente
4. Verificar conectividad de base de datos

### Si hay errores de CORS:
1. Verificar `ALLOWED_ORIGINS` en variables de entorno
2. Comprobar que el frontend usa la URL correcta
3. Revisar headers en las requests del frontend

### Si la base de datos no conecta:
1. Verificar credenciales en variables de entorno
2. Comprobar que la base de datos acepta conexiones externas
3. Revisar firewall y configuraciones de red

---

## 📞 Soporte

Si encuentras problemas durante la separación:

1. **Revisa los logs** del proveedor de hosting
2. **Consulta la documentación** en `BACKEND_SEPARATION.md`
3. **Verifica la configuración** en `DEPLOY_CONFIG.md`
4. **Usa el backup** creado automáticamente si necesitas revertir

**¡Buena suerte con la separación! 🚀**