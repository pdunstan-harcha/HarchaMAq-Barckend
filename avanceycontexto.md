# 📋 **GUÍA COMPLETA - Implementación de Módulos DDD en HarchaMAq**

## 🎯 **Resumen del Proyecto**

Hemos implementado exitosamente una **arquitectura Domain Driven Design (DDD)** completa para la aplicación HarchaMAq, con dos módulos funcionales:

- ✅ **Módulo de Recargas** - CRUD completo
- ✅ **Módulo de Ingresos y Salidas** - CRUD completo

## 🏗️ **Arquitectura Implementada (DDD)**

```
📁 backend/app/modules/{modulo}/
├── 🎯 domain/                    # Lógica de negocio pura
│   ├── entity.py                # Entidades del dominio
│   ├── refs.py                  # Referencias a otras entidades
│   └── repository.py            # Contratos de repositorio
├── 🚀 application/              # Casos de uso
│   ├── listar.py               # Listar con paginación
│   ├── crear.py                # Crear nuevo registro
│   ├── obtener.py              # Obtener por ID
│   ├── actualizar.py           # Actualizar registro
│   └── eliminar.py             # Eliminar registro
├── 🔧 infrastructure/          # Implementación técnica
│   └── sqlalchemy_repository.py # Repositorio SQLAlchemy
└── 🌐 presentation/            # API REST
    ├── schemas.py              # Modelos Swagger/OpenAPI
    └── routes.py               # Endpoints RESTful
```

## 🎉 **Lo que Hemos Logrado**

### **🔥 Módulo de RECARGAS**

#### **📊 Funcionalidades:**
- ✅ **6 endpoints RESTful** completos
- ✅ **Paginación inteligente** (10-100 registros)
- ✅ **Búsqueda avanzada** en múltiples campos
- ✅ **Validaciones de negocio** robustas
- ✅ **Generación automática** de códigos únicos
- ✅ **Manejo de Foreign Keys** nulos

#### **🌐 API Endpoints:**
| Método | Endpoint | Funcionalidad |
|--------|----------|---------------|
| `GET` | `/recargas/` | Listar paginado con búsqueda |
| `POST` | `/recargas/` | Crear nueva recarga |
| `GET` | `/recargas/{id}` | Obtener recarga específica |
| `PUT` | `/recargas/{id}` | Actualizar recarga completa |
| `PATCH` | `/recargas/{id}` | Modificar recarga parcial |
| `DELETE` | `/recargas/{id}` | Eliminar recarga |

#### **🛡️ Problemas Resueltos:**
- ❌→✅ **Recursión infinita** en relaciones SQLAlchemy
- ❌→✅ **ID_RECARGA muy largo** (17→14 caracteres)
- ❌→✅ **Foreign Keys inválidos** (0→NULL)
- ❌→✅ **Búsquedas en campos NULL** (COALESCE)

### **🚛 Módulo de INGRESOS Y SALIDAS**

#### **📊 Funcionalidades:**
- ✅ **6 endpoints RESTful** completos
- ✅ **Validación de secuencia** (no ingresos/salidas consecutivos)
- ✅ **Cálculo automático de tiempo** entre movimientos
- ✅ **Control de ediciones** con timestamps
- ✅ **Endpoint adicional** para máquinas disponibles
- ✅ **Información del movimiento anterior**

#### **🌐 API Endpoints:**
| Método | Endpoint | Funcionalidad |
|--------|----------|---------------|
| `GET` | `/ingresos-salidas/` | Listar paginado |
| `POST` | `/ingresos-salidas/` | Crear ingreso/salida |
| `GET` | `/ingresos-salidas/{id}` | Obtener específico |
| `PUT` | `/ingresos-salidas/{id}` | Actualizar |
| `DELETE` | `/ingresos-salidas/{id}` | Eliminar |
| `GET` | `/ingresos-salidas/maquinas-disponibles` | Máquinas para dropdown |

#### **🎯 Características Especiales:**
- ✅ **Lógica de negocio**: Validación de secuencia INGRESO→SALIDA→INGRESO
- ✅ **Cálculo de tiempo**: Automático entre movimientos
- ✅ **Estados predefinidos**: OPERATIVA, MANTENIMIENTO, etc.
- ✅ **Formulario matching**: Coincide con interfaz mostrada

