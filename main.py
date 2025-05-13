import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget, QSplitter,
                           QScrollArea, QSizePolicy, QSpacerItem, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QEvent, QObject
from PyQt5.QtGui import QFont, QColor, QCursor
import sqlite3
import os
from database import (
    create_database, 
    populate_sample_data, 
    get_all_professors,
    get_professor_by_id,
    get_professor_schedule,
    search_professors,
    filter_professors_by_faculty,
    filter_professors_by_course,
    get_all_faculties,
    get_all_courses,
    ensure_admin_table_exists,
    ensure_photo_url_column
)
from ui.faculty_list import FacultyListFrame
from ui.faculty_detail import FacultyDetailFrame
from ui.schedule_view import ScheduleViewFrame
from ui.admin_frame import AdminFrame
from ui.departments_list import DepartmentsListFrame
from ui.department_detail import DepartmentDetailFrame
from ui.admin_login import AdminLoginFrame
from ui.admin_dashboard import AdminDashboardFrame
from ui.faculty_management import FacultyManagementFrame
from ui.department_management import DepartmentManagementFrame
from ui.course_management import CourseManagementFrame
from ui.schedule_management import ScheduleManagementFrame

class AboutFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create main container with vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header area with yellow background
        header_container = QFrame()
        header_container.setStyleSheet("background-color: #FFDD00;")
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title at the top
        title_label = QLabel("About this app...")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: black;")
        header_layout.addWidget(title_label)
        
        main_layout.addWidget(header_container)
        
        # Content area
        content_area = QFrame()
        content_area.setStyleSheet("""
            background-color: #FCFCFC;
        """)
        content_area.setFrameShape(QFrame.StyledPanel)
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 30)
        
        # App description
        description = """
Faculty Finder is an application designed to help students easily find faculty members at the university.

Features:
• Browse faculty members across departments
• View faculty details including contact information
• Check faculty teaching schedules
• Search for specific faculty members

This application was developed as part of the Database Management Systems course project.
        """
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 12))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #333333;")
        content_layout.addWidget(desc_label)
        
        # Version information
        version_label = QLabel("Version 1.0")
        version_label.setFont(QFont("Arial", 14))
        version_label.setAlignment(Qt.AlignRight)
        version_label.setStyleSheet("color: #333333;")
        content_layout.addWidget(version_label)
        
        main_layout.addWidget(content_area)

