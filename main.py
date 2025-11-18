import os
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

import sys

# --- Comprobación y elevación a administrador (solo Windows) ---
if os.name == "nt":
    import ctypes

    def is_user_admin() -> bool:
        """
        Verifica si el proceso actual se está ejecutando con privilegios de administrador.
        Devuelve True si es administrador, False en caso contrario.
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    if not is_user_admin():
        # Si no es administrador, intentar relanzar el script con privilegios elevados
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",          # Verbo para solicitar elevación
                sys.executable,   # Intérprete de Python actual
                f'"{sys.argv[0]}" {params}',
                None,
                1                 # Mostrar ventana normal
            )
        except Exception as e:
            # Si falla la elevación, mostrar un mensaje y salir con error
            ctypes.windll.user32.MessageBoxW(
                None,
                f"No se pudo ejecutar como administrador.\n\nDetalle: {e}",
                "NailStack - Error de permisos",
                0x00000010  # MB_ICONERROR
            )
        sys.exit(0)  # Terminar el proceso actual (no admin)
# --- Fin de comprobación de administrador ---
from PyQt6.QtWidgets import QApplication
from nailstock.database.db_connection import DBConnection
from nailstock.views.login_view import LoginView
from nailstock.views.main_window import MainWindow


class NailStackApp:
    def __init__(self):
        """
        Constructor de la aplicación principal.

        - Crea la instancia de QApplication (requerida por cualquier app PyQt).
        - Configura nombre, versión y organización de la aplicación.
        - Inicializa la conexión a la base de datos.
        """
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("NailStack")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("Ferretería NailStack")
        self.db_connection = DBConnection()

    def show_login(self):
        """
        Muestra la ventana de inicio de sesión.

        - Crea la vista de login, pasándole el callback `on_login_success`.
        - Llama a `show()` para hacer visible la ventana de login.
        """
        self.login_view = LoginView(self.on_login_success)
        self.login_view.show()

    def on_login_success(self):
        """
        Callback que se ejecuta cuando el login es exitoso.

        - Cierra la ventana de login.
        - Crea la ventana principal de la aplicación.
        - Muestra la ventana principal.
        """
        self.login_view.close()
        self.main_window = MainWindow()
        self.main_window.show()

    def run(self):
        """
        Inicia el ciclo principal de la aplicación.

        - Muestra primero la ventana de login.
        - Ejecuta el bucle de eventos de Qt (`app.exec()`).
        - Devuelve el código de salida de la aplicación.
        """
        self.show_login()
        return self.app.exec()


if __name__ == '__main__':
    # Punto de entrada de la aplicación:
    # - Crea la instancia de NailStackApp.
    # - Ejecuta la aplicación y pasa el código de salida a `sys.exit`.
    nailstack = NailStackApp()
    sys.exit(nailstack.run())
