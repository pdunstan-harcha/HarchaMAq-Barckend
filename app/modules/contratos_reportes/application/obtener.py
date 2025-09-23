from dataclasses import dataclass
from typing import Optional
from ..domain.repository import ContratoReporteRepository
from ..domain.entity import ContratoReporte

@dataclass
class GetContratoReporteInput:
    reporte_id: int

@dataclass
class GetContratoReporteOutput:
    reporte: Optional[ContratoReporte]

class GetContratoReporteUseCase:
    def __init__(self, repo: ContratoReporteRepository):
        self.repo = repo

    def execute(self, input_data: GetContratoReporteInput) -> GetContratoReporteOutput:
        reporte = self.repo.obtener_por_id(input_data.reporte_id)
        return GetContratoReporteOutput(reporte=reporte)
