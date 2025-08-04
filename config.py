from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()


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