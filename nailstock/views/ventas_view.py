# Arleth. Pendiente.

from PyQt6.QtWidgets import QWidget, QVBoxLayout
class VentasView(QWidget):
    def __init__(self):
        super().__init__()
        self.productos_venta = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()        
        self.setLayout(layout)
    