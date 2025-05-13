from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLineEdit, QMessageBox, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QSpacerItem, QSizePolicy,
                           QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3
from database import get_all_courses, add_course, update_course, delete_course

class CourseManagementFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_course_code = None
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
        title_label = QLabel("Course Management")
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
        form_title = QLabel("Add New Course")
        form_title.setFont(QFont("Arial", 14, QFont.Bold))
        form_layout.addWidget(form_title, 0, 0, 1, 2)
        
        # Course Code
        form_layout.addWidget(QLabel("Course Code:"), 1, 0)
        self.code_entry = QLineEdit()
        form_layout.addWidget(self.code_entry, 1, 1)
        
        # Course Name
        form_layout.addWidget(QLabel("Course Name:"), 2, 0)
        self.name_entry = QLineEdit()
        form_layout.addWidget(self.name_entry, 2, 1)
        
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
        self.save_btn = QPushButton("Add Course")
        self.save_btn.clicked.connect(self.save_course)
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
        
        form_layout.addWidget(buttons_container, 3, 0, 1, 2)
        
        content_layout.addWidget(form_container)
        
        # Table container
        table_container = QFrame()
        table_layout = QVBoxLayout(table_container)
        
        # Table title
        table_title = QLabel("Course List")
        table_title.setFont(QFont("Arial", 14, QFont.Bold))
        table_layout.addWidget(table_title)
        
        # Course table
        self.course_table = QTableWidget()
        self.course_table.setColumnCount(2)
        self.course_table.setHorizontalHeaderLabels(["Course Code", "Course Name"])
        self.course_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.course_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.course_table.setSelectionMode(QTableWidget.SingleSelection)
        self.course_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.course_table.clicked.connect(self.select_course)
        table_layout.addWidget(self.course_table)
        
        # Action buttons container
        action_container = QFrame()
        action_layout = QHBoxLayout(action_container)
        
        # Delete button
        self.delete_btn = QPushButton("Delete Selected Course")
        self.delete_btn.clicked.connect(self.delete_course)
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
        action_layout.addWidget(self.delete_btn, 0, Qt.AlignRight)
        
        table_layout.addWidget(action_container)
        
        content_layout.addWidget(table_container)
        
        # Add content container to main layout
        main_layout.addWidget(content_container)
    
    def load_courses(self):
        """Load courses into table"""
        self.course_table.setRowCount(0)
        try:
            courses = get_all_courses()
            self.course_table.setRowCount(len(courses))
            
            for i, course in enumerate(courses):
                self.course_table.setItem(i, 0, QTableWidgetItem(course['course_code']))
                self.course_table.setItem(i, 1, QTableWidgetItem(course['course_name']))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load courses: {str(e)}")
    
    def select_course(self):
        """Handle course selection from table"""
        selected_rows = self.course_table.selectedIndexes()
        if selected_rows:
            row = selected_rows[0].row()
            course_code = self.course_table.item(row, 0).text()
            self.selected_course_code = course_code
            self.delete_btn.setEnabled(True)
            
            # Load course data into form
            name = self.course_table.item(row, 1).text()
            
            self.code_entry.setText(course_code)
            self.name_entry.setText(name)
            
            # Update UI for edit mode
            self.current_mode = "edit"
            self.save_btn.setText("Update Course")
            
            # Disable code field in edit mode
            self.code_entry.setEnabled(False)
        else:
            self.selected_course_code = None
            self.delete_btn.setEnabled(False)
    
    def reset_form(self):
        """Reset the form to add new course mode"""
        self.code_entry.clear()
        self.name_entry.clear()
        
        # Enable code field in add mode
        self.code_entry.setEnabled(True)
        
        self.selected_course_code = None
        self.current_mode = "add"
        self.save_btn.setText("Add Course")
        self.delete_btn.setEnabled(False)
        
        # Deselect any selected row
        self.course_table.clearSelection()
    
    def save_course(self):
        """Save or update course information"""
        # Validate inputs
        code = self.code_entry.text().strip().upper()
        name = self.name_entry.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "Validation Error", "All fields are required")
            return
        
        try:
            if self.current_mode == "add":
                # Add new course
                success, msg = add_course(code, name)
                
                if success:
                    QMessageBox.information(self, "Success", "Course added successfully")
                    self.reset_form()
                else:
                    QMessageBox.warning(self, "Error", msg)
            else:
                # Update existing course
                success, msg = update_course(self.selected_course_code, name)
                
                if success:
                    QMessageBox.information(self, "Success", "Course updated successfully")
                    self.reset_form()
                else:
                    QMessageBox.warning(self, "Error", msg)
            
            # Refresh course list
            self.load_courses()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save course: {str(e)}")
    
    def delete_course(self):
        """Delete the selected course"""
        if not self.selected_course_code:
            return
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this course? " +
                                   "This might affect professor schedules associated with this course.",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                success, msg = delete_course(self.selected_course_code)
                
                if success:
                    QMessageBox.information(self, "Success", "Course deleted successfully")
                    self.reset_form()
                    self.load_courses()
                else:
                    QMessageBox.warning(self, "Error", msg)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete course: {str(e)}")
    
    def on_show(self):
        """Called when frame is shown"""
        self.load_courses() 