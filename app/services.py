from datetime import datetime
from . import db
from .models import (
    User,
    Maquina,
    Contrato,
    Obra,
    Cliente,
    MaquinaIngresoSalida,
    RecargaCombustible,
    ContratoReporte,
)


def crear_ingreso_salida(data: dict) -> tuple[dict, int]:
    id_is = f"IS{datetime.now().strftime('%y%m%d%H%M%S')}"
    registro = MaquinaIngresoSalida(
        ID_IS=id_is,
        ID_MAQUINA=data.get("ID_MAQUINA"),
        pkMaquina=data.get("pkMaquina"),
        FECHAHORA=data.get("FECHAHORA"),
        INGRESO_SALIDA=data.get("INGRESO_SALIDA"),
        ESTADO_MAQUINA=data.get("ESTADO_MAQUINA"),
        Observaciones=data.get("Observaciones"),
        USUARIO_ID=data.get("USUARIO_ID"),
        pkUsuario=data.get("pkUsuario"),
    )
    db.session.add(registro)
    db.session.commit()
    return {
        "success": True,
        "message": "Registro guardado correctamente",
        "ID_IS": id_is,
        "pkIs": registro.pkIs,
    }, 201


def listar_ingresos_salidas() -> list[dict]:
    registros = (
        db.session.query(MaquinaIngresoSalida, Maquina.MAQUINA)
        .join(Maquina, MaquinaIngresoSalida.pkMaquina == Maquina.pkMaquina)
        .order_by(MaquinaIngresoSalida.FECHAHORA.desc())
        .all()
    )
    resultado = []
    for registro, nombre_maquina in registros:
        resultado.append(
            {
                "pkIs": registro.pkIs,
                "ID_IS": registro.ID_IS,
                "FECHAHORA": registro.FECHAHORA.isoformat() if registro.FECHAHORA else None,
                "INGRESO_SALIDA": registro.INGRESO_SALIDA,
                "ESTADO_MAQUINA": registro.ESTADO_MAQUINA,
                "Observaciones": registro.Observaciones,
                "ID_MAQUINA": registro.ID_MAQUINA,
                "pkMaquina": registro.pkMaquina,
                "NOMBRE_MAQUINA": nombre_maquina,
                "USUARIO_ID": registro.USUARIO_ID,
                "pkUsuario": registro.pkUsuario,
            }
        )
    return resultado


def crear_recarga_combustible(data: dict) -> tuple[dict, int]:
    codigo_recarga = f"RCO{datetime.now().strftime('%y%m%d%H%M%S')}"
    recarga = RecargaCombustible(
        ID_RECARGA=codigo_recarga,
        ID_MAQUINA=data.get("ID_MAQUINA"),
        pkMaquina=data.get("pkMaquina"),
        USUARIO_ID=data.get("USUARIO_ID"),
        pkUsuario=data.get("pkUsuario"),
        FECHA=data.get("FECHAHORA"),
        LITROS=data.get("LITROS"),
        FOTO=data.get("FOTO"),
        Observaciones=data.get("OBSERVACIONES"),
        ODOMETRO=data.get("ODOMETRO"),
        KILOMETROS=data.get("KILOMETROS"),
        PATENTE=data.get("PATENTE"),
        pkObra=data.get("OBRA_ID"),
        pkCliente=data.get("CLIENTE_ID"),
        OBRA_ID=data.get("OBRA_ID"),
        CLIENTE_ID=data.get("CLIENTE_ID"),
    )
    db.session.add(recarga)
    db.session.commit()
    return {
        "success": True,
        "message": "Recarga registrada correctamente",
        "ID_RECARGA": codigo_recarga,
        "pkRecarga": recarga.pkRecarga,
    }, 201


