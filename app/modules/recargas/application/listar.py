from dataclasses import dataclass
from typing import Sequence
from ..domain.repository import RecargaRepository, PaginationParams, PaginatedResult
from ..domain.entity import Recarga

@dataclass
class ListRecargasInput:
    page: int = 1
    per_page: int = 100
    search: str = None
    user_filter: int = None

@dataclass
class ListRecargasOutput:
    data: Sequence[Recarga]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

class ListRecargasUseCase:
    def __init__(self, repo: RecargaRepository):
        self.repo = repo

    def execute(self, input_data: ListRecargasInput = None) -> ListRecargasOutput:
        if input_data is None:
            input_data = ListRecargasInput()
            
        params = PaginationParams(
            page=input_data.page,
            per_page=input_data.per_page,
            search=input_data.search,
            user_filter=input_data.user_filter
        )
        
        result = self.repo.listar_paginado(params)
        
        return ListRecargasOutput(
            data=result.data,
            total=result.total,
            page=result.page,
            per_page=result.per_page,
            total_pages=result.total_pages,
            has_next=result.has_next,
            has_prev=result.has_prev
        )