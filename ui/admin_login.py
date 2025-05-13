from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QLineEdit, QPushButton, QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QCursor
from database import authenticate_admin

class AdminLoginFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Set background color
        self.setStyleSheet("background-color: #FFDD00;")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title at the top
        title_label = QLabel("Admin Login")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: black; background-color: #FFDD00;")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setContentsMargins(0, 100, 0, 20)
        main_layout.addWidget(title_label)
        
        # Login form container (white background)
        login_container = QFrame()
        login_container.setStyleSheet("background-color: white; border-radius: 10px;")
        login_layout = QGridLayout(login_container)
        login_layout.setContentsMargins(40, 40, 40, 40)
        login_layout.setSpacing(10)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 12))
        login_layout.addWidget(username_label, 0, 0, Qt.AlignLeft)
        
        self.username_edit = QLineEdit()
        self.username_edit.setMinimumWidth(300)
        self.username_edit.setFont(QFont("Arial", 12))
        login_layout.addWidget(self.username_edit, 0, 1, Qt.AlignLeft)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 12))
        login_layout.addWidget(password_label, 1, 0, Qt.AlignLeft)
        
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setMinimumWidth(300)
        self.password_edit.setFont(QFont("Arial", 12))
        login_layout.addWidget(self.password_edit, 1, 1, Qt.AlignLeft)
        
        # Button container
        button_container = QFrame()
        button_container.setStyleSheet("background-color: white;")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Arial", 12))
        cancel_btn.clicked.connect(lambda: controller.show_frame("departmentslistframe"))
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        button_layout.addWidget(cancel_btn)
        
        # Spacer
        button_layout.addStretch(1)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.setFont(QFont("Arial", 12))
        login_btn.clicked.connect(self.login)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00;
                color: black;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 100px;
                font-weight: bold;
                border: 2px solid #333333;
            }
            QPushButton:hover {
                background-color: #FFE840;
            }
        """)
        button_layout.addWidget(login_btn)
        
        # Add button container to login layout
        login_layout.addWidget(button_container, 2, 0, 1, 2)
        
        # Add login container to main layout, centered
        main_layout.addWidget(login_container, 0, Qt.AlignCenter)
        main_layout.addStretch(1)
        
        # Connect enter key to login
        self.password_edit.returnPressed.connect(self.login)
        self.username_edit.returnPressed.connect(self.login)
    
    def login(self):
        """Attempt to log in with provided credentials"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username or not password:
            QMessageBox.critical(self, "Login Error", "Please enter both username and password")
            return
        
        admin = authenticate_admin(username, password)
        
        if admin:
            # Authentication successful - show admin dashboard
            self.controller.admin_logged_in(admin)
            # Clear the password field for security
            self.password_edit.clear()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password") 