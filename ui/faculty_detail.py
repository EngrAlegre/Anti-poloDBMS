from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QScrollArea, QGridLayout, QPushButton, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QCursor, QPixmap, QColor
import sqlite3
from database import get_professor_by_id

class InfoCard(QFrame):
    """A styled card widget for displaying information sections"""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 0px;
                border: 1px solid #DDDDDD;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 10, 15, 15)
        self.layout.setSpacing(10)
        
        # Title
        if title:
            title_label = QLabel(title)
            title_label.setFont(QFont("Arial", 16, QFont.Bold))
            title_label.setStyleSheet("color: #333333;")
            self.layout.addWidget(title_label)
            
            # Add divider under title
            divider = QFrame()
            divider.setFrameShape(QFrame.HLine)
            divider.setFrameShadow(QFrame.Sunken)
            divider.setStyleSheet("background-color: #DDDDDD;")
            self.layout.addWidget(divider)

class FacultyDetailFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_faculty_id = None
        
        # Set background color
        self.setStyleSheet("background-color: #FFDD00;")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header container
        header_container = QWidget()
        header_container.setStyleSheet("background-color: #FFDD00;")
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(20, 10, 20, 20)
        
        # Back button
        back_button = QPushButton("← Back to Department")
        back_button.clicked.connect(self.go_back_to_department)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00;
                border: none;
                text-align: left;
                padding: 5px;
                font-size: 12px;
                color: #333333;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        header_layout.addWidget(back_button)
        
        # Name label at the top
        self.name_label = QLabel("")
        self.name_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.name_label.setStyleSheet("color: black;")
        self.name_label.setWordWrap(True)
        header_layout.addWidget(self.name_label)
        
        # Add header to main layout
        main_layout.addWidget(header_container)
        
        # Content area with white background
        content_background = QFrame()
        content_background.setStyleSheet("""
            background-color: #FCFCFC;
        """)
        content_layout = QVBoxLayout(content_background)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("background-color: white;")
        
        # Create content widget
        scroll_content = QWidget()
        scroll_content.setStyleSheet("""
            background-color: #FCFCFC;
        """)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        scroll_layout.setSpacing(25)
        
        # Create cards for each information section
        self.faculty_card = InfoCard("Faculty Information")
        
        # Create a separate layout for each row with label and value side by side
        info_layout = QVBoxLayout()
        info_layout.setSpacing(12)
        
        # Department row
        dept_row = QHBoxLayout()
        
        dept_label = QLabel("Department:")
        dept_label.setFont(QFont("Arial", 14))
        dept_label.setStyleSheet("font-weight: bold; color: #333333;")
        dept_label.setFixedWidth(120)
        
        self.faculty_value = QLabel("")
        self.faculty_value.setFont(QFont("Arial", 14))
        self.faculty_value.setStyleSheet("color: #333333;")
        
        dept_row.addWidget(dept_label)
        dept_row.addWidget(self.faculty_value)
        dept_row.addStretch(1)
        info_layout.addLayout(dept_row)
        
        # Location row
        location_row = QHBoxLayout()
        
        location_label = QLabel("Location:")
        location_label.setFont(QFont("Arial", 14))
        location_label.setStyleSheet("font-weight: bold; color: #333333;")
        location_label.setFixedWidth(120)
        
        self.location_value = QLabel("")
        self.location_value.setFont(QFont("Arial", 14))
        self.location_value.setStyleSheet("color: #333333;")
        
        location_row.addWidget(location_label)
        location_row.addWidget(self.location_value)
        location_row.addStretch(1)
        info_layout.addLayout(location_row)
        
        # Email row
        email_row = QHBoxLayout()
        
        email_label = QLabel("Email:")
        email_label.setFont(QFont("Arial", 14))
        email_label.setStyleSheet("font-weight: bold; color: #333333;")
        email_label.setFixedWidth(120)
        
        self.email_value = QLabel("")
        self.email_value.setFont(QFont("Arial", 14))
        self.email_value.setStyleSheet("color: #333333;")
        
        email_row.addWidget(email_label)
        email_row.addWidget(self.email_value)
        email_row.addStretch(1)
        info_layout.addLayout(email_row)
        
        # Specialty row
        specialty_row = QHBoxLayout()
        
        specialty_label = QLabel("Specialty:")
        specialty_label.setFont(QFont("Arial", 14))
        specialty_label.setStyleSheet("font-weight: bold; color: #333333;")
        specialty_label.setFixedWidth(120)
        
        self.subject_value = QLabel("")
        self.subject_value.setFont(QFont("Arial", 14))
        self.subject_value.setStyleSheet("color: #333333;")
        
        specialty_row.addWidget(specialty_label)
        specialty_row.addWidget(self.subject_value)
        specialty_row.addStretch(1)
        info_layout.addLayout(specialty_row)
        
        # Add the rows to the faculty card
        self.faculty_card.layout.addLayout(info_layout)
        
        # Add faculty card to scroll layout
        scroll_layout.addWidget(self.faculty_card)
        
        # Schedule card 
        schedule_card = InfoCard("Schedule")
        schedule_layout = QVBoxLayout()
        
        schedule_info = QLabel("View the professor's teaching schedule and office hours.")
        schedule_info.setFont(QFont("Arial", 12))
        schedule_info.setStyleSheet("color: #333333;")
        schedule_layout.addWidget(schedule_info)
        
        # Add spacer before button
        schedule_layout.addSpacing(5)
        
        self.schedule_btn = QPushButton("View Schedule")
        self.schedule_btn.clicked.connect(self.view_schedule)
        self.schedule_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        self.schedule_btn.setMaximumWidth(120)
        schedule_layout.addWidget(self.schedule_btn)
        
        schedule_card.layout.addLayout(schedule_layout)
        scroll_layout.addWidget(schedule_card)
        
        # Add spacer at the bottom
        scroll_layout.addStretch(1)
        
        # Set content widget to scroll area
        scroll_area.setWidget(scroll_content)
        content_layout.addWidget(scroll_area)
        
        # Add content area to main layout
        main_layout.addWidget(content_background)
    
    def on_resize(self, window_width, window_height):
        # Calculate available width
        available_width = window_width - 260  # 220px sidebar + 40px padding
        
        # Update wraplength properties
        self.name_label.setMaximumWidth(min(600, available_width - 40))
    
    def load_faculty(self, faculty_id):
        """Load faculty details"""
        self.current_faculty_id = faculty_id
        
        try:
            # Get professor details from database
            professor = get_professor_by_id(faculty_id)
            
            if not professor:
                raise Exception("Professor not found!")
            
            # Update header with professor name
            full_name = f"{professor['f_name']} {professor['l_name']}"
            self.name_label.setText(full_name)
            
            # Update faculty information
            self.faculty_value.setText(professor["office_name"])
            
            # Update location
            location = f"Building {professor['building_num']}, Room {professor['room_num']}"
            self.location_value.setText(location)
            
            # Update email
            self.email_value.setText(professor["email"])
            
            # Update subject
            self.subject_value.setText(professor["subject_id"])
            
        except Exception as e:
            self.name_label.setText(f"Error: {str(e)}")
    
    def view_schedule(self):
        """View faculty schedule"""
        if self.current_faculty_id:
            self.controller.show_schedule(self.current_faculty_id)
            
    def go_back_to_department(self):
        """Go back to the department that this faculty belongs to"""
        if self.current_faculty_id:
            # Get professor details to find their department
            professor = get_professor_by_id(self.current_faculty_id)
            if professor and professor["office_name"]:
                # Show the department details for this professor's department
                self.controller.show_department_detail(professor["office_name"])
            else:
                # Fallback to departments list if no department found
                self.controller.show_frame("departmentslistframe")
        else:
            # Fallback to departments list if no faculty ID
            self.controller.show_frame("departmentslistframe")