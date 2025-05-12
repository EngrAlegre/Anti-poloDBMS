from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QScrollArea, QGridLayout, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QCursor
import sqlite3
from database import get_all_professors, search_professors, filter_professors_by_faculty, get_all_faculties, get_all_courses, filter_professors_by_course

class FacultyCard(QFrame):
    def __init__(self, professor, controller, parent=None):
        super().__init__(parent)
        self.professor = professor
        self.controller = controller
        self.faculty_id = professor["faculty_id"]
        
        # Configure card style
        self.setStyleSheet("""
            QFrame {
                background-color: #3D3D3D;
                border-radius: 8px;
                color: white;
            }
            QFrame:hover {
                background-color: #4D4D4D;
            }
        """)
        
        # Set fixed size for card
        self.setFixedSize(220, 140)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Faculty name
        name_label = QLabel(f"{professor['f_name']} {professor['l_name']}")
        name_label.setFont(QFont("Arial", 14, QFont.Bold))
        name_label.setStyleSheet("color: white;")
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Department
        if professor['office_name']:
            dept_label = QLabel(professor['office_name'])
            dept_label.setStyleSheet("color: #CCCCCC;")
            layout.addWidget(dept_label)
        
        # Email
        email_label = QLabel(professor['email'])
        email_label.setStyleSheet("color: #CCCCCC;")
        email_label.setWordWrap(True)
        layout.addWidget(email_label)
        
        # Make card clickable
        self.setCursor(Qt.PointingHandCursor)
    
    def mousePressEvent(self, event):
        self.controller.show_faculty_detail(self.faculty_id)

class FacultyListFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Set background color
        self.setStyleSheet("background-color: #FFDD00;")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title at the top
        title_label = QLabel("Faculty Members")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: black; background-color: #FFDD00;")
        title_label.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(title_label)
        
        # White content area
        content_area = QFrame()
        content_area.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create scrollable area for faculty members
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Create widget to hold grid
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: white;")
        
        # Grid layout for faculty cards
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(20)
        
        scroll_area.setWidget(self.scroll_content)
        content_layout.addWidget(scroll_area)
        
        main_layout.addWidget(content_area)
        
        # Number of columns in grid
        self.columns = 4
        
        # Load faculty data
        self.load_faculty_list()
    
    def on_resize(self, window_width, window_height):
        # Calculate the available width (window width minus sidebar and padding)
        available_width = window_width - 260  # 220px sidebar + 40px padding
        self.adjust_grid_layout(available_width)
    
    def adjust_grid_layout(self, available_width):
        # Determine how many columns fit in the available width
        item_width = 240  # width of each faculty card
        padding = 20
        max_cols = max(1, int(available_width / (item_width + padding)))
        
        if max_cols != self.columns:
            self.columns = max_cols
            self.load_faculty_list()
    
    def load_faculty_list(self):
        """Load all faculty members into the grid layout"""
        # Clear existing grid items
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        try:
            # Get all professors
            professors = get_all_professors()
            
            # Sort professors by name
            professors = sorted(professors, key=lambda p: f"{p['f_name']} {p['l_name']}")
            
            # Create grid layout
            row, col = 0, 0
            
            for prof in professors:
                # Create faculty card
                card = FacultyCard(prof, self.controller)
                self.grid_layout.addWidget(card, row, col)
                
                # Update row and column for the next card
                col += 1
                if col >= self.columns:
                    col = 0
                    row += 1
            
            # If no faculty, show message
            if not professors:
                no_faculty_label = QLabel("No faculty members found.")
                no_faculty_label.setAlignment(Qt.AlignCenter)
                no_faculty_label.setStyleSheet("color: #666666; font-size: 14px;")
                self.grid_layout.addWidget(no_faculty_label, 0, 0, 1, self.columns)
                
        except Exception as e:
            error_label = QLabel(f"Error loading faculty: {str(e)}")
            error_label.setStyleSheet("color: red;")
            self.grid_layout.addWidget(error_label, 0, 0)
    
    def search_faculty(self, search_term):
        """Search faculty by name, email, or subject"""
        # Clear existing grid items
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        if not search_term:
            self.load_faculty_list()
            return
        
        try:
            # Search professors
            professors = search_professors(search_term)
            
            # Create grid layout for search results
            row, col = 0, 0
            
            for prof in professors:
                # Create faculty card
                card = FacultyCard(prof, self.controller)
                self.grid_layout.addWidget(card, row, col)
                
                # Update row and column for the next card
                col += 1
                if col >= self.columns:
                    col = 0
                    row += 1
                    
            # Show message if no results found
            if not professors:
                no_results_label = QLabel(f"No faculty members found matching '{search_term}'")
                no_results_label.setAlignment(Qt.AlignCenter)
                no_results_label.setStyleSheet("color: #666666; font-size: 14px;")
                self.grid_layout.addWidget(no_results_label, 0, 0, 1, self.columns)
                
        except Exception as e:
            error_label = QLabel(f"Error searching faculty: {str(e)}")
            error_label.setStyleSheet("color: red;")
            self.grid_layout.addWidget(error_label, 0, 0)
    
    def on_show(self):
        """Called when frame is shown"""
        self.load_faculty_list()