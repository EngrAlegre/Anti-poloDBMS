from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QScrollArea, QGridLayout, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor
import sqlite3
from database import get_all_departments

class DepartmentCard(QFrame):
    clicked = pyqtSignal(str)
    
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.department_name = name
        
        # Configure card style
        self.setStyleSheet("""
            QFrame {
                background-color: #333333;
                border-radius: 8px;
                color: white;
            }
            QFrame:hover {
                background-color: #444444;
            }
        """)
        
        # Set fixed size for card
        self.setFixedSize(200, 150)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Department name label
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 14, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: white;")
        name_label.setWordWrap(True)
        
        layout.addWidget(name_label)
        
        # Make card clickable
        self.setCursor(Qt.PointingHandCursor)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.department_name)

class DepartmentsListFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Set background color
        self.setStyleSheet("background-color: #FFDD00;")
        
        # Main container
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title at the top
        title_label = QLabel("Departments")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: black; background-color: #FFDD00;")
        title_label.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(title_label)
        
        # White content area with subtle background
        content_area = QFrame()
        content_area.setStyleSheet("""
            background-color: #FCFCFC;
        """)
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create scrollable area for departments
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Create widget to hold grid
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("""
            background-color: #FCFCFC;
        """)
        
        # Grid layout for departments
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(20)
        
        scroll_area.setWidget(self.scroll_content)
        content_layout.addWidget(scroll_area)
        
        main_layout.addWidget(content_area)
        
        # Track number of columns in grid
        self.columns = 3
        
        # Create departments grid
        self.create_departments_grid()
    
    def on_resize(self, window_width, window_height):
        # Calculate the available width (window width minus sidebar and padding)
        available_width = window_width - 240  # 200px sidebar + some padding
        self.adjust_grid_layout(available_width)
    
    def adjust_grid_layout(self, available_width):
        # Determine how many columns fit in the available width
        item_width = 200  # width of each department card
        padding = 20
        max_cols = max(1, int(available_width / (item_width + padding)))
        
        if max_cols != self.columns:
            self.columns = max_cols
            self.create_departments_grid()
    
    def create_departments_grid(self, max_cols=None):
        # Clear existing grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        # Set number of columns
        if max_cols is not None:
            self.columns = max_cols
        
        try:
            # Get all departments
            departments = get_all_departments()
            
            # Create department cards and add to grid
            row, col = 0, 0
            
            for dept in departments:
                department_name = dept[1]  # dept is a tuple (id, name)
                card = DepartmentCard(department_name)
                card.clicked.connect(self.show_department_detail)
                
                self.grid_layout.addWidget(card, row, col)
                
                # Move to next grid position
                col += 1
                if col >= self.columns:
                    col = 0
                    row += 1
                    
        except Exception as e:
            error_label = QLabel(f"Error loading departments: {str(e)}")
            error_label.setStyleSheet("color: red;")
            self.grid_layout.addWidget(error_label, 0, 0)
    
    def show_department_detail(self, department_name):
        self.controller.show_department_detail(department_name)
    
    def on_show(self):
        # Refresh departments when frame is shown
        self.create_departments_grid() 