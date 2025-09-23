from typing import Protocol, Sequence, Optional
from .entity import Recarga

class PaginationParams:
    def __init__(self, page: int = 1, per_page: int = 20, search: str = None, user_filter: int = None):
        self.page = max(1, page)  # Mínimo página 1
        self.per_page = min(100, max(10, per_page))  # Entre 10 y 100 por página
        self.search = search.strip() if search else None
        self.user_filter = user_filter

class PaginatedResult:
    def __init__(self, data: Sequence[Recarga], total: int, page: int, per_page: int):
        self.data = data
        self.total = total
        self.page = page
        self.per_page = per_page
        self.total_pages = (total + per_page - 1) // per_page  # Calcular total de páginas
        self.has_next = page < self.total_pages
        self.has_prev = page > 1

class RecargaRepository(Protocol):
    def listar_paginado(self, params: PaginationParams) -> PaginatedResult:
        ...
    
    def obtener_por_id(self, recarga_id: int) -> Optional[Recarga]:
        ...
    
    def crear(self, payload: dict) -> Recarga:
        ...
    
    def actualizar(self, recarga_id: int, payload: dict) -> Optional[Recarga]:
        ...
    
    def eliminar(self, recarga_id: int) -> bool:
        ...