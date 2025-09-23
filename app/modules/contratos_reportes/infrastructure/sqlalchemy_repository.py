from typing import Sequence, Tuple
from sqlalchemy.orm import joinedload
from app.models import ContratoReporte as SAContratoReporte, Maquina as SAMaquina, User as SAUser, Contrato as SAContrato
from app import db
from ..domain.entity import ContratoReporte
from ..domain.refs import ContratoRef, MaquinaRef, UsuarioRef
from ..domain.repository import ContratoReporteRepository


def _contrato_ref(contrato: SAContrato | None) -> ContratoRef | None:
    if not contrato:
        return None
    return ContratoRef(
        id=contrato.pkContrato,
        nombre=contrato.CONTRATO,
    )


def _maquina_ref(maquina: SAMaquina | None) -> MaquinaRef | None:
    if not maquina:
        return None
    return MaquinaRef(
        id=maquina.pkMaquina,
        nombre=maquina.MAQUINA,
    )


def _usuario_ref(usuario: SAUser | None) -> UsuarioRef | None:
    if not usuario:
        return None
    return UsuarioRef(
        id=usuario.pkUsuario,
        usuario=usuario.NOMBREUSUARIO,
    )


def _to_domain(row: SAContratoReporte) -> ContratoReporte:
    return ContratoReporte(
        id=row.pkReporte,
        codigo=row.ID_REPORTE,
        fecha_inicio=row.FECHAHORA_INICIO,
        descripcion=row.Descripcion,
        maquina_txt=row.MAQUINA_TXT,
        contrato_txt=row.CONTRATO_TXT,
        usuario_txt=row.USUARIO_TXT,
        contrato=_contrato_ref(getattr(row, "contrato", None)),
        maquina=_maquina_ref(getattr(row, "maquina", None)),
        usuario=_usuario_ref(getattr(row, "usuario", None)),
    )


