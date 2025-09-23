from typing import Sequence
from app.models import Cliente as SACliente
from ..domain.entity import Cliente

def _to_domain(sa: SACliente) -> Cliente:
    """Convertir modelo SQLAlchemy a entidad de dominio"""
    return Cliente(
        id=sa.pkCliente,
        id_cliente=getattr(sa, "ID_CLIENTE", None),
        nombre=getattr(sa, "CLIENTE", None),
        rut=getattr(sa, "RUT", None)
    )

class SqlAlchemyClienteRepository:
    """Repositorio SQLAlchemy para clientes"""
    
    def list_all(self) -> Sequence[Cliente]:
        """Obtener todos los clientes ordenados por nombre"""
        sa_clientes = SACliente.query.order_by(SACliente.CLIENTE.asc()).all()
        return tuple(_to_domain(sa) for sa in sa_clientes)
