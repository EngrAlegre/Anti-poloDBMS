from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QLineEdit, QPushButton, QGridLayout, QMessageBox,
                           QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
                           QFileDialog, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3
import os
from database import add_professor, update_professor, delete_professor, get_all_professors, get_all_faculties, get_professor_by_id

class FacultyManagementFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_faculty_id = None
        self.current_mode = "add"
        self.photo_path = None
        
        # Set background color
        self.setStyleSheet("background-color: #FFDD00;")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with back button and title
        header_container = QFrame()
        header_container.setStyleSheet("background-color: #FFDD00;")
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        # Back button
        back_btn = QPushButton("← Back to Dashboard")
        back_btn.setFont(QFont("Arial", 12))
        back_btn.clicked.connect(lambda: controller.show_frame("admindashboardframe"))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        header_layout.addWidget(back_btn, 0, Qt.AlignLeft)
        
        # Title label
        title_label = QLabel("Faculty Management")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title_label, 1, Qt.AlignCenter)
        
        # Add spacer to balance layout
        header_layout.addItem(QSpacerItem(back_btn.sizeHint().width(), 0, 
                                QSizePolicy.Fixed, QSizePolicy.Minimum))
        
        main_layout.addWidget(header_container)
        
        # Content container (white background)
        content_container = QFrame()
        content_container.setStyleSheet("background-color: white; border-radius: 10px;")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Form container
        form_container = QFrame()
        form_layout = QGridLayout(form_container)
        
        # Form title
        self.form_title = QLabel("Add New Faculty")
        self.form_title.setFont(QFont("Arial", 14, QFont.Bold))
        form_layout.addWidget(self.form_title, 0, 0, 1, 2)
        
        # First Name
        form_layout.addWidget(QLabel("First Name:"), 1, 0)
        self.first_name_entry = QLineEdit()
        form_layout.addWidget(self.first_name_entry, 1, 1)
        
        # Last Name
        form_layout.addWidget(QLabel("Last Name:"), 2, 0)
        self.last_name_entry = QLineEdit()
        form_layout.addWidget(self.last_name_entry, 2, 1)
        
        # Department
        form_layout.addWidget(QLabel("Department:"), 3, 0)
        self.dept_combo = QComboBox()
        form_layout.addWidget(self.dept_combo, 3, 1)
        
        # Email
        form_layout.addWidget(QLabel("Email:"), 4, 0)
        self.email_entry = QLineEdit()
        form_layout.addWidget(self.email_entry, 4, 1)
        
        # Phone
        form_layout.addWidget(QLabel("Phone:"), 5, 0)
        self.phone_entry = QLineEdit()
        self.phone_entry.setPlaceholderText("+63 XXX XXX XXXX or 09XX XXX XXXX")
        form_layout.addWidget(self.phone_entry, 5, 1)
        
        # Specialty
        form_layout.addWidget(QLabel("Specialty:"), 6, 0)
        self.specialty_entry = QLineEdit()
        form_layout.addWidget(self.specialty_entry, 6, 1)
        
        # Photo
        form_layout.addWidget(QLabel("Photo:"), 7, 0)
        photo_container = QFrame()
        photo_layout = QHBoxLayout(photo_container)
        photo_layout.setContentsMargins(0, 0, 0, 0)
        
        self.photo_btn = QPushButton("Choose Photo")
        self.photo_btn.clicked.connect(self.choose_photo)
        self.photo_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        photo_layout.addWidget(self.photo_btn)
        
        self.photo_label = QLabel("No photo selected")
        photo_layout.addWidget(self.photo_label, 1)
        
        form_layout.addWidget(photo_container, 7, 1)
        
        # Buttons container
        buttons_container = QFrame()
        buttons_layout = QHBoxLayout(buttons_container)
        
        # Reset button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_form)
        self.reset_btn.setStyleSheet("""
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
        buttons_layout.addWidget(self.reset_btn)
        
        # Spacer
        buttons_layout.addStretch(1)
        
        # Save button
        self.save_btn = QPushButton("Add Faculty")
        self.save_btn.clicked.connect(self.save_faculty)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00;
                color: black;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 120px;
                font-weight: bold;
                border: 2px solid #333333;
            }
            QPushButton:hover {
                background-color: #FFE840;
            }
        """)
        buttons_layout.addWidget(self.save_btn)
        
        form_layout.addWidget(buttons_container, 8, 0, 1, 2)
        
        content_layout.addWidget(form_container)
        
        # Table container
        table_container = QFrame()
        table_layout = QVBoxLayout(table_container)
        
        # Table title
        table_title = QLabel("Faculty List")
        table_title.setFont(QFont("Arial", 14, QFont.Bold))
        table_layout.addWidget(table_title)
        
        # Faculty table
        self.faculty_table = QTableWidget()
        self.faculty_table.setColumnCount(7)
        self.faculty_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Department", "Email", "Phone", "Specialty"])
        self.faculty_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.faculty_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.faculty_table.setSelectionMode(QTableWidget.SingleSelection)
        self.faculty_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.faculty_table.clicked.connect(self.select_faculty)
        table_layout.addWidget(self.faculty_table)
        
        # Delete button
        self.delete_btn = QPushButton("Delete Selected Faculty")
        self.delete_btn.clicked.connect(self.delete_faculty)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #F44336;
            }
            QPushButton:disabled {
                background-color: #AAAAAA;
                color: #DDDDDD;
            }
        """)
        table_layout.addWidget(self.delete_btn, 0, Qt.AlignRight)
        
        content_layout.addWidget(table_container)
        
        # Add content container to main layout
        main_layout.addWidget(content_container)
    
    def load_departments(self):
        """Load departments into combo box"""
        self.dept_combo.clear()
        try:
            faculties = get_all_faculties()
            for faculty in faculties:
                self.dept_combo.addItem(faculty['office_name'])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load departments: {str(e)}")
    
    def load_faculty_list(self):
        """Load faculty list into table"""
        self.faculty_table.setRowCount(0)
        try:
            professors = get_all_professors()
            self.faculty_table.setRowCount(len(professors))
            
            for i, prof in enumerate(professors):
                self.faculty_table.setItem(i, 0, QTableWidgetItem(str(prof['faculty_id'])))
                self.faculty_table.setItem(i, 1, QTableWidgetItem(prof['first_name']))
                self.faculty_table.setItem(i, 2, QTableWidgetItem(prof['last_name']))
                self.faculty_table.setItem(i, 3, QTableWidgetItem(prof['department_name']))
                self.faculty_table.setItem(i, 4, QTableWidgetItem(prof['email']))
                self.faculty_table.setItem(i, 5, QTableWidgetItem(prof['phone']))
                self.faculty_table.setItem(i, 6, QTableWidgetItem(prof['subject_id']))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load faculty list: {str(e)}")
    
    def select_faculty(self):
        """Handle faculty selection from table"""
        selected_rows = self.faculty_table.selectedIndexes()
        if selected_rows:
            self.delete_btn.setEnabled(True)
            row = selected_rows[0].row()
            self.selected_faculty_id = int(self.faculty_table.item(row, 0).text())
            self.current_mode = "edit"
            
            try:
                # Get faculty details
                faculty = get_professor_by_id(self.selected_faculty_id)
                
                if faculty:
                    # Update form with faculty data
                    self.form_title.setText("Edit Faculty")
                    self.save_btn.setText("Update Faculty")
                    
                    self.first_name_entry.setText(faculty['first_name'])
                    self.last_name_entry.setText(faculty['last_name'])
                    
                    # Set department
                    dept_index = self.dept_combo.findText(faculty['department_name'])
                    if dept_index >= 0:
                        self.dept_combo.setCurrentIndex(dept_index)
                    
                    self.email_entry.setText(faculty['email'])
                    # Get phone from previous load_faculty_list operation
                    row = selected_rows[0].row()
                    self.phone_entry.setText(self.faculty_table.item(row, 5).text())
                    self.specialty_entry.setText(faculty['subject_id'])
                    
                    # Handle photo, if needed in the future
                    if 'photo_url' in faculty and faculty['photo_url']:
                        self.photo_path = faculty['photo_url']
                        self.photo_label.setText(os.path.basename(self.photo_path))
                    else:
                        self.photo_path = None
                        self.photo_label.setText("No photo")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load faculty details: {str(e)}")
        else:
            self.delete_btn.setEnabled(False)
            self.selected_faculty_id = None
            self.current_mode = "add"
            self.form_title.setText("Add New Faculty")
            self.save_btn.setText("Add Faculty")
            self.reset_form()
    
    def reset_form(self):
        """Reset the form to add new faculty mode"""
        self.first_name_entry.clear()
        self.last_name_entry.clear()
        self.email_entry.clear()
        self.phone_entry.clear()
        self.specialty_entry.clear()
        if self.dept_combo.count() > 0:
            self.dept_combo.setCurrentIndex(0)
        
        self.photo_path = None
        self.photo_label.setText("No photo selected")
        
        self.selected_faculty_id = None
        self.current_mode = "add"
        self.save_btn.setText("Add Faculty")
        self.delete_btn.setEnabled(False)
        
        # Deselect any selected row
        self.faculty_table.clearSelection()
    
    def choose_photo(self):
        """Open file dialog to choose a faculty photo"""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.photo_path = selected_files[0]
                self.photo_label.setText(os.path.basename(self.photo_path))
    
    def save_faculty(self):
        """Save or update faculty information"""
        # Validate inputs
        first_name = self.first_name_entry.text().strip()
        last_name = self.last_name_entry.text().strip()
        department = self.dept_combo.currentText()
        email = self.email_entry.text().strip()
        phone = self.phone_entry.text().strip()
        specialty = self.specialty_entry.text().strip()
        
        if not first_name or not last_name or not department:
            QMessageBox.warning(self, "Validation Error", "First name, last name, and department are required")
            return
        
        try:
            if self.current_mode == "add":
                # Add new faculty
                success, msg = add_professor(
                    first_name, last_name, email, phone, department, specialty, 
                    photo_url=self.photo_path
                )
                
                if success:
                    QMessageBox.information(self, "Success", "Faculty added successfully")
                    self.reset_form()
                else:
                    QMessageBox.warning(self, "Error", msg)
            else:
                # Update existing faculty
                success, msg = update_professor(
                    self.selected_faculty_id, first_name, last_name, 
                    email, phone, department, specialty, photo_url=self.photo_path
                )
                
                if success:
                    QMessageBox.information(self, "Success", "Faculty updated successfully")
                    self.reset_form()
                else:
                    QMessageBox.warning(self, "Error", msg)
            
            # Refresh faculty list
            self.load_faculty_list()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save faculty: {str(e)}")
    
    def delete_faculty(self):
        """Delete the selected faculty"""
        if not self.selected_faculty_id:
            return
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this faculty member?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                success, msg = delete_professor(self.selected_faculty_id)
                
                if success:
                    QMessageBox.information(self, "Success", "Faculty deleted successfully")
                    self.reset_form()
                    self.load_faculty_list()
                else:
                    QMessageBox.warning(self, "Error", msg)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete faculty: {str(e)}")
    
    def on_show(self):
        """Called when frame is shown"""
        self.load_departments()
        self.load_faculty_list()