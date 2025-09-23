from dataclasses import dataclass
from typing import Optional
from ..domain.repository import IngresoSalidaRepository
from ..domain.entity import IngresoSalida

@dataclass
class UpdateIngresoSalidaInput:
    ingreso_salida_id: int
    payload: dict

@dataclass
class UpdateIngresoSalidaOutput:
    data: Optional[IngresoSalida]
    updated: bool
    message: str = ""

class UpdateIngresoSalidaUseCase:
    def __init__(self, repo: IngresoSalidaRepository):
        self.repo = repo

    def execute(self, input_data: UpdateIngresoSalidaInput) -> UpdateIngresoSalidaOutput:
        # Verificar que existe
        existing = self.repo.obtener_por_id(input_data.ingreso_salida_id)
        if not existing:
            return UpdateIngresoSalidaOutput(
                data=None, 
                updated=False, 
                message=f"Ingreso/Salida {input_data.ingreso_salida_id} no encontrado"
            )
        
        # Validaciones básicas
        payload = input_data.payload
        
        # Validar INGRESO_SALIDA si se está actualizando
        if 'INGRESO_SALIDA' in payload:
            tipo_movimiento = payload['INGRESO_SALIDA'].upper()
            if tipo_movimiento not in ['INGRESO', 'SALIDA']:
                raise ValueError("INGRESO_SALIDA debe ser 'INGRESO' o 'SALIDA'")
        
        # Actualizar en el repositorio
        updated_is = self.repo.actualizar(input_data.ingreso_salida_id, payload)
        
        return UpdateIngresoSalidaOutput(
            data=updated_is,
            updated=updated_is is not None,
            message="Ingreso/Salida actualizado exitosamente" if updated_is else "Error al actualizar"
        )