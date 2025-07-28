import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from logger_manager import LoggerManager
import config
import time
from datetime import datetime

logger = LoggerManager()

def abrir_filtros(driver):
    """Abre el panel de filtros solo si aún está oculto, evitando errores por doble clic en el toggle"""
    try:
        logger.write_log("BUSCADOR", "Verificando visibilidad del panel de filtros...", "INFO")

        panel_filtros = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "item_busq"))
        )

        # Validar si el panel está visible (no tiene display: none)
        if panel_filtros.value_of_css_property("display") != "none":
            logger.write_log("BUSCADOR", "Panel de filtros ya estaba abierto. No se hace nada.", "INFO")
            return

        logger.write_log("BUSCADOR", "Panel de filtros está cerrado. Procediendo a abrir...", "INFO")

        # Buscar botón de imagen dentro del <a> y hacer clic
        boton_img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceBody_imBusqueda"))
        )
        boton_a = boton_img.find_element(By.XPATH, "./ancestor::a")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_img)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", boton_a)

        # Esperar a que el panel se abra (display: block o similar)
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "item_busq").value_of_css_property("display") != "none"
        )
        logger.write_log("BUSCADOR", "Panel de filtros abierto correctamente.", "INFO")

    except Exception as e:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        driver.save_screenshot(f"error_abrir_filtros_{timestamp}.png")
        logger.write_log("BUSCADOR", f"Error al abrir filtros: {str(e)}", "ERROR")
        raise


def seleccionar_cadena(driver, cadena="CHEDRAUI"):
    """Selecciona la cadena comercial en los filtros"""
    try:        
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceBody_ddlCadena"))
        ).find_element(By.XPATH, f".//option[contains(text(), '{cadena}')]").click()
    except Exception as e:
        logger.write_log("BUSCADOR", "Fallo en función: seleccionar_cadena", "ERROR")
        logger.write_log("BUSCADOR", f"Error seleccionando cadena: {str(e)}", "ERROR")
        raise

def configurar_filtros_fecha(driver, fecha_inicio, fecha_fin):
    """Configura los filtros de fecha y valida que se apliquen correctamente."""
    try:
        logger.write_log("BUSCADOR", f"Configurando fechas: desde='{fecha_inicio}', hasta='{fecha_fin}'", "INFO")

        # # Validar formato de fecha: dd-mm-aaaa
        # formato_fecha = re.compile(r"^\d{2}-\d{2}-\d{4}$")
        # if not formato_fecha.match(fecha_inicio) or not formato_fecha.match(fecha_fin):
        #     raise ValueError(f"Formato de fecha inválido. Se esperaba dd-mm-aaaa. Recibido: desde='{fecha_inicio}', hasta='{fecha_fin}'")

        # Esperar que los elementos estén presentes
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "FechaDesde")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fechaHasta")))

        # Establecer las fechas usando JavaScript (modo headless seguro)
        driver.execute_script("document.getElementById('FechaDesde').value = arguments[0];", fecha_inicio)
        driver.execute_script("document.getElementById('fechaHasta').value = arguments[0];", fecha_fin)

        time.sleep(0.5)  # Pequeña pausa para estabilidad

        # Leer los valores reales para validar
        valor_desde = driver.execute_script("return document.getElementById('FechaDesde').value;")
        valor_hasta = driver.execute_script("return document.getElementById('fechaHasta').value;")

        logger.write_log("BUSCADOR", f"Fechas establecidas en el DOM: desde='{valor_desde}', hasta='{valor_hasta}'", "INFO")

        if not valor_desde or not valor_hasta:
            raise ValueError(f"Fechas no establecidas correctamente: desde='{valor_desde}', hasta='{valor_hasta}'")

    except Exception as e:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        driver.save_screenshot(f"error_fechas_{timestamp}.png")
        logger.write_log("BUSCADOR", "Fallo en función: configurar_filtros_fecha", "ERROR")
        logger.write_log("BUSCADOR", f"Error configurando fechas: {str(e)}", "ERROR")
        raise

def ejecutar_busqueda(driver):
    """Ejecuta la búsqueda luego de que los filtros estén configurados"""
    try:
        buscar_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "buscarDocs"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buscar_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", buscar_btn)

        # Espera a que se actualice la tabla con resultados
        time.sleep(config.TIEMPO_ESPERA_RESULTADOS)

        div_table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "DivTable-1"))
        )
        label_socio = div_table.find_element(By.ID, "labelEDISocio")
        texto_socio = label_socio.text.strip()

        if texto_socio != "CHEDRAUI":
            raise ValueError(f"Validación fallida: Se esperaba 'CHEDRAUI', pero se encontró '{texto_socio}'")

        configurar_paginacion(driver)

    except Exception as e:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        driver.save_screenshot(f"error_busqueda_{timestamp}.png")
        logger.write_log("BUSCADOR", "Fallo en función: ejecutar_busqueda", "ERROR")
        logger.write_log("BUSCADOR", f"Error en búsqueda: {str(e)}", "ERROR")
        raise


def configurar_paginacion(driver, valor="-1"):
    """Configura la paginación para mostrar todos los resultados"""
    try:
        logger.write_log("BUSCADOR", "Configurando paginación a 'Todos'", "INFO")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "selectRegistros"))
        )
        select_registros = Select(driver.find_element(By.ID, "selectRegistros"))
        select_registros.select_by_value(valor)
        time.sleep(1)

        # Validación: confirmar que "TODOS" esté seleccionado
        selected_option = select_registros.first_selected_option.text.strip().upper()
        if "TODOS" not in selected_option:
            raise ValueError(f"No se seleccionó la opción 'TODOS'. Seleccionado: {selected_option}")
    except Exception as e:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        driver.save_screenshot(f"error_busqueda_{timestamp}.png")
        logger.write_log("BUSCADOR", "Fallo en función: configurar_paginacion", "ERROR")
        logger.write_log("BUSCADOR", f"Error configurando paginación: {str(e)}", "ERROR")
        raise