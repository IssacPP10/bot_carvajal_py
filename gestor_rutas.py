import os
import shutil
from datetime import datetime

def preparar_carpeta_descarga(base_path, fecha_inicio, fecha_fin):
    nombre_base = f"{fecha_inicio}_{fecha_fin}"
    ruta_objetivo = os.path.join(base_path, nombre_base)

    if not os.path.exists(ruta_objetivo):
        os.makedirs(ruta_objetivo)
        return ruta_objetivo
    else:
        timestamp = datetime.now().strftime("%H%M%S")
        nuevo_nombre = f"{nombre_base}_{timestamp}"
        nueva_ruta = os.path.join(base_path, nuevo_nombre)
        os.makedirs(nueva_ruta)
        return nueva_ruta

def preparar_carpeta_limpiar_si_existe(base_path, nombre):
    ruta = os.path.join(base_path, nombre)
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    else:
        for archivo in os.listdir(ruta):
            archivo_path = os.path.join(ruta, archivo)
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)
    return ruta

def limpiar_carpeta_si_existe(ruta):
    if os.path.exists(ruta):
        for archivo in os.listdir(ruta):
            archivo_path = os.path.join(ruta, archivo)
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)
