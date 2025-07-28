from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import WebDriverException
import logging
from config import RUTA_DESCARGAS_CARVAJAL

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def configurar_navegador():
    try:
        options = EdgeOptions()
        
        # ======================
        # Configuración General (NO headless)
        # ======================
        # options.add_argument("--start-maximized")
        # options.add_argument("--force-device-scale-factor=1")

        # ======================
        # Configuración Headless (opcional - descomentá para activarlo)
        # ======================
        options.add_argument("--headless=new")  # Modo headless con nueva implementación
        options.add_argument("--window-size=1920,1080")  # Reemplaza --start-maximized
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")    

        # ======================
        # Prevención de detección (opcional)
        # ======================
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # User-Agent personalizado (opcional)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        options.add_argument(f"user-agent={user_agent}")

        # ======================
        # Configuración de descargas
        # ======================
        prefs = {
            "download.default_directory": RUTA_DESCARGAS_CARVAJAL,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.automatic_downloads": 1,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)

        # ======================
        # Inicialización del driver
        # ======================
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

        # Configuración adicional recomendada
        driver.set_page_load_timeout(30)

        logging.info("Navegador Microsoft Edge configurado correctamente")
        return driver

    except Exception as e:
        logging.error(f"Error al configurar el navegador Edge: {str(e)}")
        raise WebDriverException(f"No se pudo iniciar el navegador Edge: {str(e)}")
