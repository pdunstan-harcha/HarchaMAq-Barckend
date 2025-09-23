from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required

from .api_namespace import (
    contratos_reportes_ns, 
    create_reporte_input,
    update_reporte_input,
    list_response,
    create_response,
    get_response,
    message_response
)

from ..infrastructure.sqlalchemy_repository import SqlAlchemyContratoReporteRepository
from ..application.list_paginated import ListContratosReportesUseCase
from ..application.create_reporte import CreateContratoReporteUseCase, CreateContratoReporteInput
from ..application.obtener import GetContratoReporteUseCase, GetContratoReporteInput
from ..application.actualizar import UpdateContratoReporteUseCase, UpdateContratoReporteInput
from ..application.eliminar import DeleteContratoReporteUseCase, DeleteContratoReporteInput

from app.security.roles import (
    roles_required,
    ROLE_ADMIN,
    ROLE_SUPER_ADMIN,
    ROLE_INSPECTOR,
    ROLE_PETROLERO,
    ROLE_OPERADOR,
)

# Instanciar repositorio y casos de uso
repository = SqlAlchemyContratoReporteRepository()
list_uc = ListContratosReportesUseCase(repository)
create_uc = CreateContratoReporteUseCase(repository)
get_uc = GetContratoReporteUseCase(repository)
update_uc = UpdateContratoReporteUseCase(repository)
delete_uc = DeleteContratoReporteUseCase(repository)

@contratos_reportes_ns.route('/')
class ContratoReporteList(Resource):
    @contratos_reportes_ns.marshal_with(list_response)
    @contratos_reportes_ns.doc('list_reportes', security='Bearer')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR, ROLE_PETROLERO, ROLE_OPERADOR])
    def get(self):
        """Listar reportes de contratos"""
        from flask_jwt_extended import get_jwt
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        search = request.args.get('search', '')
        
        # Obtener información del usuario del JWT
        jwt_data = get_jwt()
        user_role = jwt_data.get('rol', '').upper()
        user_id = int(jwt_data.get('sub', 0))
        
        # Filtrar por usuario si es PETROLERO u OPERADOR
        user_filter = None
        if 'PETROLERO' in user_role or 'OPERADOR' in user_role:
            user_filter = user_id
        
        result = list_uc.execute(limit=per_page, page=page, search=search, user_filter=user_filter)
        
        data = [
            {
                "pkReporte": r.id,
                "ID_REPORTE": r.codigo,
                "FECHAHORA_INICIO": r.fecha_inicio.isoformat() if r.fecha_inicio else None,
                "Descripcion": r.descripcion,
                "MAQUINA_TXT": r.maquina_txt,
                "CONTRATO_TXT": r.contrato_txt,
                "USUARIO_TXT": r.usuario_txt,
                "contrato": ({"id": r.contrato.id, "nombre": r.contrato.nombre}
                             if r.contrato else None),
                "maquina": ({"id": r.maquina.id, "nombre": r.maquina.nombre}
                            if r.maquina else None),
                "usuario": ({"id": r.usuario.id, "usuario": r.usuario.usuario}
                            if r.usuario else None),
            }
            for r in result.data  # Use result.data instead of result[0]
        ]
        
        return {
            "success": True,
            "data": data,
            "page": result.page,
            "total_pages": result.total_pages,
            "total_records": result.total_records
        }

    @contratos_reportes_ns.expect(create_reporte_input, validate=True)
    @contratos_reportes_ns.marshal_with(create_response)
    @contratos_reportes_ns.doc('create_reporte', security='Bearer')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_PETROLERO, ROLE_OPERADOR])
    def post(self):
        """Crear nuevo reporte de contrato"""
        payload = request.get_json()
        created = create_uc.execute(CreateContratoReporteInput(payload=payload))
        
        return {
            "success": True,
            "pkReporte": created.id,
            "ID_REPORTE": created.codigo
        }

@contratos_reportes_ns.route('/<int:reporte_id>')
class ContratoReporteDetail(Resource):
    @contratos_reportes_ns.marshal_with(get_response)
    @contratos_reportes_ns.doc('get_reporte', security='Bearer')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR, ROLE_PETROLERO, ROLE_OPERADOR])
    def get(self, reporte_id):
        """Obtener reporte por ID"""
        result = get_uc.execute(GetContratoReporteInput(reporte_id=reporte_id))
        
        if not result.reporte:
            contratos_reportes_ns.abort(404, "Reporte no encontrado")
        
        r = result.reporte
        data = {
            "pkReporte": r.id,
            "ID_REPORTE": r.codigo,
            "FECHAHORA_INICIO": r.fecha_inicio.isoformat() if r.fecha_inicio else None,
            "Descripcion": r.descripcion,
            "MAQUINA_TXT": r.maquina_txt,
            "CONTRATO_TXT": r.contrato_txt,
            "USUARIO_TXT": r.usuario_txt,
            "contrato": ({"id": r.contrato.id, "nombre": r.contrato.nombre}
                         if r.contrato else None),
            "maquina": ({"id": r.maquina.id, "nombre": r.maquina.nombre}
                        if r.maquina else None),
            "usuario": ({"id": r.usuario.id, "usuario": r.usuario.usuario}
                        if r.usuario else None),
        }
        
        return {
            "success": True,
            "data": data
        }

    @contratos_reportes_ns.expect(update_reporte_input)
    @contratos_reportes_ns.marshal_with(message_response)
    @contratos_reportes_ns.doc('update_reporte', security='Bearer')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_PETROLERO, ROLE_OPERADOR])
    def put(self, reporte_id):
        """Actualizar reporte"""
        payload = request.get_json()
        result = update_uc.execute(UpdateContratoReporteInput(reporte_id=reporte_id, payload=payload))
        
        if not result.success:
            status_code = 404 if "no encontrado" in result.message else 400
            contratos_reportes_ns.abort(status_code, result.message)
        
        return {
            "success": True,
            "message": result.message
        }

    @contratos_reportes_ns.marshal_with(message_response)
    @contratos_reportes_ns.doc('delete_reporte', security='Bearer')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def delete(self, reporte_id):
        """Eliminar reporte"""
        result = delete_uc.execute(DeleteContratoReporteInput(reporte_id=reporte_id))
        
        if not result.success:
            status_code = 404 if "no encontrado" in result.message else 400
            contratos_reportes_ns.abort(status_code, result.message)
        
        return {
            "success": True,
            "message": result.message
        }
