from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QLineEdit, QPushButton, QGridLayout, QMessageBox,
                           QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from database import add_professor, get_all_faculties

class AdminFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Set up the layout
        main_layout = QVBoxLayout(self)

        # Header
        header_label = QLabel("Admin Panel - Add Professor")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(header_label, 0, Qt.AlignCenter)

        # Form Frame
        form_frame = QFrame()
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(20, 10, 20, 10)
        form_layout.setSpacing(10)

        # First Name
        fname_label = QLabel("First Name:")
        form_layout.addWidget(fname_label, 0, 0, Qt.AlignLeft)
        
        self.fname_edit = QLineEdit()
        self.fname_edit.setMinimumWidth(300)
        form_layout.addWidget(self.fname_edit, 0, 1)

        # Last Name
        lname_label = QLabel("Last Name:")
        form_layout.addWidget(lname_label, 1, 0, Qt.AlignLeft)
        
        self.lname_edit = QLineEdit()
        self.lname_edit.setMinimumWidth(300)
        form_layout.addWidget(self.lname_edit, 1, 1)

        # Email
        email_label = QLabel("Email:")
        form_layout.addWidget(email_label, 2, 0, Qt.AlignLeft)
        
        self.email_edit = QLineEdit()
        self.email_edit.setMinimumWidth(300)
        form_layout.addWidget(self.email_edit, 2, 1)

        # Faculty (Office)
        office_label = QLabel("Faculty/Office:")
        form_layout.addWidget(office_label, 3, 0, Qt.AlignLeft)
        
        self.office_combo = QComboBox()
        self.office_combo.setMinimumWidth(300)
        form_layout.addWidget(self.office_combo, 3, 1)
        self.load_faculties()

        # Subject/Specialization
        subject_label = QLabel("Subject/Specialization:")
        form_layout.addWidget(subject_label, 4, 0, Qt.AlignLeft)
        
        self.subject_edit = QLineEdit()
        self.subject_edit.setMinimumWidth(300)
        form_layout.addWidget(self.subject_edit, 4, 1)

        # Configure grid column weights
        form_layout.setColumnStretch(1, 1)
        
        # Add form to main layout
        main_layout.addWidget(form_frame)

        # Buttons Frame
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)

        # Add Professor Button
        add_button = QPushButton("Add Professor")
        add_button.setFont(QFont("Arial", 10))
        add_button.clicked.connect(self.add_new_professor)
        button_layout.addWidget(add_button)

        # Back Button
        back_button = QPushButton("Back to Faculty List")
        back_button.setFont(QFont("Arial", 10))
        back_button.clicked.connect(lambda: controller.show_frame("facultylistframe"))
        button_layout.addWidget(back_button)
        
        # Add buttons to main layout
        main_layout.addWidget(button_frame, 0, Qt.AlignCenter)
        
        # Add some space at the bottom
        main_layout.addStretch(1)

    def load_faculties(self):
        """Load faculty offices into the combobox"""
        try:
            faculties = get_all_faculties()
            self.faculty_map = {f["office_name"]: f["office_id"] for f in faculties}
            self.office_combo.clear()
            self.office_combo.addItems(list(self.faculty_map.keys()))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load faculties: {str(e)}")

    def add_new_professor(self):
        """Handle adding a new professor"""
        f_name = self.fname_edit.text().strip()
        l_name = self.lname_edit.text().strip()
        email = self.email_edit.text().strip()
        office_name = self.office_combo.currentText()
        subject_id = self.subject_edit.text().strip()

        # Basic Validation
        if not f_name or not l_name or not email or not office_name:
            QMessageBox.critical(self, "Input Error", "First Name, Last Name, Email, and Faculty/Office are required.")
            return
        
        # Validate email format (simple check)
        if "@" not in email or "." not in email.split("@")[-1]:
            QMessageBox.critical(self, "Input Error", "Please enter a valid email address.")
            return

        office_id = self.faculty_map.get(office_name)
        if office_id is None:
            QMessageBox.critical(self, "Input Error", "Selected Faculty/Office is invalid.")
            return

        # Call database function
        success, message = add_professor(f_name, l_name, email, office_id, subject_id)

        if success:
            QMessageBox.information(self, "Success", message)
            # Clear form
            self.fname_edit.clear()
            self.lname_edit.clear()
            self.email_edit.clear()
            self.subject_edit.clear()
            # Navigate back to faculty list
            self.controller.show_frame("facultylistframe")
        else:
            QMessageBox.critical(self, "Database Error", message)


