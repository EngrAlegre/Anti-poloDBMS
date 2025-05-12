from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QScrollArea, QGridLayout, QPushButton, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QCursor, QPixmap
from database import get_professors_by_department

class FacultyCard(QFrame):
    def __init__(self, faculty_data, controller, parent=None):
        super().__init__(parent)
        self.faculty_id = faculty_data[0]
        self.controller = controller
        
        # Configure appearance
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
            QFrame:hover {
                border: 1px solid #999999;
                background-color: #F9F9F9;
            }
        """)
        
        # Set fixed size for card
        self.setFixedSize(400, 150)
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(8)
        
        # Create profile picture container
        profile_pic = QLabel()
        profile_pic.setFixedSize(60, 60)
        profile_pic.setStyleSheet("""
            background-color: #DDDDDD;
            border-radius: 30px;
            border: 1px solid #CCCCCC;
        """)
        profile_pic.setText("👤")
        profile_pic.setFont(QFont("Arial", 30))
        profile_pic.setAlignment(Qt.AlignCenter)
        
        # Faculty name (larger and more prominent)
        name = f"{faculty_data[2]} {faculty_data[1]}"  # first_name last_name
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 16, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        
        # Add profile picture and name to layout
        main_layout.addWidget(profile_pic, 0, Qt.AlignCenter)
        main_layout.addWidget(name_label, 0, Qt.AlignCenter)
        
        # Subject (smaller, below name)
        if faculty_data[4]:  # subject_id
            subject_label = QLabel(faculty_data[4])
            subject_label.setStyleSheet("color: #555555;")
            subject_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(subject_label, 0, Qt.AlignCenter)
        
        # Make entire card clickable
        self.setCursor(QCursor(Qt.PointingHandCursor))
    
    def show_faculty_detail(self, event=None):
        self.controller.show_faculty_detail(self.faculty_id)
    
    def mousePressEvent(self, event):
        self.show_faculty_detail()

class DepartmentDetailFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_department = None
        self.current_columns = 2  # Default column count
        
        # Set background color
        self.setStyleSheet("background-color: #FFDD00;")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title and back button area
        title_area = QWidget()
        title_area.setStyleSheet("background-color: #FFDD00;")
        title_layout = QVBoxLayout(title_area)
        title_layout.setContentsMargins(20, 20, 20, 0)
        
        # Back button
        back_button = QPushButton("← Back to Departments")
        back_button.clicked.connect(lambda: controller.show_frame("departmentslistframe"))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00;
                border: none;
                text-align: left;
                padding: 5px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        title_layout.addWidget(back_button)
        
        # Department title
        self.title_label = QLabel("Department Name")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setStyleSheet("background-color: #FFDD00;")
        self.title_label.setWordWrap(True)
        title_layout.addWidget(self.title_label)
        
        # Faculty count subtitle
        self.subtitle_label = QLabel("0 Faculty Members")
        self.subtitle_label.setFont(QFont("Arial", 18))
        self.subtitle_label.setStyleSheet("background-color: #FFDD00;")
        title_layout.addWidget(self.subtitle_label)
        
        main_layout.addWidget(title_area)
        
        # White content area with subtle background
        content_area = QFrame()
        content_area.setStyleSheet("""
            background-color: #FCFCFC;
        """)
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create scrollable area for faculty list
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Create widget to hold grid
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("""
            background-color: #FCFCFC;
        """)
        
        # Grid layout for faculty cards
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(20)
        
        self.scroll_area.setWidget(self.scroll_content)
        content_layout.addWidget(self.scroll_area)
        
        main_layout.addWidget(content_area)
    
    def on_resize(self, window_width, window_height):
        # Calculate the available width (window width minus sidebar and padding)
        available_width = window_width - 260  # 220px sidebar + 40px padding
        self.adjust_grid_layout(available_width)
    
    def adjust_grid_layout(self, available_width):
        # Determine number of columns based on available width
        faculty_card_width = 400  # fixed width of each faculty card
        card_spacing = 20
        new_columns = max(1, int(available_width / (faculty_card_width + card_spacing)))
        
        # Only redraw if column count has changed
        if new_columns != self.current_columns and self.current_department:
            self.current_columns = new_columns
            self.load_faculty()
    
    def set_department(self, department_name):
        self.current_department = department_name
        self.title_label.setText(department_name)
        self.load_faculty()
    
    def load_faculty(self):
        # Clear existing faculty
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        # Get faculty for this department
        faculty_list = get_professors_by_department(self.current_department)
        
        # Update subtitle with count
        faculty_count = len(faculty_list)
        faculty_label = "Faculty Member" if faculty_count == 1 else "Faculty Members"
        self.subtitle_label.setText(f"{faculty_count} {faculty_label}")
        
        # Configure grid layout spacing
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setAlignment(Qt.AlignCenter)  # Center the grid in the available space
        
        # Create grid layout
        row, col = 0, 0
        max_cols = self.current_columns  # Use calculated column count
        
        for faculty in faculty_list:
            # Create faculty card
            card = FacultyCard(faculty, self.controller)
            self.grid_layout.addWidget(card, row, col)
            
            # Move to next grid position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # If no faculty, show message
        if not faculty_list:
            no_faculty_label = QLabel("No faculty members found in this department.")
            no_faculty_label.setAlignment(Qt.AlignCenter)
            no_faculty_label.setStyleSheet("color: #666666; font-size: 14px;")
            self.grid_layout.addWidget(no_faculty_label, 0, 0, 1, max_cols)
            
    def on_show(self):
        # Refresh content if needed
        if self.current_department:
            self.load_faculty() 