class SqlAlchemyContratoReporteRepository(ContratoReporteRepository):
    def list_paginated(self, limit: int, page: int, search: str = "", user_filter: int = None) -> Tuple[Sequence[ContratoReporte], int, int, int]:
        query = (
            SAContratoReporte.query
            .options(
                joinedload(SAContratoReporte.contrato),
                joinedload(SAContratoReporte.maquina),
                joinedload(SAContratoReporte.usuario),
            )
        )
        
        # Filtro por usuario si se especifica
        if user_filter is not None:
            query = query.filter(SAContratoReporte.pkUsuario == user_filter)
        
        # Filtro de búsqueda
        if search:
            like = f"%{search}%"
            query = query.filter(
                (SAContratoReporte.ID_REPORTE.like(like)) |
                (SAContratoReporte.MAQUINA_TXT.like(like)) |
                (SAContratoReporte.CONTRATO_TXT.like(like)) |
                (SAContratoReporte.USUARIO_TXT.like(like)) |
                (SAContratoReporte.Descripcion.like(like)) |
                (SAContratoReporte.OBRA_TXT.like(like))
            )
        
        total_records = query.count()
        total_pages = (total_records + limit - 1) // limit
        rows = (
            query.order_by(SAContratoReporte.FECHAHORA_INICIO.desc())
            .offset((page-1)*limit)
            .limit(limit)
            .all()
        )
        return [_to_domain(row) for row in rows], page, total_pages, total_records

    def create(self, payload:dict) -> ContratoReporte:
        report = SAContratoReporte(
            ID_REPORTE=payload.get("ID_REPORTE"),
            ID2_REPORTE=payload.get("ID2_REPORTE", 999),
            ID_CONTRATO=payload.get("ID_CONTRATO", "99"),
            pkContrato=payload.get("pkContrato", 99),
            ID_MAQUINA=payload.get("ID_MAQUINA", "m000099"),
            pkMaquina=payload.get("pkMaquina", 99),
            FECHAHORA_INICIO=payload.get("FECHAHORA_INICIO"),
            USUARIO_ID=payload.get("USUARIO_ID", "usuario_test"),
            pkUsuario=payload.get("pkUsuario", 1),
            ODOMETRO_INICIAL=payload.get("ODOMETRO_INICIAL", 1000),
            ODOMETRO_FINAL=payload.get("ODOMETRO_FINAL", 1010),
            HORAS_TRABAJADAS=payload.get("HORAS_TRABAJADAS", 8),
            Descripcion=payload.get("Descripcion"),
            Observaciones=payload.get("Observaciones"),
            FOTO1=payload.get("FOTO1"),
            FOTO2=payload.get("FOTO2"),
            CONTRATO_TXT=payload.get("CONTRATO_TXT"),
            CLIENTE_TXT=payload.get("CLIENTE_TXT"),
            MAQUINA_TXT=payload.get("MAQUINA_TXT"),
            USUARIO_TXT=payload.get("USUARIO_TXT"),
            HORAS_MINIMAS=payload.get("HORAS_MINIMAS", 8),
            FECHAHORA_FIN=payload.get("FECHAHORA_FIN"),
            OBRA_TXT=payload.get("OBRA_TXT"),
            KM_FINAL=payload.get("KM_FINAL"),
            KILOMETROS=payload.get("KILOMETROS"),
            MT3=payload.get("MT3"),
            VUELTAS=payload.get("VUELTAS"),
            KM_INICIO=payload.get("KM_INICIO"),
            MAQUINA_TIPO=payload.get("MAQUINA_TIPO"),
            MAQUINA_MARCA=payload.get("MAQUINA_MARCA"),
            MAQUINA_MODELO=payload.get("MAQUINA_MODELO"),
            HORA_INI=payload.get("HORA_INI"),
            HORA_FIN=payload.get("HORA_FIN"),
            Control=payload.get("Control", 0),
            PDF_Reporte=payload.get("PDF_Reporte"),
            Estado_Reporte=payload.get("Estado_Reporte"),
            ID3_REPORTE=payload.get("ID3_REPORTE", 999),
            Reporte_Pane=payload.get("Reporte_Pane"),
            Estado_Pane=payload.get("Estado_Pane"),
            USUARIO_ID_UltimaModificacion=payload.get("USUARIO_ID_UltimaModificacion"),
            pkUsuario_UltimaModificacion=payload.get("pkUsuario_UltimaModificacion", 1)
        )
        db.session.add(report)
        db.session.commit()
        db.session.refresh(report)
        return _to_domain(report)

    def obtener_por_id(self, reporte_id: int) -> ContratoReporte | None:
        row = (
            SAContratoReporte.query
            .options(
                joinedload(SAContratoReporte.contrato),
                joinedload(SAContratoReporte.maquina),
                joinedload(SAContratoReporte.usuario),
            )
            .filter(SAContratoReporte.pkReporte == reporte_id)
            .first()
        )
        return _to_domain(row) if row else None

    def actualizar(self, reporte_id: int, payload: dict) -> ContratoReporte | None:
        report = SAContratoReporte.query.filter(SAContratoReporte.pkReporte == reporte_id).first()
        if not report:
            return None

        # Actualizar solo los campos que vienen en el payload
        for field, value in payload.items():
            if hasattr(report, field):
                setattr(report, field, value)

        db.session.commit()
        db.session.refresh(report)
        
        # Recargar con las relaciones
        report_with_relations = (
            SAContratoReporte.query
            .options(
                joinedload(SAContratoReporte.contrato),
                joinedload(SAContratoReporte.maquina),
                joinedload(SAContratoReporte.usuario),
            )
            .filter(SAContratoReporte.pkReporte == reporte_id)
            .first()
        )
        return _to_domain(report_with_relations)

    def eliminar(self, reporte_id: int) -> bool:
        report = SAContratoReporte.query.filter(SAContratoReporte.pkReporte == reporte_id).first()
        if not report:
            return False

        db.session.delete(report)
        db.session.commit()
        return True