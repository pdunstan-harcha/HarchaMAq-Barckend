from dataclasses import dataclass
from typing import Optional
from ..domain.repository import IngresoSalidaRepository
from ..domain.entity import IngresoSalida

@dataclass
class GetIngresoSalidaInput:
    ingreso_salida_id: int

@dataclass
class GetIngresoSalidaOutput:
    data: Optional[IngresoSalida]
    found: bool

class GetIngresoSalidaUseCase:
    def __init__(self, repo: IngresoSalidaRepository):
        self.repo = repo

    def execute(self, input_data: GetIngresoSalidaInput) -> GetIngresoSalidaOutput:
        ingreso_salida = self.repo.obtener_por_id(input_data.ingreso_salida_id)
        
        return GetIngresoSalidaOutput(
            data=ingreso_salida,
            found=ingreso_salida is not None
        )