from datetime import datetime, timedelta

def obtener_rango_semana():
    fecha_actual = datetime.now().date()
    # Hoy hace una semana (7 días atrás)
    fecha_inicio = fecha_actual - timedelta(days=7)
    # Ayer
    fecha_fin = fecha_actual - timedelta(days=1)
    return fecha_inicio, fecha_fin

def obtener_fecha_actual():
    return datetime.now().date()

def formatear_fecha(fecha):
    return fecha.strftime("%Y-%m-%d")

def obtener_fecha_ayer():
    return (datetime.now() - timedelta(days=1)).date()

def es_lunes(fecha=None):
    """Verifica si la fecha actual (o la proporcionada) es lunes"""
    fecha = fecha or obtener_fecha_actual()
    return fecha.weekday() == 0  # 0=Lunes, 1=Martes, ..., 6=Domingo