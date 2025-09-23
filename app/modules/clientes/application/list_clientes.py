from dataclasses import dataclass
from typing import Sequence
from ..domain.entity import Cliente
from ..infrastructure.sqlalchemy_repository import SqlAlchemyClienteRepository

@dataclass
class ListClientesOutput:
    data: Sequence[Cliente]

class ListClientesUseCase:
    def __init__(self, repo: SqlAlchemyClienteRepository):
        self.repo = repo
        
    def execute(self) -> ListClientesOutput:
        return ListClientesOutput(data=self.repo.list_all())
