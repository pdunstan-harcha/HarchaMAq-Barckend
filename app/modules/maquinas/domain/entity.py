from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import datetime
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
    hr_actual: Optional[int] = None
    km_actual: Optional[int] = None
    pk_ultima_recarga: Optional[int] = None
    id_ultima_recarga: Optional[str] = None
    litros_ultima: Optional[int] = None
    fecha_ultima: Optional[datetime] = None  