## 🔧 **Tecnologías y Patrones Utilizados**

### **🏗️ Arquitectura:**
- **Domain Driven Design (DDD)**
- **Repository Pattern**
- **Use Case Pattern**
- **Dependency Injection**
- **RESTful API Design**

### **🛠️ Stack Tecnológico:**
- **Backend**: Flask + SQLAlchemy + Flask-RESTX
- **Autenticación**: JWT con control de roles
- **Base de Datos**: MySQL
- **Documentación**: Swagger/OpenAPI automática
- **Validación**: Marshmallow + Custom validations

### **🔐 Seguridad:**
- **JWT Authentication** obligatorio
- **Role-based Access Control** (Admin, Super Admin, Inspector)
- **Validación de entrada** robusta
- **SQL Injection** protegido por SQLAlchemy ORM

## 📖 **Estructura de Archivos Creados/Modificados**

### **Archivos Base Modificados:**
```
backend/
├── app/
│   ├── __init__.py                    # ✅ Registrar módulos
│   └── models.py                      # ✅ Modelos SQLAlchemy
```

### **Módulo Recargas:**
```
backend/app/modules/recargas/
├── domain/
│   ├── entity.py                      # ✅ Entidad Recarga
│   ├── refs.py                        # ✅ Referencias externas
│   └── repository.py                  # ✅ Contrato repositorio
├── application/
│   ├── listar.py                      # ✅ Caso uso listar
│   ├── crear.py                       # ✅ Caso uso crear
│   ├── obtener.py                     # ✅ Caso uso obtener
│   ├── actualizar.py                  # ✅ Caso uso actualizar
│   └── eliminar.py                    # ✅ Caso uso eliminar
├── infrastructure/
│   └── sqlalchemy_repository.py       # ✅ Repositorio SQLAlchemy
└── presentation/
    ├── api_namespace.py               # ✅ Namespace Swagger
    └── routes.py                      # ✅ Endpoints REST
```

### **Módulo Ingresos y Salidas:**
```
backend/app/modules/ingresos_salidas/
├── domain/
│   ├── entity.py                      # ✅ Entidad IngresoSalida
│   ├── refs.py                        # ✅ Referencias
│   └── repository.py                  # ✅ Contrato repositorio
├── application/
│   ├── listar.py                      # ✅ Casos de uso completos
│   ├── crear.py                       # ✅ Con validación secuencia
│   ├── obtener.py                     # ✅ Con info anterior
│   ├── actualizar.py                  # ✅ Con control edición
│   └── eliminar.py                    # ✅ Con validación dependencias
├── infrastructure/
│   └── sqlalchemy_repository.py       # ✅ Con cálculo tiempo
└── presentation/
    ├── schemas.py                     # ✅ Modelos API completos
    └── routes.py                      # ✅ 6 endpoints + máquinas
```

---

# 🚀 **GUÍA PARA IMPLEMENTAR NUEVOS MÓDULOS**

## 📋 **Paso a Paso - Crear Nuevo Módulo**

### **1️⃣ Preparación - Análisis de Tabla**

Antes de empezar, necesitas:

1. **📄 Estructura SQL** de la tabla
2. **🎨 Interfaz/Formulario** (si existe)
3. **🎯 Reglas de negocio** específicas

### **2️⃣ Crear Estructura de Carpetas**

```bash
# Ejemplo para módulo "mantenimientos"
mkdir -p backend/app/modules/mantenimientos/domain
mkdir -p backend/app/modules/mantenimientos/application
mkdir -p backend/app/modules/mantenimientos/infrastructure
mkdir -p backend/app/modules/mantenimientos/presentation

# Crear archivos __init__.py
touch backend/app/modules/mantenimientos/__init__.py
touch backend/app/modules/mantenimientos/domain/__init__.py
touch backend/app/modules/mantenimientos/application/__init__.py
touch backend/app/modules/mantenimientos/infrastructure/__init__.py
touch backend/app/modules/mantenimientos/presentation/__init__.py
```

### **3️⃣ Implementar Dominio**

#### **A. Crear `domain/refs.py`**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MaquinaRef:
    id: int
    nombre: str
    codigo: Optional[str] = None

