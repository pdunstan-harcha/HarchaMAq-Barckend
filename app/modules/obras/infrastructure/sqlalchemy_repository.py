from typing import Sequence
from app.models import Obra as SAObra
from ..domain.entity import Obra

def _to_domain(sa: SAObra) -> Obra:
    """Convertir modelo SQLAlchemy a entidad de dominio"""
    return Obra(
        id=sa.pkObra,
        id_obra=getattr(sa, "ID_OBRA", None),
        nombre=getattr(sa, "OBRA", None)
    )

class SqlAlchemyObraRepository:
    """Repositorio SQLAlchemy para obras"""
    
    def list_all(self) -> Sequence[Obra]:
        """Obtener todas las obras ordenadas por nombre"""
        sa_obras = SAObra.query.order_by(SAObra.OBRA.asc()).all()
        return tuple(_to_domain(sa) for sa in sa_obras)
