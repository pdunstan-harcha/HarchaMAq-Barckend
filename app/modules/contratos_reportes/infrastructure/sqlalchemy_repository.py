from typing import Sequence, Tuple
from sqlalchemy.orm import joinedload
from app.models import (
    ContratoReporte as SAContratoReporte,
    Maquina as SAMaquina,
    User as SAUser,
    Contrato as SAContrato,
    Obra as SAObra,
    Cliente as SACliente
)
from app import db
from ..domain.entity import ContratoReporte
from ..domain.refs import ContratoRef, MaquinaRef, UsuarioRef
from ..domain.repository import ContratoReporteRepository


def _contrato_ref(contrato: SAContrato | None, obra_txt: str = None, cliente_txt: str = None) -> ContratoRef | None:
    if not contrato:
        return None
    return ContratoRef(
        id=contrato.pkContrato,
        nombre=contrato.CONTRATO,
        obra_txt=obra_txt,
        cliente_txt=cliente_txt,
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

        # Campos de odómetro y horas
        odometro_inicial=row.ODOMETRO_INICIAL,
        odometro_final=row.ODOMETRO_FINAL,
        horas_trabajadas=row.HORAS_TRABAJADAS,
        horas_minimas=row.HORAS_MINIMAS,

        # Campos de kilómetros
        km_inicio=row.KM_INICIO,
        km_final=row.KM_FINAL,
        kilometros=row.KILOMETROS,

        # Otros campos importantes
        observaciones=row.Observaciones,
        reporte_pane=row.Reporte_Pane,
        estado_reporte=row.Estado_Reporte,
        obra_txt=row.OBRA_TXT,
        cliente_txt=row.CLIENTE_TXT,

        # Campos adicionales
        fechahora_fin=row.FECHAHORA_FIN,
        mt3=row.MT3,
        vueltas=row.VUELTAS,
        hora_ini=row.HORA_INI,
        hora_fin=row.HORA_FIN,
        foto1=row.FOTO1,
        foto2=row.FOTO2,

        # Campos de máquina
        maquina_tipo=row.MAQUINA_TIPO,
        maquina_marca=row.MAQUINA_MARCA,
        maquina_modelo=row.MAQUINA_MODELO,
        id_maquina=row.ID_MAQUINA,

        # Campos de contrato
        id_contrato=row.ID_CONTRATO,

        # Campos de usuario
        usuario_id=row.USUARIO_ID,

        # Referencias
        contrato=_contrato_ref(getattr(row, "contrato", None), row.OBRA_TXT, row.CLIENTE_TXT),
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

    def create(self, payload: dict) -> ContratoReporte:
        # ✅ PASO 1: Obtener datos relacionados vía JOINs

        # Obtener máquina
        pk_maquina = payload.get("pkMaquina")
        maquina = SAMaquina.query.get(pk_maquina) if pk_maquina else None

        # Obtener contrato con sus relaciones
        pk_contrato = payload.get("pkContrato")
        contrato = None
        if pk_contrato:
            contrato = (
                SAContrato.query
                .options(
                    joinedload(SAContrato.obra),
                    joinedload(SAContrato.cliente)
                )
                .filter(SAContrato.pkContrato == pk_contrato)
                .first()
            )

        # Obtener usuario
        pk_usuario = payload.get("pkUsuario")
        usuario = SAUser.query.get(pk_usuario) if pk_usuario else None

        # ✅ PASO 2: Mapear payload del frontend a campos de BD
        # Mapeo de nombres del frontend → BD
        fecha_reporte = payload.get("FECHA_REPORTE") or payload.get("FECHAHORA_INICIO")
        trabajo_realizado = payload.get("TRABAJO_REALIZADO") or payload.get("Descripcion")
        observaciones = payload.get("OBSERVACIONES") or payload.get("Observaciones")
        incidente = payload.get("INCIDENTE") or payload.get("Reporte_Pane")
        km_inicial = payload.get("KM_INICIAL") or payload.get("KM_INICIO")
        estado_reporte = payload.get("ESTADO_REPORTE") or payload.get("Estado_Reporte", "Correcto")

        # ✅ PASO 3: Crear reporte con datos automáticos + payload
        report = SAContratoReporte(
            ID_REPORTE=payload.get("ID_REPORTE"),

            # Datos de la máquina (automáticos vía JOIN)
            pkMaquina=pk_maquina,
            ID_MAQUINA=maquina.ID_MAQUINA if maquina else None,
            MAQUINA_TXT=maquina.MAQUINA if maquina else payload.get("MAQUINA"),
            MAQUINA_TIPO=getattr(maquina, "TIPO", None) if maquina else None,
            MAQUINA_MARCA=maquina.MARCA if maquina else None,
            MAQUINA_MODELO=maquina.MODELO if maquina else None,

            # Datos del contrato (automáticos vía JOIN)
            pkContrato=pk_contrato,
            ID_CONTRATO=contrato.ID_CONTRATO if contrato else None,
            CONTRATO_TXT=contrato.CONTRATO if contrato else payload.get("CONTRATO"),
            CLIENTE_TXT=contrato.cliente.CLIENTE if (contrato and contrato.cliente) else None,
            OBRA_TXT=contrato.obra.OBRA if (contrato and contrato.obra) else None,

            # Datos del usuario (automáticos vía JOIN)
            pkUsuario=pk_usuario,
            USUARIO_ID=usuario.USUARIO_ID if usuario else None,
            USUARIO_TXT=f"{usuario.NOMBRE} {usuario.APELLIDOS}".strip() if usuario else payload.get("USUARIO"),

            # Datos del reporte (del payload)
            FECHAHORA_INICIO=fecha_reporte,
            ODOMETRO_INICIAL=payload.get("ODOMETRO_INICIAL"),
            ODOMETRO_FINAL=payload.get("ODOMETRO_FINAL"),
            HORAS_TRABAJADAS=payload.get("HORAS_TRABAJADAS"),
            HORAS_MINIMAS=payload.get("HORAS_MINIMAS"),
            KM_INICIO=km_inicial,
            KM_FINAL=payload.get("KM_FINAL"),
            KILOMETROS=payload.get("KILOMETROS"),
            Descripcion=trabajo_realizado,
            Observaciones=observaciones,
            Reporte_Pane=incidente,
            Estado_Reporte=estado_reporte,
            FOTO1=payload.get("FOTO1"),
            FOTO2=payload.get("FOTO2"),

            # Campos opcionales
            ID2_REPORTE=payload.get("ID2_REPORTE"),
            FECHAHORA_FIN=payload.get("FECHAHORA_FIN"),
            MT3=payload.get("MT3"),
            VUELTAS=payload.get("VUELTAS"),
            HORA_INI=payload.get("HORA_INI"),
            HORA_FIN=payload.get("HORA_FIN"),
            Control=payload.get("Control", 0),
            PDF_Reporte=payload.get("PDF_Reporte"),
            ID3_REPORTE=payload.get("ID3_REPORTE"),
            Estado_Pane=payload.get("Estado_Pane"),
            USUARIO_ID_UltimaModificacion=usuario.USUARIO_ID if usuario else None,
            pkUsuario_UltimaModificacion=pk_usuario
        )

        db.session.add(report)
        db.session.commit()
        db.session.refresh(report)

        # Recargar con relaciones para el _to_domain
        report_with_relations = (
            SAContratoReporte.query
            .options(
                joinedload(SAContratoReporte.contrato),
                joinedload(SAContratoReporte.maquina),
                joinedload(SAContratoReporte.usuario),
            )
            .filter(SAContratoReporte.pkReporte == report.pkReporte)
            .first()
        )

        return _to_domain(report_with_relations)

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