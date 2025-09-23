from dataclasses import dataclass
from typing import Sequence
from ..domain.repository import MaquinaRepository
from ..domain.entity import Maquina


@dataclass
class ListMaquinasOutput:
    data: Sequence[Maquina]
    
    
class ListMaquinasUseCase:
    def __init__(self, repo: MaquinaRepository):
        self.repo = repo
        
    def execute(self) -> ListMaquinasOutput:
        return ListMaquinasOutput(data=self.repo.listar())