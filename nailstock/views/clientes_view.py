from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLineEdit, 
                             QHeaderView, QDialog, QFormLayout,
                             QLabel)
from ..models.cliente_model import ClienteModel
from ..controllers.cliente_controller import ClienteController
from ..utils.mensajes import Mensajes

class ClientesView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_clientes()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar clientes...")
        self.search_input.textChanged.connect(self.buscar_clientes)
        
        btn_agregar = QPushButton("Agregar Cliente")
        btn_agregar.clicked.connect(self.agregar_cliente)
        
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_input)
        search_layout.addStretch()
        search_layout.addWidget(btn_agregar)
        
        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Teléfono", "Dirección", "RFC", "Acciones"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def cargar_clientes(self):
        clientes = ClienteModel.obtener_clientes()
        self.actualizar_tabla(clientes)
    
    def buscar_clientes(self):
        termino = self.search_input.text().strip()
        if termino:
            clientes = ClienteController.buscar_clientes(termino)
            self.actualizar_tabla(clientes)
        else:
            self.cargar_clientes()
    
    def actualizar_tabla(self, clientes):
        self.table.setRowCount(len(clientes))
        
        for row, cliente in enumerate(clientes):
            self.table.setItem(row, 0, QTableWidgetItem(str(cliente[0])))
            self.table.setItem(row, 1, QTableWidgetItem(cliente[1]))
            self.table.setItem(row, 2, QTableWidgetItem(cliente[2] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(cliente[3] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(cliente[4] or ""))
            
            # Acciones
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            btn_editar = QPushButton("Editar")
            btn_editar.clicked.connect(lambda checked, c=cliente: self.editar_cliente(c))
            
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.clicked.connect(lambda checked, c=cliente: self.eliminar_cliente(c))
            
            actions_layout.addWidget(btn_editar)
            actions_layout.addWidget(btn_eliminar)
            actions_widget.setLayout(actions_layout)
            
            self.table.setCellWidget(row, 5, actions_widget)
    
    def agregar_cliente(self):
        dialog = ClienteDialog(self)
        if dialog.exec():
            self.cargar_clientes()
    
    def editar_cliente(self, cliente):
        dialog = ClienteDialog(self, cliente)
        if dialog.exec():
            self.cargar_clientes()
    
    def eliminar_cliente(self, cliente):
        if Mensajes.confirmar(f"¿Está seguro de eliminar al cliente {cliente[1]}?", self):
            try:
                ClienteModel.eliminar_cliente(cliente[0])
                Mensajes.mostrar_exito("Cliente eliminado correctamente", self)
                self.cargar_clientes()
            except Exception as e:
                Mensajes.mostrar_error(str(e), self)

class ClienteDialog(QDialog):
    def __init__(self, parent=None, cliente=None):
        super().__init__(parent)
        self.cliente = cliente
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Editar Cliente" if self.cliente else "Agregar Cliente")
        self.setModal(True)
        self.setFixedWidth(400)
        
        layout = QFormLayout()
        
        # Campos
        self.nombre_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.rfc_input = QLineEdit()
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_cancelar = QPushButton("Cancelar")
        
        btn_guardar.clicked.connect(self.guardar)
        btn_cancelar.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        
        # Agregar campos al layout
        layout.addRow("Nombre *:", self.nombre_input)
        layout.addRow("Teléfono:", self.telefono_input)
        layout.addRow("Dirección:", self.direccion_input)
        layout.addRow("RFC:", self.rfc_input)
        layout.addRow(btn_layout)
        
        # Cargar datos si es edición
        if self.cliente:
            self.nombre_input.setText(self.cliente[1])
            self.telefono_input.setText(self.cliente[2] or "")
            self.direccion_input.setText(self.cliente[3] or "")
            self.rfc_input.setText(self.cliente[4] or "")
        
        self.setLayout(layout)
    
    def guardar(self):
        try:
            data = {
                'nombre': self.nombre_input.text().strip(),
                'telefono': self.telefono_input.text().strip(),
                'direccion': self.direccion_input.text().strip(),
                'rfc': self.rfc_input.text().strip()
            }
            
            if self.cliente:
                ClienteController.actualizar_cliente(self.cliente[0], **data)
                Mensajes.mostrar_exito("Cliente actualizado correctamente", self)
            else:
                ClienteController.agregar_cliente(**data)
                Mensajes.mostrar_exito("Cliente agregado correctamente", self)
            
            self.accept()
            
        except Exception as e:
            Mensajes.mostrar_error(str(e), self)