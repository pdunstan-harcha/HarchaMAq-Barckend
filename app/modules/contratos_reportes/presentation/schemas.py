
from marshmallow import Schema, fields, validates, ValidationError

class ListQuerySchema(Schema):
   limit = fields.Int(load_default=10)
   page = fields.Int(load_default=1)
   search = fields.Str(load_default="")
   
   
   @validates("limit")
   def validate_limit(self, value):
       if value <= 0 or value > 200:
           raise ValidationError("limit debe estar entre 1 y 200")
       

   @validates("page")
   def validate_page(self, value):
       if value <= 0:
           raise ValidationError("page debe ser mayor a 0")
       


class CreateReporteSchema(Schema):
            ID_REPORTE=fields.Str(load_default=None)
            ID2_REPORTE=fields.Int(load_default=999)
            ID_CONTRATO=fields.Str(load_default="99")
            pkContrato=fields.Int(load_default=99)
            ID_MAQUINA=fields.Str(load_default="m000099")
            pkMaquina=fields.Int(load_default=99)
            FECHAHORA_INICIO=fields.DateTime()
            USUARIO_ID=fields.Str(load_default="usuario_test")
            pkUsuario=fields.Int(load_default=1)
            ODOMETRO_INICIAL=fields.Int(load_default=1000)
            ODOMETRO_FINAL=fields.Int(load_default=1010)
            HORAS_TRABAJADAS=fields.Float(load_default=8.0)
            Descripcion=fields.Str()
            Observaciones=fields.Str()
            FOTO1=fields.Str()
            FOTO2=fields.Str()
            CONTRATO_TXT=fields.Str()
            CLIENTE_TXT=fields.Str()
            MAQUINA_TXT=fields.Str()
            USUARIO_TXT=fields.Str()
            HORAS_MINIMAS=fields.Float(load_default=8.0)
            FECHAHORA_FIN=fields.DateTime()
            OBRA_TXT=fields.Str()
            KM_FINAL=fields.Int()
            KILOMETROS=fields.Int()
            MT3=fields.Int()
            VUELTAS=fields.Int()
            KM_INICIO=fields.Int()
            MAQUINA_TIPO=fields.Str()
            MAQUINA_MARCA=fields.Str()
            MAQUINA_MODELO=fields.Str()
            HORA_INI=fields.Str()
            HORA_FIN=fields.Str()
            Control=fields.Int(load_default=0)
            PDF_Reporte=fields.Str()
            Estado_Reporte=fields.Str()
            ID3_REPORTE=fields.Str(load_default=None)
            Reporte_Pane=fields.Str()
            Estado_Pane=fields.Str()
            USUARIO_ID_UltimaModificacion=fields.Str(load_default="usuario_test")
            pkUsuario_UltimaModificacion=fields.Int(load_default=1)
    
    