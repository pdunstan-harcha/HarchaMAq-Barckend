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

@dataclass(frozen=True)
class ObraRef:
    id: int
    nombre: str

@dataclass(frozen=True)
class ClienteRef:
    id: int
    nombre: str