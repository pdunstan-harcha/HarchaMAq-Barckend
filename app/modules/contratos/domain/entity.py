from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass(frozen=True)
class Contrato:
    """Entidad de dominio para Contrato"""
    id: int
    id_contrato: Optional[str] = None
    nombre: Optional[str] = None
    pk_maquina: Optional[int] = None
    pk_cliente: Optional[int] = None
    pk_obra: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    estado: Optional[str] = None
    # Datos relacionados para mostrar
    maquina_nombre: Optional[str] = None
    cliente_nombre: Optional[str] = None
    obra_nombre: Optional[str] = None
