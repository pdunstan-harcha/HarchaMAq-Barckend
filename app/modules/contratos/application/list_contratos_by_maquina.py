from dataclasses import dataclass
from typing import Sequence, Optional
from ..domain.entity import Contrato
from ..infrastructure.sqlalchemy_repository import SqlAlchemyContratoRepository

@dataclass
class ListContratosByMaquinaOutput:
    data: Sequence[Contrato]

class ListContratosByMaquinaUseCase:
    def __init__(self, repo: SqlAlchemyContratoRepository):
        self.repo = repo
        
    def execute(self, maquina_id: int) -> ListContratosByMaquinaOutput:
        return ListContratosByMaquinaOutput(data=self.repo.list_by_maquina(maquina_id))