@dataclass(frozen=True)
class UsuarioRef:
    id: int
    usuario: str
    nombre_completo: Optional[str] = None

# Agregar otras referencias según el módulo
```

#### **B. Crear `domain/entity.py`**
```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .refs import MaquinaRef, UsuarioRef

@dataclass(frozen=True)
class NombreEntidad:  # Cambiar por el nombre real
    # Campos exactos según la BD (revisar SQL)
    id: int  # pk primario
    codigo: Optional[str]
    fecha: Optional[datetime]
    # ... otros campos según la tabla
    
    # Referencias a otras entidades
    maquina: Optional[MaquinaRef]
    usuario: Optional[UsuarioRef]
```

#### **C. Crear `domain/repository.py`**
```python
from typing import Protocol, Sequence, Optional
from .entity import NombreEntidad

class PaginationParams:
    def __init__(self, page: int = 1, per_page: int = 20, search: str = None):
        self.page = max(1, page)
        self.per_page = min(100, max(10, per_page))
        self.search = search.strip() if search else None

class PaginatedResult:
    def __init__(self, data: Sequence[NombreEntidad], total: int, page: int, per_page: int):
        self.data = data
        self.total = total
        self.page = page
        self.per_page = per_page
        self.total_pages = (total + per_page - 1) // per_page
        self.has_next = page < self.total_pages
        self.has_prev = page > 1

class NombreEntidadRepository(Protocol):
    def listar_paginado(self, params: PaginationParams) -> PaginatedResult: ...
    def obtener_por_id(self, entidad_id: int) -> Optional[NombreEntidad]: ...
    def crear(self, payload: dict) -> NombreEntidad: ...
    def actualizar(self, entidad_id: int, payload: dict) -> Optional[NombreEntidad]: ...
    def eliminar(self, entidad_id: int) -> bool: ...
```

### **4️⃣ Implementar Casos de Uso**

#### **A. `application/listar.py`**
```python
from dataclasses import dataclass
from typing import Sequence
from ..domain.repository import NombreEntidadRepository, PaginationParams
from ..domain.entity import NombreEntidad

@dataclass
class ListNombreEntidadInput:
    page: int = 1
    per_page: int = 20
    search: str = None

@dataclass
class ListNombreEntidadOutput:
    data: Sequence[NombreEntidad]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

class ListNombreEntidadUseCase:
    def __init__(self, repo: NombreEntidadRepository):
        self.repo = repo

    def execute(self, input_data: ListNombreEntidadInput = None) -> ListNombreEntidadOutput:
        if input_data is None:
            input_data = ListNombreEntidadInput()
            
        params = PaginationParams(
            page=input_data.page,
            per_page=input_data.per_page,
            search=input_data.search
        )
        
        result = self.repo.listar_paginado(params)
        
        return ListNombreEntidadOutput(
            data=result.data,
            total=result.total,
            page=result.page,
            per_page=result.per_page,
            total_pages=result.total_pages,
            has_next=result.has_next,
            has_prev=result.has_prev
        )
```

#### **B. Crear otros casos de uso:**
- `application/crear.py` - Basado en el de recargas
- `application/obtener.py` - Basado en el de recargas
- `application/actualizar.py` - Basado en el de recargas
- `application/eliminar.py` - Basado en el de recargas

### **5️⃣ Implementar Infraestructura**

#### **A. Actualizar `app/models.py`**
```python
# Agregar modelo SQLAlchemy según la estructura SQL
class NombreTabla(db.Model):
    __tablename__ = "NOMBRE_TABLA_BD"

    # Campos exactos según SQL
    pkId = db.Column(db.Integer, primary_key=True)
    CAMPO1 = db.Column(db.String(50))
    CAMPO2 = db.Column(db.DateTime)
    # ... otros campos
    
    # Foreign Keys
    pkMaquina = db.Column(db.Integer, db.ForeignKey("MAQUINAS.pkMaquina"))
    pkUsuario = db.Column(db.Integer, db.ForeignKey("USUARIOS.pkUsuario"))

    # Relaciones
    maquina = db.relationship("Maquina", foreign_keys=[pkMaquina])
    usuario = db.relationship("User", foreign_keys=[pkUsuario])
