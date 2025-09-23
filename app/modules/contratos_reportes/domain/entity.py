# app/modules/contratos_reportes/domain/entity.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .refs import ContratoRef, MaquinaRef, UsuarioRef

@dataclass(frozen=True)
class ContratoReporte:
    id: int
    codigo: str
    fecha_inicio: Optional[datetime]
    descripcion: Optional[str]
    maquina_txt: Optional[str]
    contrato_txt: Optional[str]
    usuario_txt: Optional[str]
    contrato: Optional[ContratoRef] = None
    maquina: Optional[MaquinaRef] = None
    usuario: Optional[UsuarioRef] = None