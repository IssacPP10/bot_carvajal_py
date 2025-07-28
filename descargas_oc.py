from gestor_rutas import preparar_carpeta_limpiar_si_existe, limpiar_carpeta_si_existe
from carvajal_bot import descargar_txts_rango
from logger_manager import LoggerManager
from fechas import obtener_rango_semana, obtener_fecha_actual, obtener_fecha_ayer,formatear_fecha
import config

logger = LoggerManager()

def ejecutar_descarga(driver, ruta_descarga, fecha_inicio, fecha_fin):
    """
    Función centralizada para manejar el proceso completo de descarga
    """
    try:
        # 1. Configurar todos los filtros
        from buscador import (
            abrir_filtros,
            seleccionar_cadena,
            configurar_filtros_fecha,
            ejecutar_busqueda
        )
        
        logger.write_log("DESCARGA", "Abriendo panel de filtros...", "INFO")
        abrir_filtros(driver)
        
        logger.write_log("DESCARGA", "Seleccionando cadena CHEDRAUI...", "INFO")
        seleccionar_cadena(driver)
        
        # Paso 1: Configurar filtros con fechas
        logger.write_log("DESCARGA", f"Configurando filtros para {fecha_inicio} a {fecha_fin}", "INFO")
        configurar_filtros_fecha(driver, formatear_fecha(fecha_inicio), formatear_fecha(fecha_fin))
        
        # Paso 2: Ejecutar búsqueda
        logger.write_log("DESCARGA", "Ejecutando búsqueda...", "INFO")
        ejecutar_busqueda(driver)

        # Paso 3: Procesar descarga
        logger.write_log("DESCARGA", f"Iniciando descarga en {ruta_descarga}", "INFO")
        descargar_txts_rango(driver, ruta_descarga, formatear_fecha(fecha_inicio), formatear_fecha(fecha_fin))
        
        logger.write_log("DESCARGA", "Proceso de descarga completado", "INFO")
        return True
        
    except Exception as e:
        logger.write_log("DESCARGA", f"Error en el proceso: {str(e)}", "ERROR")
        raise

def descargar_por_semana(driver):
    try:
        # Configuración inicial
        ruta_base = config.RUTA_DESCARGAS_CARVAJAL
        fecha_inicio, fecha_fin = obtener_rango_semana()
        
        logger.write_log("SEMANAL", f"Preparando descarga semanal ({fecha_inicio} a {fecha_fin})", "INFO")
        limpiar_carpeta_si_existe(ruta_base)
        
        # Ejecutar descarga
        ejecutar_descarga(driver, ruta_base, fecha_inicio, fecha_fin)
        
        logger.write_log("SEMANAL", "Descarga semanal completada", "INFO")
        return ruta_base
        
    except Exception as e:
        logger.write_log("SEMANAL", f"Fallo en descarga semanal: {str(e)}", "ERROR")
        raise

def descargar_por_dia(driver, fecha=None):
    try:
        # Configuración inicial
        fecha = fecha or obtener_fecha_ayer()
        ruta_base = config.RUTA_DESCARGAS_CARVAJAL_POR_DIA
        
        logger.write_log("DIARIA", f"Preparando descarga diaria para {fecha}", "INFO")
        carpeta_destino = preparar_carpeta_limpiar_si_existe(ruta_base, formatear_fecha(fecha))
        
        # Ejecutar descarga
        ejecutar_descarga(driver, carpeta_destino, fecha, fecha)
        
        logger.write_log("DIARIA", "Descarga diaria completada", "INFO")
        return carpeta_destino
        
    except Exception as e:
        logger.write_log("DIARIA", f"Fallo en descarga diaria: {str(e)}", "ERROR")
        raise