```

#### **B. Crear `infrastructure/sqlalchemy_repository.py`**
```python
import datetime
from typing import Sequence, Optional
from sqlalchemy import or_, desc
from app.models import NombreTabla as SANombreTabla
from app import db
from ..domain.entity import NombreEntidad
from ..domain.repository import NombreEntidadRepository, PaginationParams, PaginatedResult

def _to_domain(record: SANombreTabla, include_relations: bool = True) -> NombreEntidad:
    """Convertir SQLAlchemy a dominio"""
    return NombreEntidad(
        id=record.pkId,
        # ... mapear todos los campos
        
        # Referencias (solo si include_relations=True)
        maquina=_maq_ref(record.maquina) if include_relations else None,
        usuario=_user_ref(record.usuario) if include_relations else None
    )

class SqlAlchemyNombreEntidadRepository(NombreEntidadRepository):
    
    def listar_paginado(self, params: PaginationParams) -> PaginatedResult:
        # Implementar igual que en recargas
        pass
    
    def obtener_por_id(self, entidad_id: int) -> Optional[NombreEntidad]:
        # Implementar igual que en recargas
        pass
    
    def crear(self, payload: dict) -> NombreEntidad:
        # Implementar con validaciones específicas del módulo
        # Generar código único
        # Aplicar lógica de negocio
        pass
    
    def actualizar(self, entidad_id: int, payload: dict) -> Optional[NombreEntidad]:
        # Implementar igual que en recargas
        pass
    
    def eliminar(self, entidad_id: int) -> bool:
        # Implementar igual que en recargas
        pass
```

### **6️⃣ Implementar Presentación**

#### **A. Crear `presentation/schemas.py`**
```python
from flask_restx import Namespace, fields

# Crear namespace
nombre_modulo_ns = Namespace('nombre-modulo', description='Descripción del módulo')

# Modelos de entrada y salida
entidad_input = nombre_modulo_ns.model('NombreEntidadInput', {
    'campo1': fields.String(required=True, description='Descripción'),
    'campo2': fields.DateTime(description='Fecha'),
    # ... otros campos
})

entidad_model = nombre_modulo_ns.model('NombreEntidadModel', {
    'id': fields.Integer(required=True),
    'codigo': fields.String(),
    # ... otros campos de salida
})

# Modelos de respuesta
list_response = nombre_modulo_ns.model('ListResponse', {
    'success': fields.Boolean(required=True),
    'data': fields.List(fields.Nested(entidad_model)),
    'pagination': fields.Nested(pagination_model)
})

# ... otros modelos según se necesiten
```

#### **B. Crear `presentation/routes.py`**
```python
from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required
from app.security.roles import roles_required, ROLE_ADMIN, ROLE_SUPER_ADMIN
from .schemas import nombre_modulo_ns, entidad_input, list_response

# Importar casos de uso
from ..infrastructure.sqlalchemy_repository import SqlAlchemyNombreEntidadRepository

# Instanciar repositorio y casos de uso
repository = SqlAlchemyNombreEntidadRepository()
# ... instanciar casos de uso

@nombre_modulo_ns.route('/')
class NombreEntidadList(Resource):
    
    @nombre_modulo_ns.marshal_with(list_response)
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def get(self):
        """Listar entidades"""
        # Implementar igual que en recargas
        pass
    
    @nombre_modulo_ns.expect(entidad_input, validate=True)
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def post(self):
        """Crear entidad"""
        # Implementar igual que en recargas
        pass

@nombre_modulo_ns.route('/<int:entidad_id>')
class NombreEntidadDetail(Resource):
    
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def get(self, entidad_id):
        """Obtener por ID"""
        pass
    
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def put(self, entidad_id):
        """Actualizar"""
        pass
    
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def delete(self, entidad_id):
        """Eliminar"""
        pass
