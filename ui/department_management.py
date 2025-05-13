from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLineEdit, QMessageBox, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QSpacerItem, QSizePolicy,
                           QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3
from database import get_all_departments, add_department, update_department, delete_department

class DepartmentManagementFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_dept_id = None
        self.current_mode = "add"
        
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
                border: 2px solid #FFDD00;
            }
            QPushButton:hover {
                background-color: #555555;
                border: 2px solid white;
            }
        """)
        header_layout.addWidget(back_btn, 0, Qt.AlignLeft)
        
        # Title label
        title_label = QLabel("Department Management")
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
        form_title = QLabel("Add New Department")
        form_title.setFont(QFont("Arial", 14, QFont.Bold))
        form_layout.addWidget(form_title, 0, 0, 1, 2)
        
        # Department Name
        form_layout.addWidget(QLabel("Department Name:"), 1, 0)
        self.name_entry = QLineEdit()
        form_layout.addWidget(self.name_entry, 1, 1)
        
        # Building Number
        form_layout.addWidget(QLabel("Building Number:"), 2, 0)
        self.building_entry = QLineEdit()
        form_layout.addWidget(self.building_entry, 2, 1)
        
        # Room Number
        form_layout.addWidget(QLabel("Room Number:"), 3, 0)
        self.room_entry = QLineEdit()
        form_layout.addWidget(self.room_entry, 3, 1)
        
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
        self.save_btn = QPushButton("Add Department")
        self.save_btn.clicked.connect(self.save_department)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00;
                color: black;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 150px;
                font-weight: bold;
                border: 2px solid #333333;
            }
            QPushButton:hover {
                background-color: #FFE840;
            }
        """)
        buttons_layout.addWidget(self.save_btn)
        
        form_layout.addWidget(buttons_container, 4, 0, 1, 2)
        
        content_layout.addWidget(form_container)
        
        # Table container
        table_container = QFrame()
        table_layout = QVBoxLayout(table_container)
        
        # Table title
        table_title = QLabel("Department List")
        table_title.setFont(QFont("Arial", 14, QFont.Bold))
        table_layout.addWidget(table_title)
        
        # Department table
        self.dept_table = QTableWidget()
        self.dept_table.setColumnCount(4)
        self.dept_table.setHorizontalHeaderLabels(["ID", "Department Name", "Building", "Room"])
        self.dept_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dept_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.dept_table.setSelectionMode(QTableWidget.SingleSelection)
        self.dept_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.dept_table.clicked.connect(self.select_department)
        table_layout.addWidget(self.dept_table)
        
        # Action buttons container
        action_container = QFrame()
        action_layout = QHBoxLayout(action_container)
        
        # Delete button
        self.delete_btn = QPushButton("Delete Selected Department")
        self.delete_btn.clicked.connect(self.delete_department)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #F44336;
            }
            QPushButton:disabled {
                background-color: #AAAAAA;
                color: #DDDDDD;
            }
        """)
        action_layout.addWidget(self.delete_btn, 0, Qt.AlignRight)
        
        table_layout.addWidget(action_container)
        
        content_layout.addWidget(table_container)
        
        # Add content container to main layout
        main_layout.addWidget(content_container)
    
    def load_departments(self):
        """Load departments into table"""
        self.dept_table.setRowCount(0)
        try:
            departments = get_all_departments()
            self.dept_table.setRowCount(len(departments))
            
            for i, dept in enumerate(departments):
                self.dept_table.setItem(i, 0, QTableWidgetItem(str(dept['office_id'])))
                self.dept_table.setItem(i, 1, QTableWidgetItem(dept['office_name']))
                
                # Convert building number to string (handling None values)
                building_num = dept['building_num']
                building_str = str(building_num) if building_num is not None else ""
                self.dept_table.setItem(i, 2, QTableWidgetItem(building_str))
                
                # Convert room number to string (handling None values)
                room_num = dept['room_num']
                room_str = str(room_num) if room_num is not None else ""
                self.dept_table.setItem(i, 3, QTableWidgetItem(room_str))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load departments: {str(e)}")
    
    def select_department(self):
        """Handle department selection from table"""
        selected_rows = self.dept_table.selectedIndexes()
        if selected_rows:
            row = selected_rows[0].row()
            dept_id = int(self.dept_table.item(row, 0).text())
            self.selected_dept_id = dept_id
            self.delete_btn.setEnabled(True)
            
            # Load department data into form
            name = self.dept_table.item(row, 1).text()
            building = self.dept_table.item(row, 2).text()
            room = self.dept_table.item(row, 3).text()
            
            self.name_entry.setText(name)
            self.building_entry.setText(building)
            self.room_entry.setText(room)
            
            # Update UI for edit mode
            self.current_mode = "edit"
            self.save_btn.setText("Update Department")
        else:
            self.selected_dept_id = None
            self.delete_btn.setEnabled(False)
    
    def reset_form(self):
        """Reset the form to add new department mode"""
        self.name_entry.clear()
        self.building_entry.clear()
        self.room_entry.clear()
        
        self.selected_dept_id = None
        self.current_mode = "add"
        self.save_btn.setText("Add Department")
        self.delete_btn.setEnabled(False)
        
        # Deselect any selected row
        self.dept_table.clearSelection()
    
    def save_department(self):
        """Save or update department information"""
        # Validate inputs
        name = self.name_entry.text().strip()
        building = self.building_entry.text().strip()
        room = self.room_entry.text().strip()
        
        if not name or not building or not room:
            QMessageBox.warning(self, "Validation Error", "All fields are required")
            return
        
        try:
            if self.current_mode == "add":
                # Add new department
                success, msg = add_department(name, building, room)
                
                if success:
                    QMessageBox.information(self, "Success", "Department added successfully")
                    self.reset_form()
                else:
                    QMessageBox.warning(self, "Error", msg)
            else:
                # Update existing department
                success, msg = update_department(self.selected_dept_id, name, building, room)
                
                if success:
                    QMessageBox.information(self, "Success", "Department updated successfully")
                    self.reset_form()
                else:
                    QMessageBox.warning(self, "Error", msg)
            
            # Refresh department list
            self.load_departments()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save department: {str(e)}")
    
    def delete_department(self):
        """Delete the selected department"""
        if not self.selected_dept_id:
            return
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this department? " +
                                   "This will also delete all faculty members associated with this department.",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                success, msg = delete_department(self.selected_dept_id)
                
                if success:
                    QMessageBox.information(self, "Success", "Department deleted successfully")
                    self.reset_form()
                    self.load_departments()
                else:
                    QMessageBox.warning(self, "Error", msg)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete department: {str(e)}")
    
    def on_show(self):
        """Called when frame is shown"""
        self.load_departments() 