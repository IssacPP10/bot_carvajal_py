from navegador_chrome import configurar_navegador
#from navegador_edge import configurar_navegador
from carvajal_bot import login_carvajal
from descargas_oc import descargar_por_dia, descargar_por_semana
from telegram_bot import enviar_mensaje
from logger_manager import LoggerManager
from fechas import obtener_rango_semana, es_lunes, formatear_fecha
import config

logger = LoggerManager()

def generar_mensaje_inicio():
    """Genera el mensaje de inicio usando fechas.py"""
    inicio_semana, fin_semana = obtener_rango_semana()
    return (
        f"🚀 <b>INICIO DE PROCESO</b>\n"
        f"├ <b>Semana:</b> {formatear_fecha(inicio_semana)} → {formatear_fecha(fin_semana)}\n"
        f"╰ <b>Hora:</b> {config.get_hora()}"
    )

def ejecutar_proceso_descargas():
    driver = None
    try:
        # 1. Configuración y notificación
        logger.write_log("MAIN", "Iniciando proceso", "INFO")
        enviar_mensaje(generar_mensaje_inicio())

        # 2. Iniciar sesión
        driver = configurar_navegador()
        login_carvajal(driver)

        ruta_semanal = ''
        ruta_diaria = ''

        # 3. Descarga SEMANAL (solo lunes)
        
        if es_lunes():            
            ruta_semanal = descargar_por_semana(driver)
            enviar_mensaje(f"✅ <b>DESCARGA SEMANAL COMPLETADA</b>\n"
                        f"╰ <b>Ruta:</b> {ruta_semanal}")
        else:
            ruta_semanal = 'Omitida'
            enviar_mensaje("ℹ️ <b>No es lunes</b>\n"
                        "╰ <i>Descarga semanal omitida</i>")

        # 4. Descarga DIARIA
        # DESCOMENTAR PARA EJECUTAR LA DESCARGA DIARIA
        # ruta_diaria = descargar_por_dia(driver)
        # if ruta_diaria:
        #     enviar_mensaje(f"✅ <b>DESCARGA DIARIA COMPLETADA</b>\n"
        #                 f"╰ <b>Ruta:</b> {ruta_diaria}")
        # else:
        #     ruta_diaria = 'No ejecutada'

        # 5. Reporte final
        mensaje_final = (
            f"🏁 <b>PROCESO FINALIZADO</b>\n"
            f"├ <b>Semanal:</b> {ruta_semanal}\n"
            f"├ <b>Diaria:</b> {ruta_diaria}\n"
            f"╰ <b>Hora:</b> {config.get_hora()}"
        )
        enviar_mensaje(mensaje_final)
        logger.write_log("MAIN", "Proceso completado exitosamente", "INFO")


    except Exception as e:
        enviar_mensaje(
            f"❌ <b>ERROR</b>\n"
            f"├ <b>Tipo:</b> {type(e).__name__}\n"
            f"╰ <b>Detalle:</b> {str(e)[:150]}..."
        )
        logger.write_log("MAIN", f"Error: {str(e)}", "ERROR")
        raise

    finally:
        if driver:
            # cerrar_sesion(driver)
            driver.quit()

if __name__ == "__main__":
    ejecutar_proceso_descargas()