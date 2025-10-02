from typing import Sequence
from sqlalchemy import Case, text
from sqlalchemy.orm import joinedload
from app.models import Maquina as SAMaquina, User as SAUser, MaquinaUsuario as SAMaquinaUsuario
from ..domain.repository import MaquinaRepository
from ..domain.entity import Maquina
from ..domain.operador_ref import OperadorRef
from app.modules.maquinas.domain import operador_ref

def _to_operador_ref(u: SAUser) -> OperadorRef:
    pk_usuario = getattr(u, "pkUsuario", None)
    nombre = getattr(u, 'NOMBRE', None) or ""
    usuario_id = getattr(u, 'USUARIO_ID', None) or ""
    nombre_usuario = getattr(u, 'USUARIO', None) or ""

    usuario_final = nombre_usuario if nombre_usuario else nombre

    return OperadorRef(
        id=pk_usuario,
        usuario=usuario_final,
        usuario_id=usuario_id,
        nombre=nombre,
    )

def _to_domain(sa: SAMaquina) -> Maquina:
    sa_id = sa.pkMaquina
    sa_maquina = sa.MAQUINA
    sa_marca = sa.MARCA
    sa_modelo = sa.MODELO
    sa_patente = getattr(sa, "PATENTE", None)
    sa_estado = getattr(sa, "ESTADO", None)
    sa_id_maquina = getattr(sa, "ID_MAQUINA", None)

    # ✅ NUEVO - Extraer campos de última recarga
    hr_actual = getattr(sa, "HR_Actual", None)
    km_actual = getattr(sa, "KM_Actual", None)
    pk_ultima_recarga = getattr(sa, "pkUltima_recarga", None)
    id_ultima_recarga = getattr(sa, "ID_Ultima_Recarga", None)
    litros_ultima = getattr(sa, "Litros_Ultima", None)
    fecha_ultima = getattr(sa, "Fecha_Ultima", None)

    # 🔍 DEBUG - Mostrar datos de última recarga
    print(f"🔍 MAPEO MAQUINA {sa_id} - Datos de última recarga:")
    print(f"   HR_Actual: {hr_actual}")
    print(f"   KM_Actual: {km_actual}")
    print(f"   pkUltima_recarga: {pk_ultima_recarga}")
    print(f"   ID_Ultima_Recarga: {id_ultima_recarga}")
    print(f"   Litros_Ultima: {litros_ultima}")
    print(f"   Fecha_Ultima: {fecha_ultima}")

    operadores = []
    try:
        if hasattr(sa, 'operadores') and sa.operadores is not None:
            operadores = tuple(_to_operador_ref(usr) for usr in sa.operadores)
    except Exception as e:
        print(f"⚠️  Error cargando operadores para máquina {sa_id}: {e}")
        operadores = ()
    print(f"✅ DEBUG Mapping - ID: {sa_id}, Nombre: {sa_maquina}, Marca: {sa_marca}")
   
    return Maquina(
        id=sa_id,
        nombre=sa_maquina,
        marca=sa_marca,
        modelo=sa_modelo,
        patente=sa_patente,
        estado=sa_estado,
        id_maquina=sa_id_maquina,
        operadores=operadores,
        # ✅ NUEVO - Pasar campos de última recarga
        hr_actual=hr_actual,
        km_actual=km_actual,
        pk_ultima_recarga=pk_ultima_recarga,
        id_ultima_recarga=id_ultima_recarga,
        litros_ultima=litros_ultima,
        fecha_ultima=fecha_ultima,
    )
    
    
class SqlAlchemyMaquinaRepository(MaquinaRepository):
    def listar(self) -> Sequence[Maquina]:
        items = (
            SAMaquina.query
            .options(joinedload(SAMaquina.operadores) if hasattr(SAMaquina, 'operadores')else None)
            .order_by(Case(
                (SAMaquina.MAQUINA == None, 1),
                (SAMaquina.MAQUINA == '', 1),
                else_=0
            ), SAMaquina.MAQUINA
            )
            .all()
        )
        print(f"🔍 DEBUG - Retrieved {len(items)} Maquina records from DB")

        domain_maquinas = []
        for maquina in items:
            try:
                domain_maquinas.append(_to_domain(maquina))
            except Exception as e:
                print(f"⚠️  Error mapping Maquina ID {maquina.pkMaquina}: {e}")
                continue
        return domain_maquinas

    def get_operadores_by_maquina_id(self, maquina_id: int) -> Sequence[OperadorRef]:
        """
        Obtener operadores asignados a una máquina específica usando JOIN directo.
        """
        print(f"DEBUG - Buscando operadores para máquina ID: {maquina_id}")
        
        try:
            # JOIN directo usando los modelos SQLAlchemy
            operadores = (
                SAUser.query
                .join(SAMaquinaUsuario, SAMaquinaUsuario.pkUsuario == SAUser.pkUsuario)
                .filter(SAMaquinaUsuario.pkMaquina == maquina_id)
                .all()
            )
            
            print(f"DEBUG - Query encontró {len(operadores)} operadores")
            
            # Debug detallado de cada operador
            operadores_refs = []
            for i, op in enumerate(operadores):
                print(f"DEBUG - Operador {i+1}:")
                print(f"  - pkUsuario: {op.pkUsuario}")
                print(f"  - NOMBRE: '{op.NOMBRE}'")
                print(f"  - NOMBREUSUARIO: '{op.NOMBREUSUARIO}'")
                print(f"  - USUARIO_ID: '{op.USUARIO_ID}'")
                
                operador_ref = _to_operador_ref(op)
                operadores_refs.append(operador_ref)
                
                print(f"  - Mapeado como: id={operador_ref.id}, usuario='{operador_ref.usuario}', nombre='{operador_ref.nombre}', usuario_id='{operador_ref.usuario_id}'")
            
            print(f"DEBUG - Retornando {len(operadores_refs)} operadores mapeados")
            return operadores_refs
            
        except Exception as e:
            print(f"ERROR en get_operadores_by_maquina_id: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_by_id(self, maquina_id: int) -> Maquina | None:
        """Obtener máquina por ID con sus operadores"""
        try:
            maquina = SAMaquina.query.filter_by(pkMaquina=maquina_id).first()
            if not maquina:
                return None
            return _to_domain(maquina)
        except Exception as e:
            print(f"❌ ERROR en get_by_id: {e}")
            return None

    def create(self, maquina: Maquina) -> Maquina:
        # TODO: Implementar creación
        raise NotImplementedError()

    def update(self, maquina: Maquina) -> Maquina:
        # TODO: Implementar actualización  
        raise NotImplementedError()

    def delete(self, maquina_id: int) -> bool:
        # TODO: Implementar eliminación
        raise NotImplementedError()

