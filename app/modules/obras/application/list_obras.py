from dataclasses import dataclass
from typing import Sequence
from ..domain.entity import Obra
from ..infrastructure.sqlalchemy_repository import SqlAlchemyObraRepository

@dataclass
class ListObrasOutput:
    data: Sequence[Obra]

class ListObrasUseCase:
    def __init__(self, repo: SqlAlchemyObraRepository):
        self.repo = repo
        
    def execute(self) -> ListObrasOutput:
        return ListObrasOutput(data=self.repo.list_all())
