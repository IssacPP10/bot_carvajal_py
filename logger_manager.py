import os
import sys
from datetime import datetime

class LoggerManager:
    _instance = None  # Singleton pattern

    def __new__(cls, base_path=None):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, base_path=None):
        if not self.__initialized:
            # Detectar si es ejecutable o script
            if getattr(sys, 'frozen', False):
                # Ejecutable generado con PyInstaller
                exe_path = os.path.dirname(sys.executable)
            else:
                # Script normal
                exe_path = os.path.dirname(os.path.abspath(__file__))

            self.base_path = base_path or os.path.join(exe_path, "logs")
            self.current_month = datetime.now().strftime("%Y-%m")
            self.log_folder = os.path.join(self.base_path, self.current_month)
            self.log_file = None
            self.initialize_logger()
            self.__initialized = True

    def initialize_logger(self):
        try:
            if not os.path.exists(self.base_path):
                os.makedirs(self.base_path)

            os.makedirs(self.log_folder, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_process_%H%M%S")
            log_filename = f"{timestamp}.log"
            self.log_file = os.path.join(self.log_folder, log_filename)

            self.write_log("SYSTEM", f"Logger inicializado | Archivo: {log_filename}", "INFO")

        except Exception as e:
            timestamp_fallback = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = os.path.join(self.base_path, f"fallback_{timestamp_fallback}.log")
            self.write_log("SYSTEM", f"Logger init failed: {str(e)}", "ERROR")

    def write_log(self, module, message, level="INFO"):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            log_entry = f"[{timestamp}] [{level}] [{module}] - {message}\n"

            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)

            return True
        except Exception as e:
            print(f"Error writing to log file: {str(e)}")
            return False

    def get_log_file_path(self):
        return self.log_file
