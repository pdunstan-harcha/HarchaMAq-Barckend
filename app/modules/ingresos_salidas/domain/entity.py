from dataclasses import dataclass
from typing import Optional
from datetime import datetime, time
from .refs import MaquinaRef, UsuarioRef

@dataclass(frozen=True)
class IngresoSalida:

    id: int  
    codigo: Optional[str] 
    id_maquina: Optional[str] 
    fechahora: Optional[datetime] 
    ingreso_salida: Optional[str]  
    id_ultimo_is: Optional[str] 
    fechahora_ultimo: Optional[datetime]  
    tiempo: Optional[time]  
    estado_maquina: Optional[str] 
    control1: Optional[int]  
    editar_fecha: Optional[str]  
    fecha_editada: Optional[datetime]  
    usuario_id: Optional[str]
    observaciones: Optional[str]  # Agregado campo faltante
    
    # Referencias a otras entidades (sin valores por defecto)
    maquina: Optional[MaquinaRef]
    usuario: Optional[UsuarioRef]
    ingreso_salida_anterior: Optional['IngresoSalida']
    
    # Campos adicionales para el frontend (con valores por defecto al final)
    tiempo_formateado: Optional[str] = None
    movimiento_anterior_texto: Optional[str] = None
    puede_modificar_fecha: bool = False  