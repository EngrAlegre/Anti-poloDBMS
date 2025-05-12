from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QScrollArea, QGridLayout, QPushButton, QSizePolicy, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QCursor
from database import get_all_professors, get_all_departments, get_all_faculties, get_all_courses

class StatCard(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white; border-radius: 5px;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Card title
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.title_label)
        
        # Card count
        self.count_label = QLabel("0")
        self.count_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.count_label)
    
    def update_count(self, value):
        """Update the count displayed on the card"""
        self.count_label.setText(str(value))

class AdminDashboardFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.admin_info = None
        
        # Set background color
        self.setStyleSheet("background-color: #FFDD00;")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar with title and logout button
        top_bar = QFrame()
        top_bar.setStyleSheet("background-color: #FFDD00;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 20, 20, 20)
        
        # Dashboard title
        title_label = QLabel("Admin Dashboard")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: black;")
        top_layout.addWidget(title_label)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        top_layout.addWidget(logout_btn, 0, Qt.AlignRight)
        
        main_layout.addWidget(top_bar)
        
        # Welcome message
        self.welcome_label = QLabel("Welcome, Administrator")
        self.welcome_label.setFont(QFont("Arial", 16))
        self.welcome_label.setStyleSheet("color: black; background-color: #FFDD00;")
        self.welcome_label.setContentsMargins(20, 0, 20, 20)
        main_layout.addWidget(self.welcome_label)
        
        # Statistics cards container
        stats_container = QFrame()
        stats_container.setStyleSheet("background-color: #FFDD00;")
        stats_layout = QGridLayout(stats_container)
        stats_layout.setContentsMargins(20, 0, 20, 20)
        stats_layout.setSpacing(20)
        
        # Create statistic cards
        self.faculty_card = StatCard("Faculty Members")
        stats_layout.addWidget(self.faculty_card, 0, 0)
        
        self.dept_card = StatCard("Departments")
        stats_layout.addWidget(self.dept_card, 0, 1)
        
        self.course_card = StatCard("Courses")
        stats_layout.addWidget(self.course_card, 0, 2)
        
        self.schedule_card = StatCard("Schedules")
        stats_layout.addWidget(self.schedule_card, 0, 3)
        
        # Add stats container to main layout
        main_layout.addWidget(stats_container)
        
        # Management sections container
        sections_container = QFrame()
        sections_container.setStyleSheet("background-color: white;")
        sections_layout = QVBoxLayout(sections_container)
        sections_layout.setContentsMargins(20, 20, 20, 20)
        
        # Management sections title
        sections_title = QLabel("Management Sections")
        sections_title.setFont(QFont("Arial", 16, QFont.Bold))
        sections_layout.addWidget(sections_title)
        
        # Management buttons container
        buttons_container = QFrame()
        buttons_container.setStyleSheet("background-color: white;")
        buttons_layout = QGridLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 20, 0, 0)
        buttons_layout.setSpacing(20)
        
        # Management buttons
        faculty_btn = QPushButton("Manage Faculty")
        faculty_btn.setFont(QFont("Arial", 12))
        faculty_btn.setMinimumHeight(60)
        faculty_btn.clicked.connect(self.show_faculty_management)
        buttons_layout.addWidget(faculty_btn, 0, 0)
        
        department_btn = QPushButton("Manage Departments")
        department_btn.setFont(QFont("Arial", 12))
        department_btn.setMinimumHeight(60)
        department_btn.clicked.connect(self.show_department_management)
        buttons_layout.addWidget(department_btn, 0, 1)
        
        course_btn = QPushButton("Manage Courses")
        course_btn.setFont(QFont("Arial", 12))
        course_btn.setMinimumHeight(60)
        course_btn.clicked.connect(self.show_course_management)
        buttons_layout.addWidget(course_btn, 1, 0)
        
        schedule_btn = QPushButton("Manage Schedules")
        schedule_btn.setFont(QFont("Arial", 12))
        schedule_btn.setMinimumHeight(60)
        schedule_btn.clicked.connect(self.show_schedule_management)
        buttons_layout.addWidget(schedule_btn, 1, 1)
        
        # Add buttons container to sections layout
        sections_layout.addWidget(buttons_container)
        
        # Add sections container to main layout
        main_layout.addWidget(sections_container)
    
    def set_admin_info(self, admin_info):
        """Set admin information and update the welcome message"""
        self.admin_info = admin_info
        self.welcome_label.setText(f"Welcome, {admin_info[2]}")
        
        # Refresh dashboard data
        self.refresh_dashboard()
    
    def refresh_dashboard(self):
        """Refresh dashboard statistics"""
        # Get counts from database
        professors = get_all_professors()
        departments = get_all_departments()
        courses = get_all_courses()
        
        # Update statistics
        self.faculty_card.update_count(len(professors))
        self.dept_card.update_count(len(departments))
        self.course_card.update_count(len(courses))
        
        # For schedules, we'd need a separate function, but for now let's use a placeholder
        self.schedule_card.update_count(25)  # Placeholder
    
    def show_faculty_management(self):
        """Show faculty management screen"""
        self.controller.show_faculty_management()
    
    def show_department_management(self):
        """Show department management screen"""
        self.controller.show_frame("departmentmanagementframe")
    
    def show_course_management(self):
        """Show course management screen"""
        self.controller.show_frame("coursemanagementframe")
    
    def show_schedule_management(self):
        """Show schedule management screen"""
        self.controller.show_frame("schedulemanagementframe")
    
    def logout(self):
        """Log out and return to the main application"""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to log out?", 
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.admin_info = None
            self.controller.admin_logged_out() 