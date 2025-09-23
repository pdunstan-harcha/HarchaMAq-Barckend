from dataclasses import dataclass
from ..domain.repository import RecargaRepository

@dataclass
class DeleteRecargaInput:
    recarga_id: int

@dataclass
class DeleteRecargaOutput:
    deleted: bool
    message: str = ""

class DeleteRecargaUseCase:
    def __init__(self, repo: RecargaRepository):
        self.repo = repo

    def execute(self, input_data: DeleteRecargaInput) -> DeleteRecargaOutput:
        # Verificar que existe
        existing = self.repo.obtener_por_id(input_data.recarga_id)
        if not existing:
            return DeleteRecargaOutput(
                deleted=False, 
                message=f"Recarga {input_data.recarga_id} no encontrada"
            )
        
        # Validación de negocio: ¿Se puede eliminar?
        # Por ejemplo, no eliminar si tiene recargas posteriores que la referencian
        # Esta lógica depende de las reglas de negocio específicas
        
        # Eliminar en el repositorio
        success = self.repo.eliminar(input_data.recarga_id)
        
        return DeleteRecargaOutput(
            deleted=success,
            message="Recarga eliminada exitosamente" if success else "Error al eliminar la recarga"
        )