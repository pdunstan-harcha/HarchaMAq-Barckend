# recibo_template.py

def render_recibo_html(recarga, fecha):
    def safe(val):
        return val if val is not None else ''
    return f"""
    <!DOCTYPE html>
    <html lang='es'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=50mm, initial-scale=1.0'>
        <title>Recibo Recarga</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; font-size: 9px; margin: 0; padding: 0; width: 100%; }}
            .datosHarcha {{ font-family: 'Arial', sans-serif; font-size: 8px; white-space: nowrap; padding: 0px; }}
            .receipt {{ width: 50mm; max-width: 100%; margin: 0 auto; padding: 5px; }}
            .center {{ text-align: center; }}
            .header, .footer, .details, .totals {{ margin-bottom: 5px; }}
            .header img {{ width: 40px; height: auto; margin-bottom: 2px; }}
            .details table, .totals table {{ width: 100%; border-collapse: collapse; }}
            .details th, .details td, .totals th, .totals td {{ text-align: left; padding: 2px 0; }}
            .totals th {{ text-align: left; }}
            .signature {{ margin-top: 10px; border-top: 1px solid #000; text-align: left; padding-top: 2px; }}
        </style>
    </head>
    <body>
    <div class='receipt'>
        <div class='header center'>
            <img style='height: 30px; width: auto;' src='https://harcha.cl/wp-content/uploads/2024/05/Logo-Harcha-Vectorizado_1-2048x461.webp' alt='Logo' />
            <div><strong>{fecha}</strong></div>
            <div><strong>N°: {safe(recarga.id)}</strong></div>
            <div class='datosHarcha'>
                Harcha maquinaria SPA<br>
                RUT 76.858.929-1<br>
                Calle de Servicio Oriente N° 700<br>
                Ruta 5 Sur Km. 832 fono 632461336<br>
                Comuna Los Lagos
            </div>
        </div>
        <h4 class='center'>ORDEN ENTREGA COMBUSTIBLES</h4>
        <table style='border-collapse: collapse; width: 100%; text-align: left;' border='1'>
            <tbody>
                <tr><td><strong>NOMBRE:</strong></td><td>{safe(recarga.nombre)}</td></tr>
                <tr><td><strong>RUT:</strong></td><td>{safe(recarga.rut)}</td></tr>
                <tr><td><strong>HOROMETRO:</strong></td><td>{safe(recarga.horometro)}</td></tr>
                <tr><td><strong>KILOMETRAJE:</strong></td><td>{safe(recarga.kilometros)}</td></tr>
                <tr><td><strong>LITROS:</strong></td><td>{safe(recarga.litros)}</td></tr>
                <tr><td><strong>CÓDIGO MÁQUINA:</strong></td><td>{safe(recarga.maquina.nombre if recarga.maquina else '')}</td></tr>
                <tr><td><strong>OBRA:</strong></td><td>{safe(recarga.obra.nombre if recarga.obra else '')}</td></tr>
                <tr><td><strong>CLIENTE:</strong></td><td>{safe(recarga.cliente.nombre if recarga.cliente else '')}</td></tr>
            </tbody>
        </table>
        <div>
            <table style='border-collapse: collapse; width: 100%; text-align: left;' border='0'>
                <tbody>
                    <tr><td><strong>Observaciones:</strong></td></tr>
                    <tr><td>{safe(recarga.observaciones)}</td></tr>
                </tbody>
            </table>
            <table style='border-collapse: collapse; width: 100%; text-align: left;' border='0'>
                <tbody>
                    <tr>
                        <td class='signature' style='width: 50%;'>Firma operador:</td>
                        <td style='white-space: nowrap;'>&nbsp;&nbsp;&nbsp;</td>
                        <td class='signature' style='width: 50%;'>Firma encargado reparto:</td>
                    </tr>
                    <tr>
                        <td style='width: 50%;'><strong>{safe(recarga.operador.usuario if recarga.operador else '')}</strong></td>
                        <td style='white-space: nowrap;'>&nbsp;</td>
                        <td style='width: 50%;'><strong>{safe(recarga.nombre)}</strong></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    </body>
    </html>
    """