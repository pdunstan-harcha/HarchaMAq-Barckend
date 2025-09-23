from dataclasses import dataclass
from typing import Optional, Sequence
from .operador_ref import OperadorRef

@dataclass(frozen=True)
class Maquina:
    id: int
    nombre: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    patente: Optional[str] = None   
    estado: Optional[str] = None
    id_maquina: Optional[str] = None
    operadores: Sequence[OperadorRef] = ()   