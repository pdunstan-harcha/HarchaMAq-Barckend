from dataclasses import dataclass
from ..domain.repository import ContratoReporteRepository

@dataclass
class DeleteContratoReporteInput:
    reporte_id: int

@dataclass
class DeleteContratoReporteOutput:
    success: bool
    message: str

class DeleteContratoReporteUseCase:
    def __init__(self, repo: ContratoReporteRepository):
        self.repo = repo

    def execute(self, input_data: DeleteContratoReporteInput) -> DeleteContratoReporteOutput:
        try:
            # Verificar que el reporte existe
            existing = self.repo.obtener_por_id(input_data.reporte_id)
            if not existing:
                return DeleteContratoReporteOutput(
                    success=False,
                    message="Reporte no encontrado"
                )

            # Eliminar el reporte
            success = self.repo.eliminar(input_data.reporte_id)
            
            if success:
                return DeleteContratoReporteOutput(
                    success=True,
                    message="Reporte eliminado exitosamente"
                )
            else:
                return DeleteContratoReporteOutput(
                    success=False,
                    message="Error al eliminar el reporte"
                )
        except Exception as e:
            return DeleteContratoReporteOutput(
                success=False,
                message=f"Error interno: {str(e)}"
            )
