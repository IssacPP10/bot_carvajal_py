from dotenv import load_dotenv
import os
import sys
from datetime import datetime

# Detectar si es ejecución en .exe (PyInstaller)
if getattr(sys, 'frozen', False):
    # Carpeta donde PyInstaller extrae los archivos
    base_path = sys._MEIPASS
else:
    # Carpeta donde está tu script .py
    base_path = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(base_path, ".env")
load_dotenv(env_path)

# ——— Credenciales ———
USUARIO_CARVAJAL = os.getenv("USUARIO_CARVAJAL")
CONTRASENA_CARVAJAL = os.getenv("CONTRASENA_CARVAJAL")

# ——— Plataforma Carvajal ———
URL_LOGIN = os.getenv("URL_LOGIN")

# Rutas de descarga
RUTA_DESCARGAS_CARVAJAL = os.getenv("RUTA_DESCARGAS_CARVAJAL")
RUTA_DESCARGAS_CARVAJAL_POR_DIA = os.getenv("RUTA_DESCARGAS_CARVAJAL_POR_DIA")

# ——— Opciones varias ———
TIEMPO_ESPERA_RESULTADOS = 5

# ——— Telegram Bot ———
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_hora():
    return datetime.now().strftime("%I:%M:%S.%f %p")
