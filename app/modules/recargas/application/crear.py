from dataclasses import dataclass
from ..domain.repository import RecargaRepository
from ..domain.entity import Recarga

@dataclass
class CreateRecargaInput:
    payload: dict

class CreateRecargaUseCase:
    def __init__(self, repo: RecargaRepository):
        self.repo = repo

    def execute(self, input_data: CreateRecargaInput) -> Recarga:
        # Validaciones básicas
        payload = input_data.payload
        
        if not payload.get('pkMaquina'):
            raise ValueError("pkMaquina es requerido")
            
        if not payload.get('pkUsuario'):
            raise ValueError("pkUsuario es requerido")
            
        if not payload.get('LITROS') or payload.get('LITROS') <= 0:
            raise ValueError("LITROS debe ser mayor a 0")
        
        return self.repo.crear(payload)