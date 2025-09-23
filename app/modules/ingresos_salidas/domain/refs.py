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