from ..domain.repository import MaquinaRepository
from ..domain.operador_ref import OperadorRef

class GetOperadoresByMaquinaIdUseCase:
    def __init__(self, repo: MaquinaRepository):
        self.repo = repo
    
    def execute(self, maquina_id: int) -> list[OperadorRef]:
        operadores = self.repo.get_operadores_by_maquina_id(maquina_id)
        return list(operadores) if operadores else []