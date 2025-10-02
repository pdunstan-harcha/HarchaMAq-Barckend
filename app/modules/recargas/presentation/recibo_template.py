def render_recibo_html(recarga, fecha):
    def safe(val):
        return val if val is not None else ''
    
    def remove_tildes(text):
        """Remueve tildes para evitar problemas de codificación en impresora"""
        if text is None:
            return ''
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'ñ': 'n', 'Ñ': 'N',
            'ü': 'u', 'Ü': 'U'
        }
        for old, new in replacements.items():
            text = str(text).replace(old, new)
        return text
    
    return f"""
    <!DOCTYPE html>
    <html lang='es'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=50mm, initial-scale=1.0'>
        <title>Recibo Recarga</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; font-size: 9px; margin: 0; padding: 0; width: 100%; }}
            .receipt {{ width: 50mm; max-width: 100%; margin: 0 auto; padding: 5px; }}
            .center {{ text-align: center; }}
            .header {{ margin-bottom: 8px; }}
            .header img {{ width: 50px; height: auto; margin-bottom: 3px; }}
            .company-info {{ font-size: 8px; line-height: 1.3; margin-bottom: 5px; }}
            h4 {{ margin: 8px 0; font-size: 10px; }}
            table {{ border-collapse: collapse; width: 100%; text-align: left; margin-bottom: 8px; }}
            table.data-table td {{ padding: 2px 4px; border: 1px solid #000; font-size: 8px; }}
            table.data-table td:first-child {{ font-weight: bold; width: 45%; }}
            .obs-section {{ margin: 8px 0; }}
            .obs-section td {{ padding: 2px 0; font-size: 8px; }}
            .signature {{ margin-top: 10px; border-top: 1px solid #000; padding-top: 3px; font-size: 8px; }}
            .signature-table td {{ padding: 2px; }}
        </style>
    </head>
    <body>
    <div class='receipt'>
        <div class='header center'>
            <img src='https://harcha.cl/wp-content/uploads/2024/05/Logo-Harcha-Vectorizado_1-2048x461.webp' alt='Logo Harcha' />
            <div style='font-size: 9px; margin: 3px 0;'><strong>{fecha}</strong></div>
            <div style='font-size: 9px; margin: 3px 0;'><strong>N: {safe(recarga.codigo)}</strong></div>
            <div class='company-info'>
                Harcha maquinaria SPA<br>
                RUT 76.858.929-1<br>
                Calle de Servicio Oriente N 700<br>
                Ruta 5 Sur Km. 832 fono 632461336<br>
                Comuna Los Lagos
            </div>
        </div>
        
        <h4 class='center'>ORDEN ENTREGA COMBUSTIBLES</h4>
        
        <table class='data-table'>
            <tbody>
                <tr><td>NOMBRE:</td><td>{remove_tildes(safe(recarga.usuario.usuario))}</td></tr>
                <tr><td>RUT:</td><td>{safe(recarga.rut_operador)}</td></tr>
                <tr><td>HOROMETRO:</td><td>{safe(recarga.odometro)}</td></tr>
                <tr><td>KILOMETRAJE:</td><td>{safe(recarga.kilometros)}</td></tr>
                <tr><td>LITROS:</td><td>{safe(recarga.litros)}</td></tr>
                <tr><td>CODIGO MAQUINA:</td><td>{remove_tildes(safe(recarga.maquina.nombre if recarga.maquina else ''))}</td></tr>
                <tr><td>OBRA:</td><td>{remove_tildes(safe(recarga.obra.nombre if recarga.obra else ''))}</td></tr>
                <tr><td>CLIENTE:</td><td>{remove_tildes(safe(recarga.cliente.nombre if recarga.cliente else ''))}</td></tr>
            </tbody>
        </table>
        
        <table class='obs-section'>
            <tbody>
                <tr><td><strong>Observaciones:</strong></td></tr>
                <tr><td>{remove_tildes(safe(recarga.observaciones))}</td></tr>
            </tbody>
        </table>
        
        <table class='signature-table'>
            <tbody>
                <tr>
                    <td class='signature' style='width: 48%;'>Firma operador:</td>
                    <td style='width: 4%;'>&nbsp;</td>
                    <td class='signature' style='width: 48%;'>Firma encargado reparto:</td>
                </tr>
                <tr>
                    <td><strong>{remove_tildes(safe(recarga.operador.usuario if recarga.operador else ''))}</strong></td>
                    <td>&nbsp;</td>
                    <td><strong>{remove_tildes(safe(recarga.usuario.usuario))}</strong></td>
                </tr>
            </tbody>
        </table>
    </div>
    </body>
    </html>
    """