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

    # Campos de odómetro y horas
    odometro_inicial: Optional[int] = None
    odometro_final: Optional[int] = None
    horas_trabajadas: Optional[int] = None
    horas_minimas: Optional[int] = None

    # Campos de kilómetros
    km_inicio: Optional[int] = None
    km_final: Optional[int] = None
    kilometros: Optional[int] = None

    # Otros campos importantes
    observaciones: Optional[str] = None
    reporte_pane: Optional[str] = None
    estado_reporte: Optional[str] = None
    obra_txt: Optional[str] = None
    cliente_txt: Optional[str] = None

    # Campos adicionales
    fechahora_fin: Optional[str] = None  # Es String en la BD
    mt3: Optional[int] = None
    vueltas: Optional[int] = None
    hora_ini: Optional[str] = None
    hora_fin: Optional[str] = None
    foto1: Optional[str] = None
    foto2: Optional[str] = None

    # Campos de máquina
    maquina_tipo: Optional[str] = None
    maquina_marca: Optional[str] = None
    maquina_modelo: Optional[str] = None
    id_maquina: Optional[str] = None

    # Campos de contrato
    id_contrato: Optional[str] = None

    # Campos de usuario
    usuario_id: Optional[str] = None

    # Referencias
    contrato: Optional[ContratoRef] = None
    maquina: Optional[MaquinaRef] = None
    usuario: Optional[UsuarioRef] = None