from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MaquinaRef:
    id: int
    nombre: str

@dataclass(frozen=True)
class UsuarioRef:
    id: int
    usuario: str
    # ✅ NUEVO - Campos adicionales del usuario
    usuario_id: Optional[str] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    rol: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    rut: Optional[str] = None

@dataclass(frozen=True)
class ObraRef:
    id: int
    nombre: str

@dataclass(frozen=True)
class ClienteRef:
    id: int
    nombre: str