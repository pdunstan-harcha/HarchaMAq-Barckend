from dataclasses import dataclass
from typing import Sequence, Optional
from ..domain.entity import Contrato
from ..infrastructure.sqlalchemy_repository import SqlAlchemyContratoRepository

@dataclass
class ListContratosOutput:
    data: Sequence[Contrato]

class ListContratosUseCase:
    def __init__(self, repo: SqlAlchemyContratoRepository):
        self.repo = repo
        
    def execute(self, maquina_id: Optional[int] = None) -> ListContratosOutput:
        if maquina_id:
            data = self.repo.list_by_maquina(maquina_id)
        else:
            data = self.repo.list_all()
        return ListContratosOutput(data=data)
