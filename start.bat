@echo off
:: Ir al directorio del proyecto
cd /d "C:\Users\PC\Documents\Carvajal_Bot"

:: Crear entorno virtual solo si no existe
if not exist venv (
    python -m venv venv
)

:: Activar entorno virtual
call venv\Scripts\activate

:: Instalar dependencias necesarias
pip install --upgrade pip >nul 2>&1
pip install selenium webdriver-manager requests beautifulsoup4 >nul 2>&1

:: Ejecutar el script principal
:: python main.py
:: pyinstaller --onefile --icon=bot.ico --name=CarvajalBot main.py
