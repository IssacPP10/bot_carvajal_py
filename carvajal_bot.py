from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger_manager import LoggerManager
from telegram_bot import enviar_mensaje
from bs4 import BeautifulSoup
import config
import requests
import os
import time

logger = LoggerManager()

import os
from datetime import datetime

def login_carvajal(driver):
    try:
        logger.write_log("AUTH", f"Iniciando login | Hora de inicio: {config.get_hora()}", "INFO")
        
        # Navegación inicial
        driver.get(config.URL_LOGIN)
        
        # Selección de sistema (Monitor EDC)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "cmbSistemas"))
        ).find_element(By.XPATH, ".//option[contains(text(), 'Monitor EDC')]").click()
        logger.write_log("AUTH", "Navegación: Seleccionado 'Monitor EDC'", "INFO")
        
        # Ingreso de credenciales
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "txtUserEDC"))
        )
        driver.find_element(By.ID, "txtUserEDC").send_keys(config.USUARIO_CARVAJAL)
        driver.find_element(By.ID, "txtPassEDC").send_keys(config.CONTRASENA_CARVAJAL)
        driver.find_element(By.ID, "btnIngrear1").click()
        logger.write_log("AUTH", f"Credenciales enviadas | {config.USUARIO_CARVAJAL}/{config.CONTRASENA_CARVAJAL}", "INFO")
        
        # Verificación de login exitoso
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceBody_imBusqueda"))
        )
        logger.write_log("AUTH", "Login exitoso | Redirección completada", "INFO")
        
        enviar_mensaje("✅ <b>Autenticación exitosa</b>\n"
                      f"🕒 Hora: {config.get_hora()}")
        return True
        
    except Exception as e:
        # Guardar captura de pantalla
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join("screenshots", f"login_error_{timestamp}.png")
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(screenshot_path)
        
        error_msg = (f"❌ <b>Fallo de autenticación</b>\n"
                    f"⏰ Hora: {config.get_hora()}\n"
                    f"🔍 Error: {str(e)}\n"
                    f"📸 Captura: {screenshot_path}")
        enviar_mensaje(error_msg)
        logger.write_log("AUTH", f"Error durante login | Detalle: {str(e)} | Screenshot: {screenshot_path}", "ERROR")
        raise


def descargar_txts_rango(driver, carpeta_destino, fecha_inicio_str, fecha_fin_str):
    try:
        logger.write_log("DOWNLOAD", f"Parámetros recibidos: Carpeta={carpeta_destino} | Fechas={fecha_inicio_str}→{fecha_fin_str}", "DEBUG")
        # Notificación inicial
        enviar_mensaje(
            f"<b>╭─── DESCARGA DE OC CHEDRAUI</b>\n"
            f"<b>├</b> 🕒 INICIO: {config.get_hora()}\n"
            f"<b>├</b> 📅 Rango: {fecha_inicio_str} → {fecha_fin_str}"
        )

        # Esperar y contar resultados
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//table[contains(@id,'table-1')]//tbody"))
        )
        filas = driver.find_elements(By.XPATH, "//table[contains(@id,'table-1')]//tbody//tr")
        total = len(filas)
        
        if total == 0:
            mensaje = (f"<b>├</b> 🟠 NO SE ENCONTRARON OC\n"
                      f"<b>╰</b> ❌ FIN: {config.get_hora()}")
            enviar_mensaje(mensaje)
            logger.write_log("DOWNLOAD", f"Sin resultados para {fecha_inicio_str}-{fecha_fin_str}", "WARNING")
            return
        
        # Preparar sesión de descarga
        enviar_mensaje(f"<b>├</b> 🔍 OC ENCONTRADAS: <b>{total}</b>")
        logger.write_log("DOWNLOAD", f"Iniciando descarga de {total} archivos", "INFO")
        
        session = requests.Session()
        for ck in driver.get_cookies():
            session.cookies.set(ck["name"], ck["value"])
            
        headers = {
            "User-Agent": driver.execute_script("return navigator.userAgent;"),
            "Referer": driver.current_url
        }

        # Proceso de descarga
        for i, fila in enumerate(filas, 1):
            try:
                boton = fila.find_element(By.XPATH, ".//td[8]//button[@id='downloadTXT']")
                folio = boton.get_attribute("folio")
                
                # Descarga en dos pasos (con verificación de contenido)
                url_base = "https://edcweb.levicom.com.mx/DisplayFile/frmDisplay.aspx"
                payload = {
                    "codcliente": config.USUARIO_CARVAJAL,
                    "Ext": "INF",
                    "id": folio,
                    "force": "True"
                }
                
                # Intento de descarga directa
                response = session.post(url_base, data=payload, headers=headers, stream=True)
                response.raise_for_status()
                
                destino = os.path.join(carpeta_destino, f"{folio}.INF")
                
                if "html" not in response.headers.get("Content-Type", "").lower():
                    with open(destino, "wb") as f:
                        for chunk in response.iter_content(8192):
                            f.write(chunk)
                    logger.write_log("DOWNLOAD", f"OC {folio} descargada directamente", "INFO")
                else:
                    # Fallback a método con form1
                    soup = BeautifulSoup(response.text, "html.parser")
                    form = soup.find("form", id="form1")
                    if not form:
                        raise Exception("Formulario secundario no encontrado")
                    
                    url_secundaria = requests.compat.urljoin(url_base, form["action"])
                    data_secundario = {
                        inp["name"]: inp.get("value", "")
                        for inp in form.find_all("input")
                    }
                    
                    response_sec = session.post(url_secundaria, data=data_secundario, headers=headers, stream=True)
                    response_sec.raise_for_status()
                    
                    with open(destino, "wb") as f:
                        for chunk in response_sec.iter_content(8192):
                            f.write(chunk)
                    logger.write_log("DOWNLOAD", f"OC {folio} descargada vía form1", "INFO")
                
                enviar_mensaje(f"<b>├</b> ✅ OC {i}/{total}: {folio}.INF")
                time.sleep(0.5)
                
            except Exception as e:
                error_msg = f"<b>├</b> ❌ Error en OC {i}: {str(e)[:100]}..."
                enviar_mensaje(error_msg)
                logger.write_log("DOWNLOAD", f"Error en fila {i} | Folio: {folio} | Error: {str(e)}", "ERROR")

        # Notificación final
        enviar_mensaje(f"<b>╰</b> 🕒 FIN: {config.get_hora()}")
        logger.write_log("DOWNLOAD", f"Descarga completada en {carpeta_destino}", "INFO")
        
    except Exception as e:
        error_msg = (f"<b>╰</b> ❌ ERROR CRÍTICO\n"
                    f"⏰ Hora: {config.get_hora()}\n"
                    f"🔍 Detalle: {str(e)[:200]}")
        enviar_mensaje(error_msg)
        logger.write_log("DOWNLOAD", f"Error crítico: {str(e)}", "ERROR")
        raise

# def cerrar_sesion(driver):
#     try:
#         logger.write_log("AUTH", "Iniciando cierre de sesión", "INFO")
#         WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, "btnSalir"))
#         ).click()
#         logger.write_log("AUTH", "Sesión cerrada correctamente", "INFO")
#     except Exception as e:
#         logger.write_log("AUTH", f"Error al cerrar sesión: {str(e)}", "WARNING")