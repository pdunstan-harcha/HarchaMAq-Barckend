from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class OperadorRef:
    id: int
    usuario: str
    usuario_id: Optional[str] = None
    nombre: Optional[str] = None
    
    