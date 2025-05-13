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
        header_layout = QHBoxLayout(header_container)  # Changed to horizontal layout
        header_layout.setContentsMargins(20, 10, 20, 20)
        
        # Left side container for back button and name
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Back button
        back_button = QPushButton("← Back to Department")
        back_button.clicked.connect(self.go_back_to_department)
        back_button.setStyleSheet("""
            QPushButton {
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
        left_layout.addWidget(back_button)
        
        # Name label at the top
        self.name_label = QLabel("")
        self.name_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.name_label.setStyleSheet("color: black;")
        self.name_label.setWordWrap(True)
        left_layout.addWidget(self.name_label)
        
        # Add left container to header layout
        header_layout.addWidget(left_container, 4)  # Give more space to left container
        
        # Right side for profile photo
        self.photo_container = QWidget()
        self.photo_container.setFixedSize(100, 100)
        photo_layout = QVBoxLayout(self.photo_container)
        photo_layout.setContentsMargins(0, 0, 0, 0)
        
        # Profile photo label
        self.profile_photo = QLabel()
        self.profile_photo.setFixedSize(80, 80)
        self.profile_photo.setStyleSheet("""
            background-color: #555555;
            border-radius: 40px;
            border: 2px solid #FFFFFF;
        """)
        self.profile_photo.setAlignment(Qt.AlignCenter)
        self.profile_photo.setText("👤")
        self.profile_photo.setFont(QFont("Arial", 40))
        photo_layout.addWidget(self.profile_photo, 0, Qt.AlignCenter)
        
        # Add photo container to header layout
        header_layout.addWidget(self.photo_container, 1)
        
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
        
            if professor:
                # Set professor name
                name = f"{professor['first_name']} {professor['last_name']}"
                self.name_label.setText(name)
                
                # Set department
                self.faculty_value.setText(professor['department_name'] if professor['department_name'] else "N/A")
                
                # Set location
                building = professor['building_num'] if professor['building_num'] else "N/A"
                room = professor['room_num'] if professor['room_num'] else "N/A"
                location = f"Building {building}, Room {room}" if building != "N/A" else "N/A"
                self.location_value.setText(location)
                
                # Set email
                self.email_value.setText(professor['email'] if professor['email'] else "N/A")
                
                # Set specialty (subject_id)
                self.subject_value.setText(professor['subject_id'] if professor['subject_id'] else "N/A")
                
                # Handle profile photo if available
                if 'photo_url' in professor and professor['photo_url']:
                    try:
                        pixmap = QPixmap(professor['photo_url'])
                        if not pixmap.isNull():
                            # Scale the pixmap to fit the label while maintaining aspect ratio
                            pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            # Set the pixmap on the label
                            self.profile_photo.setText("")
                            self.profile_photo.setPixmap(pixmap)
                            # Make the label circular by setting a stylesheet with border-radius
                            self.profile_photo.setStyleSheet("""
                                background-color: #555555;
                                border-radius: 40px;
                                border: 2px solid #FFFFFF;
                            """)
                        else:
                            # Fallback to default icon if pixmap is null
                            self.profile_photo.setText("👤")
                            self.profile_photo.setFont(QFont("Arial", 40))
                    except Exception as e:
                        print(f"Error loading profile image: {str(e)}")
                        self.profile_photo.setText("👤")
                        self.profile_photo.setFont(QFont("Arial", 40))
                else:
                    # Default icon if no photo_url
                    self.profile_photo.setText("👤")
                    self.profile_photo.setFont(QFont("Arial", 40))
            else:
                # Handle case where professor is not found
                self.name_label.setText("Faculty not found")
                self.faculty_value.setText("N/A")
                self.location_value.setText("N/A")
                self.email_value.setText("N/A")
                self.subject_value.setText("N/A")
                self.schedule_btn.setEnabled(False)
                
                # Reset profile photo
                self.profile_photo.setText("👤")
                self.profile_photo.setFont(QFont("Arial", 40))
        
        except Exception as e:
            print(f"Error loading faculty: {str(e)}")
            self.name_label.setText("Error loading faculty")
            self.faculty_value.setText("N/A")
            self.location_value.setText("N/A")
            self.email_value.setText("N/A")
            self.subject_value.setText("N/A")
            self.schedule_btn.setEnabled(False)
            
            # Reset profile photo
            self.profile_photo.setText("👤")
            self.profile_photo.setFont(QFont("Arial", 40))
    
    def view_schedule(self):
        """View faculty schedule"""
        if self.current_faculty_id:
            self.controller.show_schedule(self.current_faculty_id)
    
    def go_back_to_department(self):
        """Go back to department view"""
        if self.current_faculty_id:
            # Get the department for this faculty
            professor = get_professor_by_id(self.current_faculty_id)
            if professor and professor["department_name"]:
                self.controller.show_department_detail(professor["department_name"])
            else:
                # If no department, go back to departments list
                self.controller.show_frame("departmentslistframe")
        else:
            # If no faculty selected, go back to departments list
            self.controller.show_frame("departmentslistframe")