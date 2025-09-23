CREATE TABLE `CLIENTES` (
  `pkCliente` int NOT NULL AUTO_INCREMENT,
  `ID_CLIENTE` char(16) DEFAULT NULL,
  `CLIENTE` varchar(255) DEFAULT NULL,
  `TELEFONO` varchar(255) DEFAULT NULL,
  `EMAIL` varchar(255) DEFAULT NULL,
  `RUT` varchar(255) DEFAULT NULL,
  `RESPONSABLE` varchar(255) DEFAULT NULL,
  `CARGO` varchar(255) DEFAULT NULL,
  `Comentarios` text,
  PRIMARY KEY (`pkCliente`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `CONTRATOS` (
  `pkContrato` int NOT NULL AUTO_INCREMENT,
  `ID_CONTRATO` char(16) DEFAULT NULL,
  `CONTRATO` varchar(255) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `FECHA_INICIO` datetime DEFAULT NULL,
  `OBRA` varchar(255) DEFAULT NULL,
  `ID_CLIENTE` char(16) DEFAULT NULL,
  `pkCliente` int DEFAULT NULL,
  `CON_OPERADOR` varchar(5) DEFAULT NULL,
  `CON_COMBUSTIBLE` varchar(5) DEFAULT NULL,
  `CON_PENSION` varchar(5) DEFAULT NULL,
  `PRECIO_HORA` int DEFAULT NULL,
  `Observaciones` text,
  `Estado` varchar(255) DEFAULT NULL,
  `PRECIO_MENSUAL` int DEFAULT NULL,
  `PRECIO_DIARIO` int DEFAULT NULL,
  `PRECIO_KM` int DEFAULT NULL,
  `PRECIO_MT3` int DEFAULT NULL,
  `TIPO_MEDICION` varchar(255) DEFAULT NULL,
  `TIPO_CONTRATO` varchar(255) DEFAULT NULL,
  `PRECIO_VUELTA` int DEFAULT NULL,
  `ID_OBRA` varchar(60) DEFAULT NULL,
  `pkObra` int DEFAULT NULL,
  `ContadorControl` int DEFAULT NULL,
  PRIMARY KEY (`pkContrato`),
  KEY `fk_contratos_cliente` (`pkCliente`),
  KEY `fk_contratos_maquina` (`pkMaquina`),
  KEY `fk_contratos_obra` (`pkObra`),
  CONSTRAINT `fk_contratos_cliente` FOREIGN KEY (`pkCliente`) REFERENCES `CLIENTES` (`pkCliente`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_contratos_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_contratos_obra` FOREIGN KEY (`pkObra`) REFERENCES `OBRAS` (`pkObra`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=817 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `CONTRATOS_REPORTES` (
  `pkReporte` int NOT NULL AUTO_INCREMENT,
  `ID_REPORTE` char(16) DEFAULT NULL,
  `ID2_REPORTE` int DEFAULT NULL,
  `ID_CONTRATO` char(16) DEFAULT NULL,
  `pkContrato` int DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `FECHAHORA_INICIO` datetime DEFAULT NULL,
  `USUARIO_ID` varchar(50) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  `ODOMETRO_INICIAL` int DEFAULT NULL,
  `ODOMETRO_FINAL` int DEFAULT NULL,
  `HORAS_TRABAJADAS` int DEFAULT NULL,
  `Descripcion` text,
  `Observaciones` text,
  `FOTO1` varchar(255) DEFAULT NULL,
  `FOTO2` varchar(255) DEFAULT NULL,
  `CONTRATO_TXT` varchar(255) DEFAULT NULL,
  `CLIENTE_TXT` varchar(255) DEFAULT NULL,
  `MAQUINA_TXT` varchar(255) DEFAULT NULL,
  `USUARIO_TXT` varchar(255) DEFAULT NULL,
  `HORAS_MINIMAS` int DEFAULT NULL,
  `FECHAHORA_FIN` varchar(255) DEFAULT NULL,
  `OBRA_TXT` varchar(255) DEFAULT NULL,
  `KM_FINAL` int DEFAULT NULL,
  `KILOMETROS` int DEFAULT NULL,
  `MT3` int DEFAULT NULL,
  `VUELTAS` int DEFAULT NULL,
  `KM_INICIO` int DEFAULT NULL,
  `MAQUINA_TIPO` varchar(255) DEFAULT NULL,
  `MAQUINA_MARCA` varchar(255) DEFAULT NULL,
  `MAQUINA_MODELO` varchar(255) DEFAULT NULL,
  `HORA_INI` varchar(255) DEFAULT NULL,
  `HORA_FIN` varchar(255) DEFAULT NULL,
  `Control` int DEFAULT NULL,
  `PDF_Reporte` varchar(255) DEFAULT NULL,
  `Estado_Reporte` varchar(255) DEFAULT NULL,
  `ID3_REPORTE` int DEFAULT NULL,
  `Reporte_Pane` text,
  `Estado_Pane` varchar(255) DEFAULT NULL,
  `USUARIO_ID_UltimaModificacion` varchar(50) DEFAULT NULL,
  `pkUsuario_UltimaModificacion` int DEFAULT NULL,
  PRIMARY KEY (`pkReporte`),
  KEY `idx_id_reporte` (`ID_REPORTE`),
  KEY `idx_id_contrato` (`ID_CONTRATO`),
  KEY `idx_id_maquina` (`ID_MAQUINA`),
  KEY `idx_id_usuario` (`USUARIO_ID`),
  KEY `fk_reportes_contrato` (`pkContrato`),
  KEY `fk_reportes_maquina` (`pkMaquina`),
  KEY `fk_reportes_usuario` (`pkUsuario`),
  KEY `idx_id_usuario_ultimamodificacion` (`USUARIO_ID_UltimaModificacion`),
  CONSTRAINT `fk_reportes_contrato` FOREIGN KEY (`pkContrato`) REFERENCES `CONTRATOS` (`pkContrato`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_reportes_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_reportes_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `DESCRIPCION_FAENA` (
  `DESCRIPCION` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `EQUIPO_FAMILIA` (
  `EQUIPO_FAMILIA` varchar(255) DEFAULT NULL,
  `FOTO` varchar(255) DEFAULT NULL,
  `TIPO_MEDICION` varchar(255) DEFAULT NULL,
  `TIPO_CONTRATO` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `LOG_Cambios_Maquinas` (
  `pkLog` int NOT NULL AUTO_INCREMENT,
  `FECHA_HORA` datetime DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `CODIGO_MAQUINA` varchar(255) DEFAULT NULL,
  `EMAIL_USUARIO` varchar(255) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  `ORIGEN_CAMBIO` varchar(255) DEFAULT NULL,
  `TIPO_ACCION` varchar(255) DEFAULT NULL,
  `Cambios` text,
  PRIMARY KEY (`pkLog`),
  KEY `fk_logcambios_maquina` (`pkMaquina`),
  KEY `fk_logcambios_usuario` (`pkUsuario`),
  CONSTRAINT `fk_logcambios_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_logcambios_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28433 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `LOG_OT` (
  `pkLog` int NOT NULL AUTO_INCREMENT,
  `IDLOG` char(16) DEFAULT NULL,
  `ID_ORDEN` char(16) DEFAULT NULL,
  `pkOrden` int DEFAULT NULL,
  `MAQUINA` varchar(255) DEFAULT NULL,
  `EmailUsuario` varchar(255) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL,
  `Tipo_Accion` varchar(255) DEFAULT NULL,
  `Cambios` text,
  `FechaOT` datetime DEFAULT NULL,
  PRIMARY KEY (`pkLog`),
  KEY `fk_logot_orden` (`pkOrden`),
  KEY `fk_logot_usuario` (`pkUsuario`),
  CONSTRAINT `fk_logot_orden` FOREIGN KEY (`pkOrden`) REFERENCES `OT` (`pkOrden`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_logot_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `LOG_TRIGGERS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tabla_afectada` varchar(100) DEFAULT NULL,
  `tipo_trigger` varchar(50) DEFAULT NULL,
  `evento` varchar(50) DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `detalle` text,
  `estado` varchar(20) DEFAULT 'OK',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `LOG_recargas` (
  `pkLog` int NOT NULL AUTO_INCREMENT,
  `IDLOG` char(16) DEFAULT NULL,
  `ID_RECARGA` char(16) DEFAULT NULL,
  `pkRecarga` int DEFAULT NULL,
  `EmailUsuario` varchar(255) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL,
  `Tipo_Accion` varchar(255) DEFAULT NULL,
  `Cambios` text,
  `FechaRecarga` datetime DEFAULT NULL,
  PRIMARY KEY (`pkLog`),
  KEY `fk_logrecargas_recarga` (`pkRecarga`),
  KEY `fk_logrecargas_usuario` (`pkUsuario`),
  CONSTRAINT `fk_logrecargas_recarga` FOREIGN KEY (`pkRecarga`) REFERENCES `RECARGAS_COMBUSTIBLE` (`pkRecarga`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_logrecargas_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `LOG_reportes` (
  `pkLog` int NOT NULL AUTO_INCREMENT,
  `IDLOG` char(16) DEFAULT NULL,
  `ID_REPORTE` char(16) DEFAULT NULL,
  `pkReporte` int DEFAULT NULL,
  `ID2_REPORTE` int DEFAULT NULL,
  `CONTRATO_TXT` varchar(255) DEFAULT NULL,
  `EMAIL_USUARIO` varchar(255) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL,
  `Tipo_Accion` varchar(255) DEFAULT NULL,
  `Cambios` text,
  `FechaReporte` datetime DEFAULT NULL,
  PRIMARY KEY (`pkLog`),
  KEY `idx_id_reporte_LOGReportes` (`ID_REPORTE`),
  KEY `fk_logreportes_reporte` (`pkReporte`),
  KEY `fk_logreportes_usuario` (`pkUsuario`),
  CONSTRAINT `fk_logreportes_reporte` FOREIGN KEY (`pkReporte`) REFERENCES `CONTRATOS_REPORTES` (`pkReporte`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_logreportes_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1581 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `MAQUINAS` (
  `pkMaquina` int NOT NULL AUTO_INCREMENT,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `CODIGO_MAQUINA` varchar(255) DEFAULT NULL,
  `EQUIPO_FAMILIA` varchar(255) DEFAULT NULL,
  `TIPO_MAQUINA` varchar(255) DEFAULT NULL,
  `MARCA` varchar(255) DEFAULT NULL,
  `MODELO` varchar(255) DEFAULT NULL,
  `ANYO` int DEFAULT NULL,
  `NUM_MOTOR` varchar(255) DEFAULT NULL,
  `NUM_CHASIS` varchar(255) DEFAULT NULL,
  `PATENTE` varchar(255) DEFAULT NULL,
  `EMPRESA` varchar(255) DEFAULT NULL,
  `POTENCIA_MOTOR` varchar(255) DEFAULT NULL,
  `LARGO` varchar(255) DEFAULT NULL,
  `ANCHO` varchar(255) DEFAULT NULL,
  `ALTURA` varchar(255) DEFAULT NULL,
  `PESO` varchar(255) DEFAULT NULL,
  `NEUMATICO` varchar(255) DEFAULT NULL,
  `CAPACIDAD_COMBUSTIBLE` varchar(255) DEFAULT NULL,
  `CAPACIDAD_TOLVA` varchar(255) DEFAULT NULL,
  `CAPACIDAD_BALDE` varchar(255) DEFAULT NULL,
  `COMENTARIOS_PAUTA` varchar(255) DEFAULT NULL,
  `NF_50` int DEFAULT NULL,
  `NF_250` int DEFAULT NULL,
  `NF_500` int DEFAULT NULL,
  `NF_750` int DEFAULT NULL,
  `NF_1000` int DEFAULT NULL,
  `NF_2000` int DEFAULT NULL,
  `ESTADO` varchar(255) DEFAULT NULL,
  `FOTO1` varchar(255) DEFAULT NULL,
  `CONTRATO_VIGENTE` char(16) DEFAULT NULL,
  `pkContrato_vigente` int DEFAULT NULL,
  `ALERTA_INCIDENTE` varchar(255) DEFAULT NULL,
  `CONTROL` int DEFAULT NULL,
  `MAQUINA` varchar(255) DEFAULT NULL,
  `HR_Actual` int DEFAULT NULL,
  `KM_Actual` int DEFAULT NULL,
  `Ultima_Actualizacion_HR` datetime DEFAULT NULL,
  `Ultima_Actualizacion_KM` datetime DEFAULT NULL,
  `HR_Proximo_Preventivo` int DEFAULT NULL,
  `KM_Proximo_Preventivo` int DEFAULT NULL,
  `ID_OT_Ultimo_Preventivo` char(16) DEFAULT NULL,
  `pkOt_ultimo_preventivo` int DEFAULT NULL,
  `KmHr` varchar(255) DEFAULT NULL,
  `ID_Ultimo_IS` char(16) DEFAULT NULL,
  `pkUltimo_is` int DEFAULT NULL,
  `HR_ActualCopia` int DEFAULT NULL,
  `KM_ActualCopia` int DEFAULT NULL,
  `Fecha_Horometro` datetime DEFAULT NULL,
  `Fecha_CuentaKm` datetime DEFAULT NULL,
  `ID_Ultimo_Reporte` char(16) DEFAULT NULL,
  `pkUltimo_reporte` int DEFAULT NULL,
  `ID_Ultima_Recarga` char(16) DEFAULT NULL,
  `pkUltima_recarga` int DEFAULT NULL,
  `Litros_Ultima` int DEFAULT NULL,
  `HrTrabajadas_Ultima` int DEFAULT NULL,
  `KmRecorridos_Ultima` int DEFAULT NULL,
  `Fecha_Ultima` datetime DEFAULT NULL,
  PRIMARY KEY (`pkMaquina`),
  KEY `fk_maquina_contrato_vigente` (`pkContrato_vigente`),
  KEY `fk_maquina_ultimo_preventivo` (`pkOt_ultimo_preventivo`),
  KEY `fk_maquina_ultimo_IS` (`pkUltimo_is`),
  KEY `fk_maquina_ultimo_reporte` (`pkUltimo_reporte`),
  KEY `fk_maquina_ultima_recarga` (`pkUltima_recarga`),
  CONSTRAINT `fk_maquina_contrato_vigente` FOREIGN KEY (`pkContrato_vigente`) REFERENCES `CONTRATOS` (`pkContrato`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_maquina_ultima_recarga` FOREIGN KEY (`pkUltima_recarga`) REFERENCES `RECARGAS_COMBUSTIBLE` (`pkRecarga`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_maquina_ultimo_IS` FOREIGN KEY (`pkUltimo_is`) REFERENCES `MAQUINAS_INGRESOS_SALIDAS` (`pkIs`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_maquina_ultimo_preventivo` FOREIGN KEY (`pkOt_ultimo_preventivo`) REFERENCES `OT` (`pkOrden`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_maquina_ultimo_reporte` FOREIGN KEY (`pkUltimo_reporte`) REFERENCES `CONTRATOS_REPORTES` (`pkReporte`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=229 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `MAQUINAS_DOCS` (
  `pkMaqdoc` int NOT NULL AUTO_INCREMENT,
  `ID_MAQDOC` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `DOCUMENTO` varchar(255) DEFAULT NULL,
  `OBSERVACIONES` text,
  PRIMARY KEY (`pkMaqdoc`),
  KEY `fk_maqdocs_maquina` (`pkMaquina`),
  CONSTRAINT `fk_maqdocs_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `MAQUINAS_INGRESOS_SALIDAS` (
  `pkIs` int NOT NULL AUTO_INCREMENT,
  `ID_IS` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `FECHAHORA` datetime DEFAULT NULL,
  `INGRESO_SALIDA` varchar(255) DEFAULT NULL,
  `ID_ULTIMO_IS` char(16) DEFAULT NULL,
  `pkUltimo_is` int DEFAULT NULL,
  `FECHAHORA_ULTIMO` datetime DEFAULT NULL,
  `TIEMPO` time DEFAULT NULL,
  `ESTADO_MAQUINA` varchar(255) DEFAULT NULL,
  `Control1` int DEFAULT NULL,
  `Observaciones` text,
  `Editar_Fecha` varchar(5) DEFAULT NULL,
  `Fecha_Editada` datetime DEFAULT NULL,
  `USUARIO_ID` varchar(50) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  PRIMARY KEY (`pkIs`),
  KEY `fk_ingresos_maquina` (`pkMaquina`),
  KEY `fk_ingresos_usuario` (`pkUsuario`),
  KEY `fk_ingresos_isanterior` (`pkUltimo_is`),
  CONSTRAINT `fk_ingresos_isanterior` FOREIGN KEY (`pkUltimo_is`) REFERENCES `MAQUINAS_INGRESOS_SALIDAS` (`pkIs`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ingresos_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ingresos_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=971 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `MAQUINAS_USUARIOS` (
  `pkMaqusuario` int NOT NULL AUTO_INCREMENT,
  `ID_MAQUSUARIO` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `USUARIO_ID` varchar(50) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  PRIMARY KEY (`pkMaqusuario`),
  KEY `fk_maqusuarios_maquina` (`pkMaquina`),
  KEY `fk_maqusuarios_usuario` (`pkUsuario`),
  CONSTRAINT `fk_maqusuarios_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_maqusuarios_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=533 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `MARCAS` (
  `MARCA` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `OBRAS` (
  `pkObra` int NOT NULL AUTO_INCREMENT,
  `ID_OBRA` varchar(60) DEFAULT NULL,
  `OBRA` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pkObra`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
CREATE TABLE `OT` (
  `pkOrden` int NOT NULL AUTO_INCREMENT,
  `ID_ORDEN` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `FECHA` datetime DEFAULT NULL,
  `FECHA_LLEGADA` datetime DEFAULT NULL,
  `FECHA_SALIDA` datetime DEFAULT NULL,
  `TIPO_ORDEN` varchar(255) DEFAULT NULL,
  `TALLER` varchar(255) DEFAULT NULL,
  `HRKM_LLEGADA` int DEFAULT NULL,
  `HRKM_SALIDA` int DEFAULT NULL,
  `FAENA_ORIGEN` varchar(255) DEFAULT NULL,
  `FAENA_DESTINO` varchar(255) DEFAULT NULL,
  `USUARIO_ID` varchar(50) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  `HORAS_HOMBRE` int DEFAULT NULL,
  `HRS_PREVENTIVO` int DEFAULT NULL,
  `Trabajos_a_realizar` text,
  `Trabajos_realizados` text,
  `Observaciones` text,
  `Responsable_entrega` varchar(255) DEFAULT NULL,
  `Responsable_recepcion` varchar(255) DEFAULT NULL,
  `Rev_Encendido_Motor` varchar(3) DEFAULT NULL,
  `Rev_Nivel_Estado_Aceite_Motor` varchar(3) DEFAULT NULL,
  `Rev_Nivel_Estado_Aceite_Hidraulico` varchar(3) DEFAULT NULL,
  `Rev_Nivel_Estado_Agua` varchar(3) DEFAULT NULL,
  `Rev_Nivel_Estado_Liquido_Freno_Pedal` varchar(3) DEFAULT NULL,
  `Rev_Fuga_Agua_Aceite_Motor` varchar(3) DEFAULT NULL,
  `Rev_Fuga_Aceite_Sistema_Hidraulico` varchar(3) DEFAULT NULL,
  `Rev_Filtro_Aceite_Motor` varchar(3) DEFAULT NULL,
  `Rev_Filtro_Aire_AC` varchar(3) DEFAULT NULL,
  `Rev_Baterias` varchar(3) DEFAULT NULL,
  `Rev_Limpia_Parabrisas_Estado` varchar(3) DEFAULT NULL,
  `Rev_Puertas_Cabina` varchar(3) DEFAULT NULL,
  `Rev_Plumillas` varchar(3) DEFAULT NULL,
  `Rev_Asiento` varchar(3) DEFAULT NULL,
  `Rev_Cinturon_de_Seguridad` varchar(3) DEFAULT NULL,
  `Rev_Corta_Corriente` varchar(3) DEFAULT NULL,
  `Rev_Estado_Luces` varchar(3) DEFAULT NULL,
  `Rev_Cinta_Reflectante` varchar(3) DEFAULT NULL,
  `Rev_Codigo_de_Falla` varchar(3) DEFAULT NULL,
  `Rev_Neumaticos_o_Rodados` varchar(3) DEFAULT NULL,
  `Rev_Mangueras_Principales` varchar(3) DEFAULT NULL,
  `Rev_Estado_Cableado_Principales` varchar(3) DEFAULT NULL,
  `Rev_Vidrios` varchar(3) DEFAULT NULL,
  `Rev_Espejos` varchar(3) DEFAULT NULL,
  `Rev_Calefaccin_y_Acc` varchar(3) DEFAULT NULL,
  `Rev_Escalas_y_Barandas` varchar(3) DEFAULT NULL,
  `Rev_Alarma_Retroceso` varchar(3) DEFAULT NULL,
  `Rev_Extintor` varchar(3) DEFAULT NULL,
  `Rev_Estructura_Revision_General` varchar(3) DEFAULT NULL,
  `Rev_Limpieza_general` varchar(3) DEFAULT NULL,
  `Estado_Orden` varchar(20) DEFAULT NULL,
  `HR_LLEGADA` int DEFAULT NULL,
  `HR_SALIDA` int DEFAULT NULL,
  `KM_LLEGADA` int DEFAULT NULL,
  `KM_SALIDA` int DEFAULT NULL,
  `HR_Pauta_Preventivo_OBSOLETO` int DEFAULT NULL,
  `KM_Pauta_Preventivo_OBSOLETO` int DEFAULT NULL,
  `EstadoMaquina_Anterior` varchar(255) DEFAULT NULL,
  `Lugar_Reparacion` varchar(255) DEFAULT NULL,
  `Reporte_Pane` text,
  `Estado_Pane` varchar(255) DEFAULT NULL,
  `USUARIO_ID_UltimaModificacion` varchar(50) DEFAULT NULL,
  `pkUsuario_UltimaModificacion` int DEFAULT NULL,
  PRIMARY KEY (`pkOrden`),
  KEY `fk_ot_maquina` (`pkMaquina`),
  KEY `fk_ot_usuario` (`pkUsuario`),
  CONSTRAINT `fk_ot_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ot_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1694 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `OT_MECANICOS` (
  `pkOrdenMecanico` int NOT NULL AUTO_INCREMENT,
  `ORDEN_ID` char(16) DEFAULT NULL,
  `pkOrden` int DEFAULT NULL,
  `MECANICO` varchar(255) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  `HORAS` int DEFAULT NULL,
  PRIMARY KEY (`pkOrdenMecanico`),
  KEY `fk_otmecanico_orden` (`pkOrden`),
  KEY `fk_otmecanico_usuario` (`pkUsuario`),
  CONSTRAINT `fk_otmecanico_orden` FOREIGN KEY (`pkOrden`) REFERENCES `OT` (`pkOrden`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_otmecanico_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2035 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `PAUTAS_ACTIVIDADES` (
  `pkActividades` int NOT NULL AUTO_INCREMENT,
  `ID_ACTIVIDADES` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `ACTIVIDAD` varchar(255) DEFAULT NULL,
  `HRS_50` varchar(255) DEFAULT NULL,
  `HRS_250` varchar(255) DEFAULT NULL,
  `HRS_500` varchar(255) DEFAULT NULL,
  `HRS_750` varchar(255) DEFAULT NULL,
  `HRS_1000` varchar(255) DEFAULT NULL,
  `HRS_2000` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pkActividades`),
  KEY `fk_pautasactividades_maquina` (`pkMaquina`),
  CONSTRAINT `fk_pautasactividades_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1665 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `PAUTAS_FILTROS` (
  `pkFiltros` int NOT NULL AUTO_INCREMENT,
  `ID_FILTROS` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `FILTRO` varchar(255) DEFAULT NULL,
  `CANTIDAD` int DEFAULT NULL,
  `NUM_FILTRO_ORIGINAL` varchar(255) DEFAULT NULL,
  `DONALSON` varchar(255) DEFAULT NULL,
  `FLEETGUARD` varchar(255) DEFAULT NULL,
  `BALWIN` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pkFiltros`),
  KEY `fk_pautasfiltros_maquina` (`pkMaquina`),
  CONSTRAINT `fk_pautasfiltros_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=488 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `PAUTAS_LUBRICANTES` (
  `pkLubricantes` int NOT NULL AUTO_INCREMENT,
  `ID_lUBRICANTES` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `LUBRICANTES` varchar(255) DEFAULT NULL,
  `CANTIDAD` varchar(255) DEFAULT NULL,
  `ESPECIFICACION_ORIGINAL` varchar(255) DEFAULT NULL,
  `ESPECIFICACION_ALTERNATIVA` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pkLubricantes`),
  KEY `fk_pautaslubricantes_maquina` (`pkMaquina`),
  CONSTRAINT `fk_pautaslubricantes_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=354 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `RECARGAS_COMBUSTIBLE` (
  `pkRecarga` int NOT NULL AUTO_INCREMENT,
  `ID_RECARGA` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `USUARIO_ID` varchar(50) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  `FECHA` datetime DEFAULT NULL,
  `LITROS` int DEFAULT NULL,
  `FOTO` varchar(255) DEFAULT NULL,
  `Observaciones` text,
  `ODOMETRO` int DEFAULT NULL,
  `KILOMETROS` int DEFAULT NULL,
  `FECHAHORA_RECARGA` datetime DEFAULT NULL,
  `ID_OPERADOR` varchar(50) DEFAULT NULL,
  `pkOperador` int DEFAULT NULL,
  `RUT_OPERADOR` varchar(255) DEFAULT NULL,
  `PATENTE` varchar(255) DEFAULT NULL,
  `OBRA_ID` varchar(60) DEFAULT NULL,
  `pkObra` int DEFAULT NULL,
  `CLIENTE_ID` char(16) DEFAULT NULL,
  `pkCliente` int DEFAULT NULL,
  `ID_Recarga_Anterior` char(16) DEFAULT NULL,
  `pkRecarga_anterior` int DEFAULT NULL,
  `Litros_Anterior` int DEFAULT NULL,
  `Horometro_Anterior` int DEFAULT NULL,
  `Kilometro_Anterior` int DEFAULT NULL,
  `Fecha_Anterior` datetime DEFAULT NULL,
  `USUARIO_ID_UltimaModificacion` varchar(50) DEFAULT NULL,
  `pkUsuario_UltimaModificacion` int DEFAULT NULL,
  PRIMARY KEY (`pkRecarga`),
  KEY `idx_id_recarga` (`ID_RECARGA`),
  KEY `fk_recarga_maquina` (`pkMaquina`),
  KEY `fk_recarga_usuario` (`pkUsuario`),
  KEY `fk_recarga_operador` (`pkOperador`),
  KEY `fk_recarga_obra` (`pkObra`),
  KEY `fk_recarga_cliente` (`pkCliente`),
  KEY `fk_recarga_anterior` (`pkRecarga_anterior`),
  CONSTRAINT `fk_recarga_anterior` FOREIGN KEY (`pkRecarga_anterior`) REFERENCES `RECARGAS_COMBUSTIBLE` (`pkRecarga`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_recarga_cliente` FOREIGN KEY (`pkCliente`) REFERENCES `CLIENTES` (`pkCliente`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_recarga_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_recarga_obra` FOREIGN KEY (`pkObra`) REFERENCES `OBRAS` (`pkObra`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_recarga_operador` FOREIGN KEY (`pkOperador`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_recarga_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3231 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `REPORTE_INCIDENTES` (
  `pkReporte` int NOT NULL AUTO_INCREMENT,
  `ID_REPORTE` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `USUARIO_ID` varchar(50) DEFAULT NULL,
  `pkUsuario` int DEFAULT NULL,
  `FECHA` datetime DEFAULT NULL,
  `Observaciones` text,
  `FOTO1` varchar(255) DEFAULT NULL,
  `FOTO2` varchar(255) DEFAULT NULL,
  `ODOMETRO` int DEFAULT NULL,
  PRIMARY KEY (`pkReporte`),
  KEY `fk_incidentes_maquina` (`pkMaquina`),
  KEY `fk_incidentes_usuario` (`pkUsuario`),
  CONSTRAINT `fk_incidentes_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_incidentes_usuario` FOREIGN KEY (`pkUsuario`) REFERENCES `USUARIOS` (`pkUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=164 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `TIPO_MAQUINA` (
  `TIPO_MAQUINA` varchar(255) DEFAULT NULL,
  `EQUIPO_FAMILIA` varchar(255) DEFAULT NULL,
  `PAUTA_HR_MANUTENCION` varchar(255) DEFAULT NULL,
  `PAUTA_KM_MANUTENCION` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `TRASLADOS` (
  `pkTraslado` int NOT NULL AUTO_INCREMENT,
  `ID_TRASLADO` char(16) DEFAULT NULL,
  `ID_MAQUINA` char(16) DEFAULT NULL,
  `pkMaquina` int DEFAULT NULL,
  `FECHA` datetime DEFAULT NULL,
  `ORIGEN` varchar(255) DEFAULT NULL,
  `DESTINO` varchar(255) DEFAULT NULL,
  `Observaciones` text,
  PRIMARY KEY (`pkTraslado`),
  KEY `fk_traslados_maquina` (`pkMaquina`),
  CONSTRAINT `fk_traslados_maquina` FOREIGN KEY (`pkMaquina`) REFERENCES `MAQUINAS` (`pkMaquina`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE `USUARIOS` (
  `pkUsuario` int NOT NULL AUTO_INCREMENT,
  `USUARIO_ID` varchar(50) DEFAULT NULL,
  `NOMBRE` varchar(100) DEFAULT NULL,
  `APELLIDOS` varchar(100) DEFAULT NULL,
  `ROL` varchar(20) DEFAULT NULL,
  `EmailUsuario` varchar(100) DEFAULT NULL,
  `TELEFONO` varchar(50) DEFAULT NULL,
  `USUARIO` varchar(200) DEFAULT NULL,
  `RUT` varchar(20) DEFAULT NULL,
  `NOMBREUSUARIO` varchar(20) DEFAULT NULL,
  `CLAVE` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`pkUsuario`),
  KEY `idx_usuarios_usuarioid` (`USUARIO_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=193 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
