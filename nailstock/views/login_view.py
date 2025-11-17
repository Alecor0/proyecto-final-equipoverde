from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class LoginView(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("NailStack - Login")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Título
        title = QLabel("NAILSTACK")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        
        subtitle = QLabel("Sistema de Gestión de Ferretería")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Formulario
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_frame.setFixedWidth(300)
        
        form_layout = QVBoxLayout()
        
        # Usuario
        usuario_layout = QVBoxLayout()
        usuario_label = QLabel("Usuario:")
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Ingrese su usuario")
        usuario_layout.addWidget(usuario_label)
        usuario_layout.addWidget(self.usuario_input)
        
        # Contraseña
        password_layout = QVBoxLayout()
        password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Botón
        self.login_btn = QPushButton("Iniciar Sesión")
        self.login_btn.clicked.connect(self.validar_login)
        
        form_layout.addLayout(usuario_layout)
        form_layout.addLayout(password_layout)
        form_layout.addWidget(self.login_btn)
        form_frame.setLayout(form_layout)
        
        # Agregar al layout principal
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(form_frame)
        
        self.setLayout(layout)
        
        # Enter para login
        self.usuario_input.returnPressed.connect(self.validar_login)
        self.password_input.returnPressed.connect(self.validar_login)
    
    def validar_login(self):
        usuario = self.usuario_input.text().strip()
        password = self.password_input.text().strip()
        
        if usuario.lower() == "admin" and password.lower() == "admin":
            self.on_login_success()