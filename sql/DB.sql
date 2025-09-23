-- Estructura de las tablas principales de APP_HARCHA_MAQUINARIA

CREATE TABLE `CLIENTES` (
  `pkCliente` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`pkCliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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

CREATE TABLE `USUARIOS` (
  `pkUsuario` int NOT NULL AUTO_INCREMENT,
  `NOMBREUSUARIO` varchar(255) DEFAULT NULL,
  `CLAVE` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pkUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `OBRAS` (
  `pkObra` int NOT NULL AUTO_INCREMENT,
  `NOMBRE_OBRA` varchar(255) DEFAULT NULL,
  `UBICACION` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pkObra`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `CONTRATOS` (
  `pkContrato` int NOT NULL AUTO_INCREMENT,
  `CODIGO_CONTRATO` varchar(255) DEFAULT NULL,
  `NOMBRE_CONTRATO` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pkContrato`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `MAQUINAS_INGRESOS_SALIDAS` (
  `pkIngresoSalida` int NOT NULL AUTO_INCREMENT,
  `ID_MAQUINA` int DEFAULT NULL,
  `FECHAHORA` datetime DEFAULT NULL,
  `INGRESO_SALIDA` varchar(50) DEFAULT NULL,
  `ESTADO_MAQUINA` varchar(255) DEFAULT NULL,
  `Observaciones` text,
  `USUARIO_ID` int DEFAULT NULL,
  PRIMARY KEY (`pkIngresoSalida`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
  PRIMARY KEY (`pkRecarga`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
