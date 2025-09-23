from dataclasses import dataclass
from typing import Optional
from ..domain.repository import RecargaRepository
from ..domain.entity import Recarga

@dataclass
class GetRecargaInput:
    recarga_id: int

@dataclass
class GetRecargaOutput:
    data: Optional[Recarga]
    found: bool

class GetRecargaUseCase:
    def __init__(self, repo: RecargaRepository):
        self.repo = repo

    def execute(self, input_data: GetRecargaInput) -> GetRecargaOutput:
        recarga = self.repo.obtener_por_id(input_data.recarga_id)
        
        return GetRecargaOutput(
            data=recarga,
            found=recarga is not None
        )