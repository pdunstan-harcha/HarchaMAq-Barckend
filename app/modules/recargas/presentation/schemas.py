from marshmallow import Schema, fields

class CreateRecargaSchema(Schema):
    ID_MAQUINA = fields.Str(load_default=None)
    pkMaquina = fields.Int(load_default=None)
    FECHAHORA = fields.DateTime(required=True)
    LITROS = fields.Int(required=True)
    FOTO = fields.Str(load_default=None)
    OBSERVACIONES = fields.Str(load_default=None)
    ODOMETRO = fields.Int(load_default=None)
    KILOMETROS = fields.Int(load_default=None)
    PATENTE = fields.Str(load_default=None)
    OBRA_ID = fields.Int(load_default=None)
    CLIENTE_ID = fields.Int(load_default=None)
    USUARIO_ID = fields.Str(load_default=None)
    pkUsuario = fields.Int(load_default=None)