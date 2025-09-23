from typing import Sequence, Optional
from sqlalchemy.orm import joinedload
from app.models import Contrato as SAContrato, Maquina as SAMaquina, Cliente as SACliente, Obra as SAObra
from app import db
from ..domain.entity import Contrato

def _to_domain(sa: SAContrato, maquina_nombre: str = None, cliente_nombre: str = None, obra_nombre: str = None) -> Contrato:
    """Convertir modelo SQLAlchemy a entidad de dominio"""
    return Contrato(
        id=sa.pkContrato,
        id_contrato=getattr(sa, "ID_CONTRATO", None),
        nombre=getattr(sa, "CONTRATO", None),
        pk_maquina=getattr(sa, "pkMaquina", None),
        pk_cliente=getattr(sa, "pkCliente", None),
        pk_obra=getattr(sa, "pkObra", None),
        fecha_inicio=getattr(sa, "FECHA_INICIO", None),
        estado=getattr(sa, "Estado", None),
        maquina_nombre=maquina_nombre,
        cliente_nombre=cliente_nombre,
        obra_nombre=obra_nombre
    )

class SqlAlchemyContratoRepository:
    """Repositorio SQLAlchemy para contratos"""
    
    def list_by_maquina(self, maquina_id: int) -> Sequence[Contrato]:
        """Obtener contratos filtrados por máquina con datos relacionados"""
        query = db.session.query(
            SAContrato,
            SAMaquina.MAQUINA,
            SACliente.CLIENTE,
            SAObra.OBRA
        ).join(
            SAMaquina, SAContrato.pkMaquina == SAMaquina.pkMaquina
        ).join(
            SACliente, SAContrato.pkCliente == SACliente.pkCliente
        ).join(
            SAObra, SAContrato.pkObra == SAObra.pkObra
        ).filter(
            SAContrato.pkMaquina == maquina_id
        ).order_by(
            SAContrato.FECHA_INICIO.desc()
        )
        
        results = query.all()
        return tuple(
            _to_domain(contrato, maquina_nombre, cliente_nombre, obra_nombre)
            for contrato, maquina_nombre, cliente_nombre, obra_nombre in results
        )
    
    def list_all(self) -> Sequence[Contrato]:
        """Obtener todos los contratos con datos relacionados"""
        query = db.session.query(
            SAContrato,
            SAMaquina.MAQUINA,
            SACliente.CLIENTE,
            SAObra.OBRA
        ).join(
            SAMaquina, SAContrato.pkMaquina == SAMaquina.pkMaquina
        ).join(
            SACliente, SAContrato.pkCliente == SACliente.pkCliente
        ).join(
            SAObra, SAContrato.pkObra == SAObra.pkObra
        ).order_by(
            SAContrato.FECHA_INICIO.desc()
        )
        
        results = query.all()
        return tuple(
            _to_domain(contrato, maquina_nombre, cliente_nombre, obra_nombre)
            for contrato, maquina_nombre, cliente_nombre, obra_nombre in results
        )