```

### **7️⃣ Registrar en la Aplicación**

#### **Actualizar `app/__init__.py`**
```python
# Agregar al final antes del return app
from .modules.nombre_modulo.presentation.schemas import nombre_modulo_ns
from .modules.nombre_modulo.presentation import routes as nombre_modulo_routes
api.add_namespace(nombre_modulo_ns, path='/nombre-modulo')
```

### **8️⃣ Probar el Módulo**

#### **A. Reiniciar servidor:**
```bash
python run.py
```

#### **B. Verificar Swagger:**
```
http://127.0.0.1:5000/
```

#### **C. Probar endpoints:**
```http
# Listar
GET http://127.0.0.1:5000/nombre-modulo/
Authorization: Bearer tu_token

# Crear
POST http://127.0.0.1:5000/nombre-modulo/
Authorization: Bearer tu_token
Content-Type: application/json

{
  "campo1": "valor",
  "campo2": "2025-09-17T10:00:00"
}
```

---

## 🎯 **Módulos Sugeridos para Implementar**

### **📋 Basados en las Tablas Existentes:**

1. **📝 MANTENIMIENTOS** (`MAQUINAS_MANTENIMIENTOS`)
   - Registro de mantenimientos preventivos/correctivos
   - Validación de fechas de próximo mantenimiento
   - Control de estados (PENDIENTE, EN_PROCESO, COMPLETADO)

2. **🔧 INSPECCIONES** (`INSPECCIONES`)
   - Registro de inspecciones de seguridad
   - Checklists predefinidos
   - Aprobación/rechazo con observaciones

3. **🏗️ OBRAS** (`OBRAS`)
   - Gestión de proyectos/obras
   - Asignación de máquinas a obras
   - Control de fechas inicio/fin

4. **👥 OPERADORES** (`OPERADORES`)
   - Gestión de operadores de máquinas
   - Certificaciones y licencias
   - Asignación temporal a máquinas

5. **💰 COSTOS** (si existe tabla de costos)
   - Seguimiento de costos operacionales
   - Combustible, mantenimiento, operación
   - Reportes por período

### **🎯 Priorización Sugerida:**

1. **🥇 MANTENIMIENTOS** - Crítico para operación
2. **🥈 INSPECCIONES** - Importante para seguridad
3. **🥉 OBRAS** - Importante para gestión
4. **4️⃣ OPERADORES** - Complementario
5. **5️⃣ COSTOS** - Para análisis

---

## 🔧 **Consejos y Mejores Prácticas**

### **📝 Nomenclatura:**
- **Entidades**: Singular, PascalCase (`Mantenimiento`, `Inspeccion`)
- **Repositories**: `NombreEntidadRepository`
- **Use Cases**: `CreateNombreEntidadUseCase`
- **Endpoints**: kebab-case (`/mantenimientos`, `/inspecciones`)

### **🎯 Validaciones:**
- **Dominio**: Reglas de negocio puras
- **Aplicación**: Validaciones de casos de uso
- **Presentación**: Validaciones de entrada HTTP

### **🔄 Reutilización:**
- **Copiar estructura** de módulos existentes
- **Adaptar lógica específica** según reglas de negocio
- **Mantener patrones consistentes**

### **🐛 Testing:**
- **Probar cada endpoint** individualmente
- **Verificar validaciones** con datos inválidos
- **Confirmar paginación** y búsqueda

### **📚 Documentación:**
- **Swagger automático** está configurado
- **Agregar descripciones** claras en schemas
- **Documentar reglas de negocio** específicas

---

## 🚀 **Próximos Pasos Recomendados**

### **Inmediato:**
1. **🧪 Testing automatizado** - Crear pruebas unitarias
2. **🔐 Logging avanzado** - Mejorar el sistema de logs
3. **⚡ Performance** - Optimizar queries con índices

### **Mediano Plazo:**
1. **📊 Reportes** - Módulo de reportes y analytics
2. **📱 API Mobile** - Endpoints específicos para móvil
3. **🔄 Sincronización** - Sistema de sincronización offline

### **Largo Plazo:**
1. **🤖 Automatización** - Procesos automáticos (recordatorios, alertas)
2. **📈 Dashboard** - Panel de control con métricas
3. **🌐 Integración** - APIs externas (GPS, sensores)

---

## 📞 **Soporte y Recursos**

### **🔍 Para Resolver Problemas:**
1. **Revisar logs** detallados en consola
2. **Verificar estructura SQL** vs modelos SQLAlchemy
3. **Comprobar imports** y dependencias
4. **Validar JWT tokens** y permisos

### **📖 Documentación de Referencia:**
- **Flask-RESTX**: [https://flask-restx.readthedocs.io/](https://flask-restx.readthedocs.io/)
- **SQLAlchemy**: [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/)
- **Domain Driven Design**: Conceptos aplicados en la arquitectura

### **🎯 Patrones Implementados:**
- **Repository Pattern**: Abstracción de persistencia
- **Use Case Pattern**: Lógica de aplicación aislada
- **Dependency Injection**: Desacoplamiento de componentes
- **Clean Architecture**: Separación clara de capas

---

## ✅ **Checklist para Nuevo Módulo**

### **Antes de Empezar:**
- [ ] 📄 Analizar estructura SQL de la tabla
- [ ] 🎨 Revisar interfaz/formulario (si existe)
- [ ] 🎯 Definir reglas de negocio específicas
- [ ] 🔍 Identificar relaciones con otras tablas

### **Implementación:**
- [ ] 📁 Crear estructura de carpetas
- [ ] 🎯 Implementar capa de dominio (entity, refs, repository)
- [ ] 🚀 Crear casos de uso (listar, crear, obtener, actualizar, eliminar)
- [ ] 🔧 Desarrollar repositorio SQLAlchemy
- [ ] 🌐 Implementar presentación (schemas, routes)
- [ ] 🔗 Registrar en aplicación principal

### **Testing:**
- [ ] 🧪 Probar endpoints con Postman/Insomnia
- [ ] 📖 Verificar documentación Swagger
- [ ] 🔐 Confirmar autenticación y autorización
- [ ] 📊 Validar paginación y búsqueda
- [ ] ✅ Probar validaciones con datos inválidos

### **Documentación:**
- [ ] 📝 Actualizar este README con el nuevo módulo
- [ ] 💬 Documentar reglas de negocio específicas
- [ ] 🎯 Agregar ejemplos de uso

---

## 🎉 **¡Felicitaciones!**

Has implementado exitosamente una **arquitectura DDD completa y escalable**. Los módulos siguientes serán mucho más rápidos de implementar siguiendo estos patrones establecidos.

**¡El sistema está listo para crecer de manera organizada y mantenible!** 🚀

---

## 📊 **Ejemplos de Testing**

### **Ejemplo con cURL:**

```bash
# Listar recargas
curl -X GET "http://127.0.0.1:5000/recargas/?page=1&per_page=20" \
     -H "Authorization: Bearer tu_jwt_token"

