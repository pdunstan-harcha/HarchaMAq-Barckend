from dataclasses import dataclass
from typing import Optional
from ..domain.repository import RecargaRepository
from ..domain.entity import Recarga

@dataclass
class UpdateRecargaInput:
    recarga_id: int
    payload: dict

@dataclass
class UpdateRecargaOutput:
    data: Optional[Recarga]
    updated: bool
    message: str = ""

class UpdateRecargaUseCase:
    def __init__(self, repo: RecargaRepository):
        self.repo = repo

    def execute(self, input_data: UpdateRecargaInput) -> UpdateRecargaOutput:
        # Verificar que existe
        existing = self.repo.obtener_por_id(input_data.recarga_id)
        if not existing:
            return UpdateRecargaOutput(
                data=None, 
                updated=False, 
                message=f"Recarga {input_data.recarga_id} no encontrada"
            )
        
        # Validaciones básicas
        payload = input_data.payload
        
        # Validar LITROS si se está actualizando
        if 'LITROS' in payload:
            litros = payload['LITROS']
            if litros is not None and (not isinstance(litros, (int, float)) or litros <= 0):
                raise ValueError("LITROS debe ser un número mayor a 0")
        
        # Validar ODOMETRO si se está actualizando
        if 'ODOMETRO' in payload:
            odometro = payload['ODOMETRO']
            if odometro is not None and (not isinstance(odometro, (int, float)) or odometro < 0):
                raise ValueError("ODOMETRO debe ser un número mayor o igual a 0")
        
        # Validar KILOMETROS si se está actualizando
        if 'KILOMETROS' in payload:
            kilometros = payload['KILOMETROS']
            if kilometros is not None and (not isinstance(kilometros, (int, float)) or kilometros < 0):
                raise ValueError("KILOMETROS debe ser un número mayor o igual a 0")
        
        # Actualizar en el repositorio
        updated_recarga = self.repo.actualizar(input_data.recarga_id, payload)
        
        return UpdateRecargaOutput(
            data=updated_recarga,
            updated=updated_recarga is not None,
            message="Recarga actualizada exitosamente" if updated_recarga else "Error al actualizar la recarga"
        )