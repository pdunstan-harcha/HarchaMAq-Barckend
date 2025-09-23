from typing import Protocol, Sequence, Tuple, Optional, Dict, Any
from .entity import ContratoReporte

class ContratoReporteRepository(Protocol):
    """
    Protocol que define las operaciones del repositorio para contratos y reportes.
    """
    
    def list_paginated(
        self, 
        limit: int, 
        page: int, 
        search: Optional[str] = None,
        user_filter: Optional[int] = None
    ) -> Tuple[Sequence[ContratoReporte], int, int, int]:
        """Lista reportes paginados con búsqueda y filtro opcional por usuario."""
        ...
    
    def create(self, payload: dict) -> ContratoReporte:
        """Crea un nuevo reporte de contrato."""
        ...
    
    def obtener_por_id(self, reporte_id: int) -> Optional[ContratoReporte]:
        """Obtiene un reporte por su ID."""
        ...
    
    def actualizar(self, reporte_id: int, payload: dict) -> Optional[ContratoReporte]:
        """Actualiza un reporte existente."""
        ...
    
    def eliminar(self, reporte_id: int) -> bool:
        """Elimina un reporte por su ID."""
        ...
    
    def get_by_contract_and_date(
        self, 
        contract_id: str, 
        fecha_inicio: str,
        fecha_fin: Optional[str] = None
    ) -> Sequence[ContratoReporte]:
        """Obtiene reportes por contrato y rango de fechas."""
        ...
    
    def get_by_machine(
        self, 
        machine_id: str,
        limit: Optional[int] = None
    ) -> Sequence[ContratoReporte]:
        """Obtiene reportes por máquina."""
        ...
    
    def get_by_user(
        self, 
        user_id: int,
        limit: Optional[int] = None
    ) -> Sequence[ContratoReporte]:
        """Obtiene reportes por usuario."""
        ...
    
    def update_status(self, reporte_id: str, status: str) -> bool:
        """Actualiza el estado de un reporte."""
        ...
    
    def get_pending_reports(self, limit: Optional[int] = None) -> Sequence[ContratoReporte]:
        """Obtiene reportes pendientes de aprobación."""
        ...