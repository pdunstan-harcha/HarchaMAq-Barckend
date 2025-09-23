from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Cliente:
    """Entidad de dominio para Cliente"""
    id: int
    id_cliente: Optional[str] = None
    nombre: Optional[str] = None
    rut: Optional[str] = None
