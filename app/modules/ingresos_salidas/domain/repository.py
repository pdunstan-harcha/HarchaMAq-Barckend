from typing import Protocol, Sequence, Optional
from .entity import IngresoSalida

class PaginationParams:
    def __init__(self, page: int = 1, per_page: int = 20, search: str = None):
        self.page = max(1, page)
        self.per_page = min(100, max(10, per_page))
        self.search = search.strip() if search else None

class PaginatedResult:
    def __init__(self, data: Sequence[IngresoSalida], total: int, page: int, per_page: int):
        self.data = data
        self.total = total
        self.page = page
        self.per_page = per_page
        self.total_pages = (total + per_page - 1) // per_page
        self.has_next = page < self.total_pages
        self.has_prev = page > 1

class IngresoSalidaRepository(Protocol):
    def listar_paginado(self, params: PaginationParams) -> PaginatedResult:
        ...
    
    def obtener_por_id(self, ingreso_salida_id: int) -> Optional[IngresoSalida]:
        ...
    
    def crear(self, payload: dict) -> IngresoSalida:
        ...
    
    def actualizar(self, ingreso_salida_id: int, payload: dict) -> Optional[IngresoSalida]:
        ...
    
    def eliminar(self, ingreso_salida_id: int) -> bool:
        ...
    
    def obtener_ultimo_por_maquina(self, maquina_id: int) -> Optional[IngresoSalida]:
        """Obtener el último ingreso/salida de una máquina específica"""
        ...