class NavButton(QWidget):
    clicked = pyqtSignal()
    
    def __init__(self, text, parent=None):
        super(NavButton, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(text)
        self.label.setFont(QFont("Arial", 20))
        self.label.setStyleSheet("color: white; background-color: #212121; padding: 10px 15px;")
        self.label.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.layout.addWidget(self.label)
        self.setStyleSheet("background-color: #212121;")
        
        # Store original and active colors
        self.default_bg = "#212121"
        self.active_bg = "#FFDD00"  # Changed to yellow
        self.hover_bg = "#2D2D2D"
        self.is_active = False
    
    def enterEvent(self, event):
        if not self.is_active:
            self.label.setStyleSheet(f"color: white; background-color: {self.hover_bg}; padding: 10px 15px;")
    
    def leaveEvent(self, event):
        if not self.is_active:
            self.label.setStyleSheet(f"color: white; background-color: {self.default_bg}; padding: 10px 15px;")
    
    def mousePressEvent(self, event):
        self.clicked.emit()
    
    def setActive(self, active):
        self.is_active = active
        if active:
            self.label.setStyleSheet(f"color: black; background-color: {self.active_bg}; padding: 10px 15px;")
        else:
            self.label.setStyleSheet(f"color: white; background-color: {self.default_bg}; padding: 10px 15px;")

class FacultyManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Faculty Finder!")
        self.resize(1000, 600)
        self.setMinimumSize(800, 500)
        
        # Admin mode tracking
        self.admin_mode = False
        self.admin_info = None
        
        # Initialize database if it doesn't exist
        db_path = "faculty_db.sqlite"
        db_exists = os.path.exists(db_path)
        
        if not db_exists:
            create_database()
            populate_sample_data()
        
        # Always ensure admin table exists and photo_url column exists
        ensure_admin_table_exists()
        ensure_photo_url_column()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main container with horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create navigation frame (black sidebar)
        self.nav_frame = QFrame()
        self.nav_frame.setStyleSheet("background-color: #212121;")
        self.nav_frame.setFixedWidth(220)
        
        nav_layout = QVBoxLayout(self.nav_frame)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        
        # Create logo container in sidebar
        logo_frame = QFrame()
        logo_frame.setStyleSheet("background-color: #212121;")
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(15, 10, 15, 10)
        logo_layout.setSpacing(5)  # Add spacing between Faculty and Finder
        
        # Add Faculty text to black background
        faculty_label = QLabel("Faculty")
        faculty_label.setFont(QFont("Arial", 32, QFont.Bold))  # Reduced from 36 to 32
        faculty_label.setStyleSheet("color: white; background-color: #212121;")
        faculty_label.setAlignment(Qt.AlignLeft)
        logo_layout.addWidget(faculty_label)
        
        # Add Finder in white text (no background box)
        finder_frame = QFrame()
        finder_frame.setFixedWidth(190)  # Set fixed width to prevent cutoff
        finder_layout = QHBoxLayout(finder_frame)  # Change to horizontal layout
        finder_layout.setContentsMargins(10, 5, 10, 5)  # Adjust padding for better fit
        
        finder_label = QLabel("Finder")
        finder_label.setFont(QFont("Arial", 32, QFont.Bold))  # Reduced from 36 to 32
        finder_label.setStyleSheet("color: white;")
        finder_label.setAlignment(Qt.AlignCenter)  # Center align the text
        finder_layout.addWidget(finder_label)
        
        logo_layout.addWidget(finder_frame)
        nav_layout.addWidget(logo_frame)
        
        # Create navigation buttons container
        self.nav_buttons_container = QFrame()
        self.nav_buttons_container.setStyleSheet("background-color: #212121;")
        buttons_layout = QVBoxLayout(self.nav_buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(0)
        
        # Add navigation buttons
        self.faculty_btn = NavButton("Faculty")
        self.faculty_btn.clicked.connect(lambda: self.show_frame("departmentslistframe"))
        buttons_layout.addWidget(self.faculty_btn)
        
        self.about_btn = NavButton("About")
        self.about_btn.clicked.connect(lambda: self.show_frame("aboutframe"))
        buttons_layout.addWidget(self.about_btn)
        
        self.admin_btn = NavButton("Admin")
        self.admin_btn.clicked.connect(self.show_admin_login)
        buttons_layout.addWidget(self.admin_btn)
        
        nav_layout.addWidget(self.nav_buttons_container)
        
        # Add spacer at the bottom to push buttons to top
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        nav_layout.addItem(spacer)
        
        # Content area (default background)
        self.content_widget = QFrame()
        
        # Add navigation frame and content frame to main layout
        main_layout.addWidget(self.nav_frame)
        main_layout.addWidget(self.content_widget, 1)  # content takes remaining space
        
        # Create stacked widget for different frames
        self.stacked_widget = QStackedWidget(self.content_widget)
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.stacked_widget)
        
        # Initialize frames
        self.frames = {}
        
        # About frame
        about_frame = AboutFrame(self.stacked_widget, self)
        self.stacked_widget.addWidget(about_frame)
        self.frames["aboutframe"] = about_frame
        
        # Create other frames
        frames_classes = [
            FacultyListFrame, DepartmentsListFrame, DepartmentDetailFrame, 
            FacultyDetailFrame, ScheduleViewFrame, AdminFrame,
            AdminLoginFrame, AdminDashboardFrame, FacultyManagementFrame,
            DepartmentManagementFrame, CourseManagementFrame, ScheduleManagementFrame
        ]
        
        for FrameClass in frames_classes:
            frame_name = FrameClass.__name__.lower()
            if frame_name != "aboutframe":  # Already created above
                frame = FrameClass(self.stacked_widget, self)
                self.stacked_widget.addWidget(frame)
                self.frames[frame_name] = frame
        
        # Show default frame - Departments list
        self.show_frame("departmentslistframe")
        
        # Track active button
        self.active_button = None
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Propagate resize event to frames that need special handling
        for frame_name, frame in self.frames.items():
            if hasattr(frame, 'on_resize'):
                frame.on_resize(self.width(), self.height())
    
    def deactivate_all_buttons(self):
        """Deactivate all navigation buttons"""
        self.faculty_btn.setActive(False)
        self.about_btn.setActive(False)
        self.admin_btn.setActive(False)
    
    def show_frame(self, frame_name):
        """Show the specified frame"""
        frame_name = frame_name.lower()
        if frame_name in self.frames:
            # Show the requested frame
            self.stacked_widget.setCurrentWidget(self.frames[frame_name])
            
            # Special handling for certain frames
            if hasattr(self.frames[frame_name], 'on_show'):
                self.frames[frame_name].on_show()
            
            # Activate the corresponding button
            self.deactivate_all_buttons()
            
            button_map = {
                "facultylistframe": self.faculty_btn,
                "departmentslistframe": self.faculty_btn,
                "departmentdetailframe": self.faculty_btn,
                "facultydetailframe": self.faculty_btn,
                "scheduleviewframe": self.faculty_btn,
                "aboutframe": self.about_btn,
                "adminloginframe": self.admin_btn,
                "admindashboardframe": self.admin_btn,
                "facultymanagementframe": self.admin_btn,
                "departmentmanagementframe": self.admin_btn,
                "coursemanagementframe": self.admin_btn,
                "schedulemanagementframe": self.admin_btn
            }
            
            if frame_name in button_map:
                button_map[frame_name].setActive(True)
                self.active_button = button_map[frame_name]
            
            # Handle navigation display based on frame type
            is_detail_view = frame_name in ["departmentdetailframe", "facultydetailframe", "scheduleviewframe"]
            is_admin_view = frame_name in ["adminloginframe", "admindashboardframe", "facultymanagementframe",
                                          "departmentmanagementframe", "coursemanagementframe", "schedulemanagementframe"]
            
            # Show/hide navigation buttons based on view type
            if is_detail_view or is_admin_view:
                # Hide navigation buttons when showing detail pages or admin pages
                self.nav_buttons_container.hide()
            else:
                # Show navigation buttons container
                self.nav_buttons_container.show()
            
            # Reload faculty list if returning to it from admin frame after adding a professor
            if frame_name in ["facultylistframe", "departmentslistframe"] and hasattr(self.frames[frame_name], 'load_faculty_list'):
                try:
                    # Refresh the faculty list
                    self.frames[frame_name].load_faculty_list()
                except Exception as e:
                    print(f"Error refreshing faculty list: {e}")  # Log error, don't crash
            
            # Reload faculties in admin frame if needed
            if frame_name == "adminframe" and hasattr(self.frames["adminframe"], 'load_faculties'):
                try:
                    self.frames["adminframe"].load_faculties()
                except Exception as e:
                    print(f"Error reloading faculties in admin frame: {e}")
    
    def show_faculty_detail(self, faculty_id):
        """Show faculty detail for the specified faculty ID"""
        try:
            self.frames["facultydetailframe"].load_faculty(faculty_id)
            self.show_frame("facultydetailframe")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load faculty details: {str(e)}")
    
    def show_schedule(self, faculty_id):
        """Show schedule for the specified faculty ID"""
        try:
            self.frames["scheduleviewframe"].load_schedule(faculty_id)
            self.show_frame("scheduleviewframe")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load schedule: {str(e)}")
    
    def show_department_detail(self, department_name):
        """Show department detail for the specified department"""
        try:
            self.frames["departmentdetailframe"].set_department(department_name)
            self.show_frame("departmentdetailframe")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load department details: {str(e)}")
    
    def show_admin_login(self):
        """Show the admin login screen"""
        self.show_frame("adminloginframe")
    
    def admin_logged_in(self, admin_info):
        """Called when admin successfully logs in"""
        self.admin_mode = True
        self.admin_info = admin_info
        
        # Update admin dashboard with user info
        self.frames["admindashboardframe"].set_admin_info(admin_info)
        
        # Show admin dashboard
        self.show_frame("admindashboardframe")
    
    def admin_logged_out(self):
        """Called when admin logs out"""
        self.admin_mode = False
        self.admin_info = None
        
        # Return to main view
        self.show_frame("departmentslistframe")
    
    def show_faculty_management(self):
        """Show faculty management screen"""
        self.show_frame("facultymanagementframe")

    def on_resize(self, window_width, window_height):
        # Calculate available width (adjust for 220px sidebar instead of 200px)
        available_width = window_width - 260  # 220px sidebar + 40px padding
        self.adjust_grid_layout(available_width)

if __name__ == "__main__":
    # Add basic error handling for application startup
    try:
        app = QApplication(sys.argv)
        window = FacultyManagementSystem()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        # Fallback error display if QApplication fails early
        print(f"Fatal error starting application: {str(e)}")
        try:
            # Attempt to show an error message if possible
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "Application Error", 
                               f"A fatal error occurred: {str(e)}\n\nThe application will now close.")
        except:
            pass  # If Qt itself is broken, just print error

