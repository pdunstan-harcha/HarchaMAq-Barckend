from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Obra:
    """Entidad de dominio para Obra"""
    id: int
    id_obra: Optional[str] = None
    nombre: Optional[str] = None
