from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QComboBox, QTimeEdit,
                            QPushButton, QGridLayout, QMessageBox, QVBoxLayout,
                            QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont
import sqlite3
from database import (add_schedule, get_all_professors, get_all_courses)

class AddScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Schedule")
        self.setFixedWidth(500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Add New Schedule")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Content frame
        content_frame = QFrame()
        content_frame.setStyleSheet("QFrame { background-color: white; border-radius: 5px; }")
        content_layout = QGridLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)
        
        # Form fields
        row = 0
        
        # Professor selection
        content_layout.addWidget(QLabel("Professor:"), row, 0)
        self.professor_combo = QComboBox()
        content_layout.addWidget(self.professor_combo, row, 1)
        row += 1
        
        # Course selection
        content_layout.addWidget(QLabel("Course:"), row, 0)
        self.course_combo = QComboBox()
        content_layout.addWidget(self.course_combo, row, 1)
        row += 1
        
        # Day of week
        content_layout.addWidget(QLabel("Day:"), row, 0)
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
        content_layout.addWidget(self.day_combo, row, 1)
        row += 1
        
        # Start time
        content_layout.addWidget(QLabel("Start Time:"), row, 0)
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("hh:mm")
        self.start_time.setTime(QTime(8, 0))
        content_layout.addWidget(self.start_time, row, 1)
        row += 1
        
        # End time
        content_layout.addWidget(QLabel("End Time:"), row, 0)
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("hh:mm")
        self.end_time.setTime(QTime(10, 0))
        content_layout.addWidget(self.end_time, row, 1)
        row += 1
        
        # Room location
        content_layout.addWidget(QLabel("Room:"), row, 0)
        self.room_edit = QLineEdit()
        self.room_edit.setPlaceholderText("e.g. Room 101")
        content_layout.addWidget(self.room_edit, row, 1)
        row += 1
        
        # Academic year
        content_layout.addWidget(QLabel("Academic Year:"), row, 0)
        self.year_edit = QLineEdit()
        self.year_edit.setPlaceholderText("e.g. 2023-2024")
        self.year_edit.setText("2023-2024")
        content_layout.addWidget(self.year_edit, row, 1)
        row += 1
        
        # Semester
        content_layout.addWidget(QLabel("Semester:"), row, 0)
        self.semester_combo = QComboBox()
        self.semester_combo.addItems(["1st", "2nd", "Summer"])
        content_layout.addWidget(self.semester_combo, row, 1)
        row += 1
        
        main_layout.addWidget(content_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #DDDDDD;
                color: #333333;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #CCCCCC;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("Save Schedule")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00;
                color: black;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 100px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFE840;
            }
        """)
        self.save_btn.clicked.connect(self.save_schedule)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
        
        # Load professors and courses
        self.load_data()
    
    def load_data(self):
        """Load professors and courses into combo boxes"""
        try:
            # Load professors
            professors = get_all_professors()
            for prof in professors:
                display_text = f"{prof['first_name']} {prof['last_name']}"
                self.professor_combo.addItem(display_text, prof['faculty_id'])
            
            # Load courses
            courses = get_all_courses()
            for course in courses:
                display_text = f"{course['course_code']} - {course['course_name']}"
                self.course_combo.addItem(display_text, course['course_code'])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
    
    def save_schedule(self):
        """Save the schedule to the database"""
        try:
            # Get values from form
            faculty_id = self.professor_combo.currentData()
            if faculty_id is None:
                QMessageBox.warning(self, "Error", "Please select a professor")
                return
            
            course_code = self.course_combo.currentData()
            if course_code is None:
                QMessageBox.warning(self, "Error", "Please select a course")
                return
            
            day_of_week = self.day_combo.currentText()
            start_time = self.start_time.time().toString("hh:mm")
            end_time = self.end_time.time().toString("hh:mm")
            
            room_location = self.room_edit.text().strip()
            if not room_location:
                QMessageBox.warning(self, "Error", "Please enter a room location")
                return
            
            academic_year = self.year_edit.text().strip()
            if not academic_year:
                QMessageBox.warning(self, "Error", "Please enter an academic year")
                return
            
            semester_num = self.semester_combo.currentText()
            
            # Validate time range
            if self.start_time.time() >= self.end_time.time():
                QMessageBox.warning(self, "Error", "End time must be after start time")
                return
            
            # Add schedule to database
            success, message = add_schedule(
                faculty_id, day_of_week, start_time, end_time,
                room_location, academic_year, semester_num, course_code
            )
            
            if success:
                self.accept()  # Close dialog with success
            else:
                QMessageBox.warning(self, "Error", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save schedule: {str(e)}") 