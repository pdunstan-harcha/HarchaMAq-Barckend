from dataclasses import dataclass
from ..domain.repository import IngresoSalidaRepository

@dataclass
class DeleteIngresoSalidaInput:
    ingreso_salida_id: int

@dataclass
class DeleteIngresoSalidaOutput:
    deleted: bool
    message: str = ""

class DeleteIngresoSalidaUseCase:
    def __init__(self, repo: IngresoSalidaRepository):
        self.repo = repo

    def execute(self, input_data: DeleteIngresoSalidaInput) -> DeleteIngresoSalidaOutput:
        # Verificar que existe
        existing = self.repo.obtener_por_id(input_data.ingreso_salida_id)
        if not existing:
            return DeleteIngresoSalidaOutput(
                deleted=False, 
                message=f"Ingreso/Salida {input_data.ingreso_salida_id} no encontrado"
            )
        
        # Eliminar en el repositorio
        success = self.repo.eliminar(input_data.ingreso_salida_id)
        
        return DeleteIngresoSalidaOutput(
            deleted=success,
            message="Ingreso/Salida eliminado exitosamente" if success else "Error al eliminar"
        )