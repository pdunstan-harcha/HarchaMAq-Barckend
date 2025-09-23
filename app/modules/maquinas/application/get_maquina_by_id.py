from ..domain.repository import MaquinaRepository
from ..domain.entity import Maquina

class GetMaquinaByIdUseCase:
    def __init__(self, repo: MaquinaRepository):
        self._repo = repo
    
    def execute(self, maquina_id: int) -> Maquina | None:
        # TODO: Implementar método get_by_id en el repositorio
        return self._repo.get_by_id(maquina_id)