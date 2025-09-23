from dataclasses import dataclass
from ..domain.repository import IngresoSalidaRepository
from ..domain.entity import IngresoSalida

@dataclass
class CreateIngresoSalidaInput:
    payload: dict

class CreateIngresoSalidaUseCase:
    def __init__(self, repo: IngresoSalidaRepository):
        self.repo = repo

    def execute(self, input_data: CreateIngresoSalidaInput) -> IngresoSalida:
        # Validaciones básicas
        payload = input_data.payload
        
        if not payload.get('pkMaquina'):
            raise ValueError("pkMaquina es requerido")
            
        if not payload.get('pkUsuario'):
            raise ValueError("pkUsuario es requerido")
            
        tipo_movimiento = payload.get('INGRESO_SALIDA', '').upper()
        if tipo_movimiento not in ['INGRESO', 'SALIDA']:
            raise ValueError("INGRESO_SALIDA debe ser 'INGRESO' o 'SALIDA'")
        
        # Validar lógica de negocio
        maquina_id = payload.get('pkMaquina')
        ultimo_is = self.repo.obtener_ultimo_por_maquina(maquina_id)
        
        if ultimo_is:
            # Validar secuencia lógica: no pueden ser dos ingresos o dos salidas seguidas
            if ultimo_is.ingreso_salida == tipo_movimiento:
                raise ValueError(
                    f"No se puede registrar {tipo_movimiento} consecutivo. "
                    f"El último registro fue {ultimo_is.ingreso_salida}"
                )
        
        return self.repo.crear(payload)