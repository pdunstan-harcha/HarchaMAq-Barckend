from dataclasses import dataclass
from typing import Optional, Dict, Any
from ..domain.repository import ContratoReporteRepository
from ..domain.entity import ContratoReporte

@dataclass
class UpdateContratoReporteInput:
    reporte_id: int
    payload: Dict[str, Any]

@dataclass
class UpdateContratoReporteOutput:
    reporte: Optional[ContratoReporte]
    success: bool
    message: str

class UpdateContratoReporteUseCase:
    def __init__(self, repo: ContratoReporteRepository):
        self.repo = repo

    def execute(self, input_data: UpdateContratoReporteInput) -> UpdateContratoReporteOutput:
        try:
            # Verificar que el reporte existe
            existing = self.repo.obtener_por_id(input_data.reporte_id)
            if not existing:
                return UpdateContratoReporteOutput(
                    reporte=None,
                    success=False,
                    message="Reporte no encontrado"
                )

            # Actualizar el reporte
            updated = self.repo.actualizar(input_data.reporte_id, input_data.payload)
            
            if updated:
                return UpdateContratoReporteOutput(
                    reporte=updated,
                    success=True,
                    message="Reporte actualizado exitosamente"
                )
            else:
                return UpdateContratoReporteOutput(
                    reporte=None,
                    success=False,
                    message="Error al actualizar el reporte"
                )
        except Exception as e:
            return UpdateContratoReporteOutput(
                reporte=None,
                success=False,
                message=f"Error interno: {str(e)}"
            )