def listar_recargas_combustible() -> list[dict]:
    recargas = (
        db.session.query(
            RecargaCombustible,
            Maquina.MAQUINA.label("NOMBRE_MAQUINA"),
            User.NOMBREUSUARIO.label("NOMBRE_USUARIO"),
            Obra.OBRA.label("NOMBRE_OBRA"),
            Cliente.CLIENTE.label("NOMBRE_CLIENTE"),
        )
        .outerjoin(Maquina, RecargaCombustible.pkMaquina == Maquina.pkMaquina)
        .outerjoin(User, RecargaCombustible.pkUsuario == User.pkUsuario)
        .outerjoin(Obra, RecargaCombustible.pkObra == Obra.pkObra)
        .outerjoin(Cliente, RecargaCombustible.pkCliente == Cliente.pkCliente)
        .order_by(RecargaCombustible.FECHA.desc())
        .all()
    )
    resultado = []
    for recarga, nombre_maquina, nombre_usuario, nombre_obra, nombre_cliente in recargas:
        resultado.append(
            {
                "pkRecarga": recarga.pkRecarga,
                "ID_RECARGA": recarga.ID_RECARGA,
                "ID_MAQUINA": recarga.ID_MAQUINA,
                "NOMBRE_MAQUINA": nombre_maquina,
                "USUARIO_ID": recarga.USUARIO_ID,
                "NOMBRE_USUARIO": nombre_usuario,
                "FECHA": recarga.FECHA.isoformat() if recarga.FECHA else None,
                "LITROS": recarga.LITROS,
                "FOTO": recarga.FOTO,
                "Observaciones": recarga.Observaciones,
                "ODOMETRO": recarga.ODOMETRO,
                "KILOMETROS": recarga.KILOMETROS,
                "PATENTE": recarga.PATENTE,
                "OBRA_ID": recarga.OBRA_ID,
                "NOMBRE_OBRA": nombre_obra,
                "CLIENTE_ID": recarga.CLIENTE_ID,
                "NOMBRE_CLIENTE": nombre_cliente,
            }
        )
    return resultado


