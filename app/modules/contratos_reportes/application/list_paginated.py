from dataclasses import dataclass
from typing import Sequence
from ..domain.repository import ContratoReporteRepository
from ..domain.entity import ContratoReporte

@dataclass
class ListContratosReportesOutput:
    data: Sequence[ContratoReporte]
    page: int
    total_pages: int
    total_records: int


class ListContratosReportesUseCase:
    def __init__(self, repo: ContratoReporteRepository):
        self.repo = repo
        
    def execute(self, limit: int, page: int, search: str, user_filter: int = None) -> ListContratosReportesOutput:
        data, p, total_pages, total_records = self.repo.list_paginated(limit, page, search, user_filter)
        return ListContratosReportesOutput(data=data, page=p, total_pages=total_pages, total_records=total_records)