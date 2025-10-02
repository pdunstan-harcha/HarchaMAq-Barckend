from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ContratoRef:
    id: int
    nombre: Optional[str] = None
    obra_txt: Optional[str] = None
    cliente_txt: Optional[str] = None


@dataclass(frozen=True)
class MaquinaRef:
    id: int
    nombre: Optional[str] = None


@dataclass(frozen=True)
class UsuarioRef:
    id: int
    usuario: Optional[str] = None