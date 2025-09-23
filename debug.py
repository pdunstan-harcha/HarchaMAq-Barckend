from app import create_app
from app.modules.maquinas.infrastructure.sqlalchemy_repository import SqlAlchemyMaquinaRepository
from app.modules.maquinas.application.list_maquinas import ListMaquinasUseCase

# Crear contexto de aplicación Flask
app = create_app()

with app.app_context():
    # Primero, probar directamente el modelo SQLAlchemy
    from app.models import Maquina as SAMaquina
    
    print("=== PRUEBA DIRECTA DEL MODELO SQLALCHEMY ===")
    primera_sa = SAMaquina.query.first()
    if primera_sa:
        print(f"SA - ID: {primera_sa.pkMaquina}")
        print(f"SA - Atributos: {[attr for attr in dir(primera_sa) if not attr.startswith('_') and not callable(getattr(primera_sa, attr))]}")
        print(f"SA - MAQUINA: {getattr(primera_sa, 'MAQUINA', 'NO_EXISTE')}")
        print(f"SA - MARCA: {getattr(primera_sa, 'MARCA', 'NO_EXISTE')}")
        print(f"SA - MODELO: {getattr(primera_sa, 'MODELO', 'NO_EXISTE')}")
    
    print("\n=== PRUEBA DEL CASO DE USO ===")
    repo = SqlAlchemyMaquinaRepository()
    use_case = ListMaquinasUseCase(repo=repo)
    
    try:
        result = use_case.execute()
        
        if hasattr(result, 'data') and result.data:
            primera_maquina = result.data[0]
            print(f"Domain - ID: {primera_maquina.id}")
            print(f"Domain - Nombre: {primera_maquina.nombre}")
            print(f"Domain - Marca: {primera_maquina.marca}")
            print(f"Domain - Modelo: {primera_maquina.modelo}")
            
    except Exception as e:
        print(f"Error: {e}")