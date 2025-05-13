from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QScrollArea, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QCursor
import sqlite3
from database import get_professor_by_id, get_professor_schedule

class ScheduleViewFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_faculty_id = None
        
        # Set background color
        self.setStyleSheet("background-color: #FFDD00;")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Name label at the top
        self.name_label = QLabel("")
        self.name_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.name_label.setStyleSheet("color: black; background-color: #FFDD00;")
        self.name_label.setWordWrap(True)
        self.name_label.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(self.name_label)
        
        # White content area
        content_area = QFrame()
        content_area.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Schedule frame
        schedule_frame = QFrame()
        schedule_frame.setStyleSheet("background-color: white;")
        schedule_layout = QVBoxLayout(schedule_frame)
        
        # Create table for schedule items
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(4)
        self.schedule_table.setHorizontalHeaderLabels(["Day", "Time", "Course", "Location"])
        self.schedule_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.schedule_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.schedule_table.horizontalHeader().setStretchLastSection(True)
        self.schedule_table.horizontalHeader().setFont(QFont("Arial", 12, QFont.Bold))
        self.schedule_table.verticalHeader().setVisible(False)
        
        # Set column widths
        self.schedule_table.setColumnWidth(0, 100) # Day
        self.schedule_table.setColumnWidth(1, 150) # Time
        self.schedule_table.setColumnWidth(2, 300) # Course
        
        # Add table to schedule layout
        schedule_layout.addWidget(self.schedule_table)
        
        # Button area
        button_frame = QFrame()
        button_frame.setStyleSheet("background-color: white;")
        button_layout = QHBoxLayout(button_frame)
        
        # Back button
        self.back_btn = QPushButton("Back to Faculty Details")
        self.back_btn.clicked.connect(self.back_to_details)
        button_layout.addWidget(self.back_btn)
        button_layout.addStretch(1)  # Push button to the left
        
        # Add schedule frame and button frame to content layout
        content_layout.addWidget(schedule_frame)
        content_layout.addWidget(button_frame)
        
        # Add content area to main layout
        main_layout.addWidget(content_area)
    
    def on_resize(self, window_width, window_height):
        # Calculate available width
        available_width = window_width - 260  # 220px sidebar + 40px padding
        
        # Update column sizes based on available width
        if self.schedule_table.isVisible():
            header_width = available_width - 80  # account for padding and scrollbar
            
            # Distribution: Day (15%), Time (25%), Course (40%), Location (20%)
            self.schedule_table.setColumnWidth(0, int(header_width * 0.15))
            self.schedule_table.setColumnWidth(1, int(header_width * 0.25))
            self.schedule_table.setColumnWidth(2, int(header_width * 0.40))
    
    def load_schedule(self, faculty_id):
        """Load schedule for a faculty member"""
        self.current_faculty_id = faculty_id
        
        try:
            # Get professor details
            professor = get_professor_by_id(faculty_id)
            if not professor:
                raise Exception("Professor not found!")
            
            # Update name label
            full_name = f"{professor['first_name']} {professor['last_name']} - Schedule"
            self.name_label.setText(full_name)
            
            # Clear existing schedule items
            self.schedule_table.setRowCount(0)
            
            # Get schedule items
            schedule_items = get_professor_schedule(faculty_id)
            
            # Create schedule items display
            for i, item in enumerate(schedule_items):
                self.schedule_table.insertRow(i)
                
                # Day
                day_item = QTableWidgetItem(item["day_of_week"])
                day_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.schedule_table.setItem(i, 0, day_item)
                
                # Time
                time_text = f"{item['start_time']} - {item['end_time']}"
                time_item = QTableWidgetItem(time_text)
                time_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.schedule_table.setItem(i, 1, time_item)
                
                # Course
                course_text = f"{item['course_code']} - {item['course_name']}"
                course_item = QTableWidgetItem(course_text)
                course_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.schedule_table.setItem(i, 2, course_item)
                
                # Location
                location_item = QTableWidgetItem(item["room_location"])
                location_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.schedule_table.setItem(i, 3, location_item)
                
                # Set row height
                self.schedule_table.setRowHeight(i, 40)
            
            # Show message if no schedule items
            if not schedule_items:
                self.schedule_table.insertRow(0)
                no_schedule = QTableWidgetItem("No schedule items found for this faculty member.")
                no_schedule.setTextAlignment(Qt.AlignCenter)
                self.schedule_table.setSpan(0, 0, 1, 4)
                self.schedule_table.setItem(0, 0, no_schedule)
            
        except Exception as e:
            self.schedule_table.setRowCount(0)
            self.schedule_table.insertRow(0)
            error_item = QTableWidgetItem(f"Error: {str(e)}")
            error_item.setTextAlignment(Qt.AlignCenter)
            error_item.setForeground(Qt.red)
            self.schedule_table.setSpan(0, 0, 1, 4)
            self.schedule_table.setItem(0, 0, error_item)
    
    def back_to_details(self):
        """Go back to faculty details"""
        if self.current_faculty_id:
            self.controller.show_faculty_detail(self.current_faculty_id)
        else:
            self.controller.show_frame("facultylistframe")