# Crear recarga
curl -X POST "http://127.0.0.1:5000/recargas/" \
     -H "Authorization: Bearer tu_jwt_token" \
     -H "Content-Type: application/json" \
     -d '{
       "pkMaquina": 2,
       "pkUsuario": 150,
       "LITROS": 100,
       "OBSERVACIONES": "Recarga de prueba"
     }'

# Crear ingreso
curl -X POST "http://127.0.0.1:5000/ingresos-salidas/" \
     -H "Authorization: Bearer tu_jwt_token" \
     -H "Content-Type: application/json" \
     -d '{
       "pkMaquina": 1,
       "pkUsuario": 150,
       "INGRESO_SALIDA": "INGRESO",
       "ESTADO_MAQUINA": "OPERATIVA",
       "Observaciones": "Ingreso de prueba"
     }'
```

### **Ejemplo con Postman Collections:**

```json
{
  "info": {
    "name": "HarchaMAq API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{jwt_token}}",
        "type": "string"
      }
    ]
  },
  "item": [
    {
      "name": "Recargas",
      "item": [
        {
          "name": "Listar Recargas",
          "request": {
            "method": "GET",
            "url": "{{base_url}}/recargas/"
          }
        },
        {
          "name": "Crear Recarga",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/recargas/",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"pkMaquina\": 2,\n  \"pkUsuario\": 150,\n  \"LITROS\": 100\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            }
          }
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://127.0.0.1:5000"
    },
    {
      "key": "jwt_token",
      "value": "tu_token_aqui"
    }
  ]
}
```

---

*Última actualización: 20 de septiembre de 2025*
*Versión: 1.0*
*Autor: Sistema de desarrollo HarchaMAq*