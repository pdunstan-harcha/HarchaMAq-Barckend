from ..domain.repository import MaquinaRepository
from ..domain.entity import Maquina

class UpdateMaquinaUseCase:
    def __init__(self, repo: MaquinaRepository):
        self._repo = repo
    
    def execute(self, maquina: Maquina) -> Maquina:
        # Lógica de negocio para actualizar máquina
        # TODO: Implementar según reglas de negocio
        return self._repo.update(maquina)