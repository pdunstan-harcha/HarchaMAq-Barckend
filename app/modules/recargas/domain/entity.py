from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .refs import MaquinaRef, UsuarioRef, ObraRef, ClienteRef

@dataclass(frozen=True)
class Recarga:
    id: int
    codigo: str
    fecha: Optional[datetime]
    litros: Optional[int]
    foto: Optional[str]
    observaciones: Optional[str]
    odometro: Optional[int]
    kilometros: Optional[int]
    fechahora_recarga: Optional[datetime]
    patente: Optional[str]
    rut_operador: Optional[str]
    id_recarga_anterior: Optional[str]
    litros_anterior: Optional[int]
    horometro_anterior: Optional[int]
    kilometro_anterior: Optional[int]
    fecha_anterior: Optional[datetime]
    
    # Referencias simples (pueden ser None)
    maquina: Optional[MaquinaRef]
    usuario: Optional[UsuarioRef]
    operador: Optional[UsuarioRef]
    obra: Optional[ObraRef]
    cliente: Optional[ClienteRef]
    recarga_anterior: Optional['Recarga']  # Puede ser None para evitar recursión
    usuario_ultima_modificacion: Optional[UsuarioRef]