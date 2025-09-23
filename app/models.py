from . import db

# Asociación como objeto (tabla con PK propia)
class MaquinaUsuario(db.Model):
    __tablename__ = "MAQUINAS_USUARIOS"

    pkMaqusuario = db.Column(db.Integer, primary_key=True)
    ID_MAQUSUARIO = db.Column(db.String(16))
    ID_MAQUINA = db.Column(db.String(16))
    pkMaquina = db.Column(db.Integer, db.ForeignKey("MAQUINAS.pkMaquina"))
    USUARIO_ID = db.Column(db.String(50))
    pkUsuario = db.Column(db.Integer, db.ForeignKey("USUARIOS.pkUsuario"))


class User(db.Model):
    __tablename__ = "USUARIOS"

    pkUsuario = db.Column(db.Integer, primary_key=True)
    USUARIO_ID = db.Column(db.String(50))
    NOMBRE = db.Column(db.String(100))
    APELLIDOS = db.Column(db.String(100))
    ROL = db.Column(db.String(20))
    EmailUsuario = db.Column(db.String(100))
    TELEFONO = db.Column(db.String(50))
    USUARIO = db.Column(db.String(200))
    RUT = db.Column(db.String(20))
    NOMBREUSUARIO = db.Column(db.String(20))
    # Nota: en el esquema actual la columna es VARCHAR(20) y puede ser NULL
    CLAVE = db.Column(db.String(20))

    # Relación a las máquinas que este usuario opera
    maquinas = db.relationship(
        "Maquina", secondary=MaquinaUsuario.__table__, back_populates="operadores"
    )

    def __repr__(self):
        return f"<User {self.NOMBREUSUARIO}>"


class Maquina(db.Model):
    __tablename__ = "MAQUINAS"

    pkMaquina = db.Column(db.Integer, primary_key=True)
    ID_MAQUINA = db.Column(db.String(16))
    CODIGO_MAQUINA = db.Column(db.String(255))
    MAQUINA = db.Column(db.String(255))
    MARCA = db.Column(db.String(255))
    MODELO = db.Column(db.String(255))
    PATENTE = db.Column(db.String(255))
    ESTADO = db.Column(db.String(255))

    # Relación a los usuarios (operadores) de esta máquina
    operadores = db.relationship(
        "User", secondary=MaquinaUsuario.__table__, back_populates="maquinas"
    )

    def __repr__(self):
        return f"<Maquina {self.MAQUINA}>"


class Cliente(db.Model):
    __tablename__ = "CLIENTES"
    pkCliente = db.Column(db.Integer, primary_key=True)
    ID_CLIENTE = db.Column(db.String(16))
    CLIENTE = db.Column(db.String(255))
    RUT = db.Column(db.String(255))


class Obra(db.Model):
    __tablename__ = "OBRAS"
    pkObra = db.Column(db.Integer, primary_key=True)
    ID_OBRA = db.Column(db.String(60))
    OBRA = db.Column(db.String(255))


class Contrato(db.Model):
    __tablename__ = "CONTRATOS"
    pkContrato = db.Column(db.Integer, primary_key=True)
    ID_CONTRATO = db.Column(db.String(16))
    CONTRATO = db.Column(db.String(255))
    pkMaquina = db.Column(db.Integer, db.ForeignKey("MAQUINAS.pkMaquina"))
    pkCliente = db.Column(db.Integer, db.ForeignKey("CLIENTES.pkCliente"))
    pkObra = db.Column(db.Integer, db.ForeignKey("OBRAS.pkObra"))
    FECHA_INICIO = db.Column(db.DateTime)
    Estado = db.Column(db.String(255))


class MaquinaIngresoSalida(db.Model):
    __tablename__ = "MAQUINAS_INGRESOS_SALIDAS"
    
    pkIs = db.Column(db.Integer, primary_key=True)
    ID_IS = db.Column(db.String(16))
    ID_MAQUINA = db.Column(db.String(16))
    pkMaquina = db.Column(db.Integer, db.ForeignKey("MAQUINAS.pkMaquina"))
    FECHAHORA = db.Column(db.DateTime)
    INGRESO_SALIDA = db.Column(db.String(255))
    ID_ULTIMO_IS = db.Column(db.String(16))
    pkUltimo_is = db.Column(db.Integer, db.ForeignKey("MAQUINAS_INGRESOS_SALIDAS.pkIs"))
    FECHAHORA_ULTIMO = db.Column(db.DateTime)
    TIEMPO = db.Column(db.Time)
    ESTADO_MAQUINA = db.Column(db.String(255))
    Control1 = db.Column(db.Integer)
    Observaciones = db.Column(db.Text)
    Editar_Fecha = db.Column(db.String(5))
    Fecha_Editada = db.Column(db.DateTime)
    USUARIO_ID = db.Column(db.String(50))
    pkUsuario = db.Column(db.Integer, db.ForeignKey("USUARIOS.pkUsuario"))

    # Relaciones
    maquina = db.relationship("Maquina", foreign_keys=[pkMaquina])
    usuario = db.relationship("User", foreign_keys=[pkUsuario])
    ingreso_salida_anterior = db.relationship(
        "MaquinaIngresoSalida", 
        foreign_keys=[pkUltimo_is], 
        remote_side=[pkIs]
    )

