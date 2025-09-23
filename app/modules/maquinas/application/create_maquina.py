from dataclasses import dataclass
from ..domain.repository import MaquinaRepository
from ..domain.entity import Maquina

@dataclass
class CreateMaquinaCommand:
    nombre: str
    marca: str
    modelo: str
    patente: str | None = None
    estado: str | None = None

class CreateMaquinaUseCase:
    def __init__(self, repo: MaquinaRepository):
        self._repo = repo
    
    def execute(self, command: CreateMaquinaCommand) -> Maquina:
        # Lógica de negocio para crear máquina
        # TODO: Implementar según reglas de negocio
        pass