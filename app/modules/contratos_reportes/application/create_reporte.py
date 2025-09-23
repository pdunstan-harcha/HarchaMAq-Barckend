from dataclasses import dataclass
from ..domain.repository import ContratoReporteRepository
from ..domain.entity import ContratoReporte


@dataclass
class CreateContratoReporteInput:
    payload: dict

class CreateContratoReporteUseCase:
    def __init__(self, repo: ContratoReporteRepository):
        self.repo = repo
        
    def execute(self, input: CreateContratoReporteInput) -> ContratoReporte:
        return self.repo.create(input.payload)