class RecargaCombustible(db.Model):
    __tablename__ = "RECARGAS_COMBUSTIBLE"

    # ✅ SOLO los campos que REALMENTE existen en la BD
    pkRecarga = db.Column(db.Integer, primary_key=True)
    ID_RECARGA = db.Column(db.String(16))
    ID_MAQUINA = db.Column(db.String(16))
    pkMaquina = db.Column(db.Integer, db.ForeignKey("MAQUINAS.pkMaquina"))
    USUARIO_ID = db.Column(db.String(50))
    pkUsuario = db.Column(db.Integer, db.ForeignKey("USUARIOS.pkUsuario"))
    FECHA = db.Column(db.DateTime)
    LITROS = db.Column(db.Integer)
    FOTO = db.Column(db.String(255))
    Observaciones = db.Column(db.Text)
    ODOMETRO = db.Column(db.Integer)
    KILOMETROS = db.Column(db.Integer)
    FECHAHORA_RECARGA = db.Column(db.DateTime)
    ID_OPERADOR = db.Column(db.String(50))
    pkOperador = db.Column(db.Integer, db.ForeignKey("USUARIOS.pkUsuario"))
    RUT_OPERADOR = db.Column(db.String(255))
    PATENTE = db.Column(db.String(255))
    OBRA_ID = db.Column(db.String(60))
    pkObra = db.Column(db.Integer, db.ForeignKey("OBRAS.pkObra"))
    CLIENTE_ID = db.Column(db.String(16))
    pkCliente = db.Column(db.Integer, db.ForeignKey("CLIENTES.pkCliente"))
    ID_Recarga_Anterior = db.Column(db.String(16))
    pkRecarga_anterior = db.Column(db.Integer, db.ForeignKey("RECARGAS_COMBUSTIBLE.pkRecarga"))
    Litros_Anterior = db.Column(db.Integer)
    Horometro_Anterior = db.Column(db.Integer)
    Kilometro_Anterior = db.Column(db.Integer)
    Fecha_Anterior = db.Column(db.DateTime)
    USUARIO_ID_UltimaModificacion = db.Column(db.String(50))
    pkUsuario_UltimaModificacion = db.Column(db.Integer, db.ForeignKey("USUARIOS.pkUsuario"))

    # Relaciones
    maquina = db.relationship("Maquina", foreign_keys=[pkMaquina])
    usuario = db.relationship("User", foreign_keys=[pkUsuario])
    operador = db.relationship("User", foreign_keys=[pkOperador])
    obra = db.relationship("Obra", foreign_keys=[pkObra])
    cliente = db.relationship("Cliente", foreign_keys=[pkCliente])
    recarga_anterior = db.relationship(
        "RecargaCombustible", foreign_keys=[pkRecarga_anterior], remote_side=[pkRecarga]
    )
    usuario_ultima_modificacion = db.relationship(
        "User", foreign_keys=[pkUsuario_UltimaModificacion]
    )

class ContratoReporte(db.Model):
    __tablename__ = "CONTRATOS_REPORTES"

    pkReporte = db.Column(db.Integer, primary_key=True)
    ID_REPORTE = db.Column(db.String(16))
    ID2_REPORTE = db.Column(db.Integer)
    ID_CONTRATO = db.Column(db.String(16))
    pkContrato = db.Column(db.Integer, db.ForeignKey("CONTRATOS.pkContrato"))
    ID_MAQUINA = db.Column(db.String(16))
    pkMaquina = db.Column(db.Integer, db.ForeignKey("MAQUINAS.pkMaquina"))
    FECHAHORA_INICIO = db.Column(db.DateTime)
    USUARIO_ID = db.Column(db.String(50))
    pkUsuario = db.Column(db.Integer, db.ForeignKey("USUARIOS.pkUsuario"))
    ODOMETRO_INICIAL = db.Column(db.Integer)
    ODOMETRO_FINAL = db.Column(db.Integer)
    HORAS_TRABAJADAS = db.Column(db.Integer)
    Descripcion = db.Column(db.Text)
    Observaciones = db.Column(db.Text)
    FOTO1 = db.Column(db.String(255))
    FOTO2 = db.Column(db.String(255))
    CONTRATO_TXT = db.Column(db.String(255))
    CLIENTE_TXT = db.Column(db.String(255))
    MAQUINA_TXT = db.Column(db.String(255))
    USUARIO_TXT = db.Column(db.String(255))
    HORAS_MINIMAS = db.Column(db.Integer)
    FECHAHORA_FIN = db.Column(db.String(255))
    OBRA_TXT = db.Column(db.String(255))
    KM_FINAL = db.Column(db.Integer)
    KILOMETROS = db.Column(db.Integer)
    MT3 = db.Column(db.Integer)
    VUELTAS = db.Column(db.Integer)
    KM_INICIO = db.Column(db.Integer)
    MAQUINA_TIPO = db.Column(db.String(255))
    MAQUINA_MARCA = db.Column(db.String(255))
    MAQUINA_MODELO = db.Column(db.String(255))
    HORA_INI = db.Column(db.String(255))
    HORA_FIN = db.Column(db.String(255))
    Control = db.Column(db.Integer)
    PDF_Reporte = db.Column(db.String(255))
    Estado_Reporte = db.Column(db.String(255))
    ID3_REPORTE = db.Column(db.Integer)
    Reporte_Pane = db.Column(db.Text)
    Estado_Pane = db.Column(db.String(255))
    USUARIO_ID_UltimaModificacion = db.Column(db.String(50))
    pkUsuario_UltimaModificacion = db.Column(
        db.Integer, db.ForeignKey("USUARIOS.pkUsuario")
    )

    # Relaciones
    contrato = db.relationship("Contrato", foreign_keys=[pkContrato])
    maquina = db.relationship("Maquina", foreign_keys=[pkMaquina])
    usuario = db.relationship("User", foreign_keys=[pkUsuario])
    usuario_ultima_modificacion = db.relationship(
        "User", foreign_keys=[pkUsuario_UltimaModificacion]
    )
