from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLineEdit, 
                             QHeaderView, QMessageBox, QDialog, QFormLayout,
                             QTextEdit, QLabel)
from PyQt6.QtCore import Qt
from ..models.proveedor_model import ProveedorModel
from ..controllers.proveedor_controller import ProveedorController
from ..utils.mensajes import Mensajes

class ProveedoresView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_proveedores()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar proveedores...")
        self.search_input.textChanged.connect(self.buscar_proveedores)
        
        btn_agregar = QPushButton("Agregar Proveedor")
        btn_agregar.clicked.connect(self.agregar_proveedor)
        
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_input)
        search_layout.addStretch()
        search_layout.addWidget(btn_agregar)
        
        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Teléfono", "Dirección", "Correo", "RFC", "Observaciones", "Acciones"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def cargar_proveedores(self):
        proveedores = ProveedorModel.obtener_proveedores()
        self.actualizar_tabla(proveedores)
    
    def buscar_proveedores(self):
        termino = self.search_input.text().strip()
        if termino:
            proveedores = ProveedorController.buscar_proveedores(termino)
            self.actualizar_tabla(proveedores)
        else:
            self.cargar_proveedores()
    
    def actualizar_tabla(self, proveedores):
        self.table.setRowCount(len(proveedores))
        
        for row, proveedor in enumerate(proveedores):
            self.table.setItem(row, 0, QTableWidgetItem(str(proveedor[0])))
            self.table.setItem(row, 1, QTableWidgetItem(proveedor[1]))
            self.table.setItem(row, 2, QTableWidgetItem(proveedor[2] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(proveedor[3] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(proveedor[4] or ""))
            self.table.setItem(row, 5, QTableWidgetItem(proveedor[5] or ""))
            
            # Observaciones (truncadas)
            observaciones = proveedor[6] or ""
            if len(observaciones) > 50:
                observaciones = observaciones[:50] + "..."
            self.table.setItem(row, 6, QTableWidgetItem(observaciones))
            
            # Acciones
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            btn_editar = QPushButton("Editar")
            btn_editar.clicked.connect(lambda checked, p=proveedor: self.editar_proveedor(p))
            
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.clicked.connect(lambda checked, p=proveedor: self.eliminar_proveedor(p))
            
            actions_layout.addWidget(btn_editar)
            actions_layout.addWidget(btn_eliminar)
            actions_widget.setLayout(actions_layout)
            
            self.table.setCellWidget(row, 7, actions_widget)
    
    def agregar_proveedor(self):
        dialog = ProveedorDialog(self)
        if dialog.exec():
            self.cargar_proveedores()
    
    def editar_proveedor(self, proveedor):
        dialog = ProveedorDialog(self, proveedor)
        if dialog.exec():
            self.cargar_proveedores()
    
    def eliminar_proveedor(self, proveedor):
        if Mensajes.confirmar(f"¿Está seguro de eliminar al proveedor {proveedor[1]}?", self):
            try:
                ProveedorModel.eliminar_proveedor(proveedor[0])
                Mensajes.mostrar_exito("Proveedor eliminado correctamente", self)
                self.cargar_proveedores()
            except Exception as e:
                Mensajes.mostrar_error(str(e), self)

class ProveedorDialog(QDialog):
    def __init__(self, parent=None, proveedor=None):
        super().__init__(parent)
        self.proveedor = proveedor
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Editar Proveedor" if self.proveedor else "Agregar Proveedor")
        self.setModal(True)
        self.setFixedWidth(500)
        
        layout = QFormLayout()
        
        # Campos
        self.nombre_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.correo_input = QLineEdit()
        self.rfc_input = QLineEdit()
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMaximumHeight(100)
        
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
        layout.addRow("Correo:", self.correo_input)
        layout.addRow("RFC:", self.rfc_input)
        layout.addRow("Observaciones:", self.observaciones_input)
        layout.addRow(btn_layout)
        
        # Cargar datos si es edición
        if self.proveedor:
            self.nombre_input.setText(self.proveedor[1])
            self.telefono_input.setText(self.proveedor[2] or "")
            self.direccion_input.setText(self.proveedor[3] or "")
            self.correo_input.setText(self.proveedor[4] or "")
            self.rfc_input.setText(self.proveedor[5] or "")
            self.observaciones_input.setText(self.proveedor[6] or "")
        
        self.setLayout(layout)
    
    def guardar(self):
        try:
            data = {
                'nombre': self.nombre_input.text().strip(),
                'telefono': self.telefono_input.text().strip(),
                'direccion': self.direccion_input.text().strip(),
                'correo': self.correo_input.text().strip(),
                'rfc': self.rfc_input.text().strip(),
                'observaciones': self.observaciones_input.toPlainText().strip()
            }
            
            if self.proveedor:
                ProveedorController.actualizar_proveedor(self.proveedor[0], **data)
                Mensajes.mostrar_exito("Proveedor actualizado correctamente", self)
            else:
                ProveedorController.agregar_proveedor(**data)
                Mensajes.mostrar_exito("Proveedor agregado correctamente", self)
            
            self.accept()
            
        except Exception as e:
            Mensajes.mostrar_error(str(e), self)