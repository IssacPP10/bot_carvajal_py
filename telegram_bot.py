import requests
import config

def enviar_mensaje(mensaje):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()  # lanza error si la respuesta no es 200
        return response
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al enviar mensaje a Telegram: {e}")
        return None
