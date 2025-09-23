from dataclasses import dataclass
from typing import Sequence
from ..domain.repository import IngresoSalidaRepository, PaginationParams, PaginatedResult
from ..domain.entity import IngresoSalida

@dataclass
class ListIngresosSalidasInput:
    page: int = 1
    per_page: int = 20
    search: str = None
    maquina_id: int = None  # Filtro opcional por máquina

@dataclass
class ListIngresosSalidasOutput:
    data: Sequence[IngresoSalida]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

class ListIngresosSalidasUseCase:
    def __init__(self, repo: IngresoSalidaRepository):
        self.repo = repo

    def execute(self, input_data: ListIngresosSalidasInput = None) -> ListIngresosSalidasOutput:
        if input_data is None:
            input_data = ListIngresosSalidasInput()
            
        params = PaginationParams(
            page=input_data.page,
            per_page=input_data.per_page,
            search=input_data.search
        )
        
        result = self.repo.listar_paginado(params)
        
        return ListIngresosSalidasOutput(
            data=result.data,
            total=result.total,
            page=result.page,
            per_page=result.per_page,
            total_pages=result.total_pages,
            has_next=result.has_next,
            has_prev=result.has_prev
        )