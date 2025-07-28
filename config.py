from datetime import datetime

# ——— Credenciales ———
USUARIO_CARVAJAL = "3395"
CONTRASENA_CARVAJAL = "t57973"

# ——— Plataforma Carvajal ———
URL_LOGIN = "https://contingencia.carvajaltys.mx/"

# Rutas de descarga
RUTA_DESCARGAS_CARVAJAL = r"\\Srvcomplan\oc"
RUTA_DESCARGAS_CARVAJAL_POR_DIA = r"\\10.79.1.210\Users\ricardo.puentes\Downloads\OC_por_dia"

# ——— Opciones varias ———
TIEMPO_ESPERA_RESULTADOS = 5

# ——— Telegram Bot ———
TELEGRAM_BOT_TOKEN = "8120633832:AAFP5lXg5AXwF9lLag3ctyEDhTVODjYemTg"
TELEGRAM_CHAT_ID = "8145443131"

def get_hora():
    return datetime.now().strftime("%I:%M:%S.%f %p")