def crear_contrato_reporte(data: dict) -> tuple[dict, int]:
    id_reporte = f"RPT{datetime.now().strftime('%y%m%d%H%M%S')}"
    reporte = ContratoReporte(
        ID_REPORTE=id_reporte,
        ID2_REPORTE=data.get("ID2_REPORTE", 999),
        ID_CONTRATO=data.get("ID_CONTRATO", "99"),
        pkContrato=data.get("pkContrato", 99),
        ID_MAQUINA=data.get("ID_MAQUINA", "m000099"),
        pkMaquina=data.get("pkMaquina", 99),
        FECHAHORA_INICIO=data.get("FECHAHORA_INICIO", datetime.now()),
        USUARIO_ID=data.get("USUARIO_ID", "usuario_test"),
        pkUsuario=data.get("pkUsuario", 1),
        ODOMETRO_INICIAL=data.get("ODOMETRO_INICIAL", 1000),
        ODOMETRO_FINAL=data.get("ODOMETRO_FINAL", 1010),
        HORAS_TRABAJADAS=data.get("HORAS_TRABAJADAS", 8),
        Descripcion=data.get("Descripcion", "Descripción de prueba"),
        Observaciones=data.get("Observaciones", "Observaciones de prueba"),
        FOTO1=data.get("FOTO1", "foto1.jpg"),
        FOTO2=data.get("FOTO2", "foto2.jpg"),
        CONTRATO_TXT=data.get("CONTRATO_TXT", "Contrato de prueba"),
        CLIENTE_TXT=data.get("CLIENTE_TXT", "Cliente de prueba"),
        MAQUINA_TXT=data.get("MAQUINA_TXT", "Máquina de prueba"),
        USUARIO_TXT=data.get("USUARIO_TXT", "Usuario de prueba"),
        HORAS_MINIMAS=data.get("HORAS_MINIMAS", 8),
        FECHAHORA_FIN=data.get("FECHAHORA_FIN", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        OBRA_TXT=data.get("OBRA_TXT", "Obra de prueba"),
        KM_FINAL=data.get("KM_FINAL", 2000),
        KILOMETROS=data.get("KILOMETROS", 100),
        MT3=data.get("MT3", 50),
        VUELTAS=data.get("VUELTAS", 2),
        KM_INICIO=data.get("KM_INICIO", 1900),
        MAQUINA_TIPO=data.get("MAQUINA_TIPO", "Tipo prueba"),
        MAQUINA_MARCA=data.get("MAQUINA_MARCA", "Marca prueba"),
        MAQUINA_MODELO=data.get("MAQUINA_MODELO", "Modelo prueba"),
        HORA_INI=data.get("HORA_INI", "08:00"),
        HORA_FIN=data.get("HORA_FIN", "17:00"),
        Control=data.get("Control", 0),
        PDF_Reporte=data.get("PDF_Reporte", "reporte.pdf"),
        Estado_Reporte=data.get("Estado_Reporte", "Completado"),
        ID3_REPORTE=data.get("ID3_REPORTE", 999),
        Reporte_Pane=data.get("Reporte_Pane", "Pane prueba"),
        Estado_Pane=data.get("Estado_Pane", "OK"),
        USUARIO_ID_UltimaModificacion=data.get("USUARIO_ID_UltimaModificacion", "usuario_test"),
        pkUsuario_UltimaModificacion=data.get("pkUsuario_UltimaModificacion", 1),
    )
    db.session.add(reporte)
    db.session.commit()
    return {
        "success": True,
        "message": "Reporte registrado correctamente",
        "ID_REPORTE": id_reporte,
        "pkReporte": reporte.pkReporte,
    }, 201


def listar_contratos_reportes(limit: int, page: int, search: str) -> dict:
    query = ContratoReporte.query
    if search:
        query = query.filter(
            ContratoReporte.ID_REPORTE.like(f"%{search}%")
            | ContratoReporte.MAQUINA_TXT.like(f"%{search}%")
            | ContratoReporte.CONTRATO_TXT.like(f"%{search}%")
            | ContratoReporte.USUARIO_TXT.like(f"%{search}%")
            | ContratoReporte.Descripcion.like(f"%{search}%")
            | ContratoReporte.OBRA_TXT.like(f"%{search}%")
        )
    total_records = query.count()
    offset = (page - 1) * limit
    total_pages = (total_records + limit - 1) // limit
    reportes = (
        query.order_by(ContratoReporte.FECHAHORA_INICIO.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    data = []
    for r in reportes:
        data.append(
            {
                "pkReporte": r.pkReporte,
                "ID_REPORTE": r.ID_REPORTE,
                "ID2_REPORTE": r.ID2_REPORTE,
                "ID_CONTRATO": r.ID_CONTRATO,
                "pkContrato": r.pkContrato,
                "ID_MAQUINA": r.ID_MAQUINA,
                "pkMaquina": r.pkMaquina,
                "FECHAHORA_INICIO": r.FECHAHORA_INICIO.isoformat() if r.FECHAHORA_INICIO else None,
                "USUARIO_ID": r.USUARIO_ID,
                "pkUsuario": r.pkUsuario,
                "ODOMETRO_INICIAL": r.ODOMETRO_INICIAL,
                "ODOMETRO_FINAL": r.ODOMETRO_FINAL,
                "HORAS_TRABAJADAS": r.HORAS_TRABAJADAS,
                "Descripcion": r.Descripcion,
                "Observaciones": r.Observaciones,
                "FOTO1": r.FOTO1,
                "FOTO2": r.FOTO2,
                "CONTRATO_TXT": r.CONTRATO_TXT,
                "CLIENTE_TXT": r.CLIENTE_TXT,
                "MAQUINA_TXT": r.MAQUINA_TXT,
                "USUARIO_TXT": r.USUARIO_TXT,
                "HORAS_MINIMAS": r.HORAS_MINIMAS,
                "FECHAHORA_FIN": r.FECHAHORA_FIN,
                "OBRA_TXT": r.OBRA_TXT,
                "KM_FINAL": r.KM_FINAL,
                "KILOMETROS": r.KILOMETROS,
                "MT3": r.MT3,
                "VUELTAS": r.VUELTAS,
                "KM_INICIO": r.KM_INICIO,
                "MAQUINA_TIPO": r.MAQUINA_TIPO,
                "MAQUINA_MARCA": r.MAQUINA_MARCA,
                "MAQUINA_MODELO": r.MAQUINA_MODELO,
                "HORA_INI": r.HORA_INI,
                "HORA_FIN": r.HORA_FIN,
                "Control": r.Control,
                "PDF_Reporte": r.PDF_Reporte,
                "Estado_Reporte": r.Estado_Reporte,
                "ID3_REPORTE": r.ID3_REPORTE,
                "Reporte_Pane": r.Reporte_Pane,
                "Estado_Pane": r.Estado_Pane,
                "USUARIO_ID_UltimaModificacion": r.USUARIO_ID_UltimaModificacion,
                "pkUsuario_UltimaModificacion": r.pkUsuario_UltimaModificacion,
            }
        )
    return {
        "data": data,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "total_records": total_records,
    }
