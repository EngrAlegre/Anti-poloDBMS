from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLineEdit, QMessageBox, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QSpacerItem, QSizePolicy,
                           QGridLayout, QComboBox, QTimeEdit)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont
import sqlite3
from database import (get_all_professors, get_all_courses, get_professor_schedule,
                    add_schedule, update_schedule, delete_schedule, get_all_schedules)
from ui.add_schedule_dialog import AddScheduleDialog

class ScheduleManagementFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_schedule_id = None
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
        title_label = QLabel("Schedule Management")
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
        
        # Table container
        table_container = QFrame()
        table_layout = QVBoxLayout(table_container)
        
        # Table title
        table_title = QLabel("Schedule List")
        table_title.setFont(QFont("Arial", 14, QFont.Bold))
        table_layout.addWidget(table_title)
        
        # Schedule table
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(8)
        self.schedule_table.setHorizontalHeaderLabels([
            "ID", "Professor", "Course", "Day", "Time", "Room", "Year", "Semester"
        ])
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.schedule_table.setSelectionMode(QTableWidget.SingleSelection)
        self.schedule_table.setEditTriggers(QTableWidget.NoEditTriggers)
        table_layout.addWidget(self.schedule_table)
        
        # Action buttons container
        action_container = QFrame()
        action_layout = QHBoxLayout(action_container)
        
        # Add button
        self.add_btn = QPushButton("Add New Schedule")
        self.add_btn.clicked.connect(self.show_add_dialog)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00;
                color: black;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 150px;
                font-weight: bold;
                border: 2px solid #333333;
            }
            QPushButton:hover {
                background-color: #FFE840;
            }
        """)
        action_layout.addWidget(self.add_btn, 0, Qt.AlignLeft)
        
        # Delete button
        self.delete_btn = QPushButton("Delete Selected Schedule")
        self.delete_btn.clicked.connect(self.delete_selected_schedule)
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
        
        # Connect table selection
        self.schedule_table.clicked.connect(self.on_table_click)
    
    def on_table_click(self):
        """Enable delete button when a row is selected"""
        selected_rows = self.schedule_table.selectedIndexes()
        if selected_rows:
            self.delete_btn.setEnabled(True)
            row = selected_rows[0].row()
            self.selected_schedule_id = int(self.schedule_table.item(row, 0).text())
        else:
            self.delete_btn.setEnabled(False)
            self.selected_schedule_id = None
    
    def show_add_dialog(self):
        """Show dialog to add a new schedule"""
        dialog = AddScheduleDialog(self)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            self.load_schedules()
            QMessageBox.information(self, "Success", "Schedule added successfully")
    
    def delete_selected_schedule(self):
        """Delete the selected schedule"""
        if not self.selected_schedule_id:
            return
            
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this schedule?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                success, msg = delete_schedule(self.selected_schedule_id)
                
                if success:
                    QMessageBox.information(self, "Success", "Schedule deleted successfully")
                    self.load_schedules()
                    self.selected_schedule_id = None
                    self.delete_btn.setEnabled(False)
                else:
                    QMessageBox.warning(self, "Error", msg)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete schedule: {str(e)}")
    
    def load_schedules(self):
        """Load schedules into table"""
        self.schedule_table.setRowCount(0)
        try:
            schedules = get_all_schedules()
            self.schedule_table.setRowCount(len(schedules))
            
            for i, sched in enumerate(schedules):
                self.schedule_table.setItem(i, 0, QTableWidgetItem(str(sched['schedule_id'])))
                
                professor_name = f"{sched['first_name']} {sched['last_name']}"
                self.schedule_table.setItem(i, 1, QTableWidgetItem(professor_name))
                
                self.schedule_table.setItem(i, 2, QTableWidgetItem(sched['course_code']))
                self.schedule_table.setItem(i, 3, QTableWidgetItem(sched['day_of_week']))
                
                time_str = f"{sched['start_time']} - {sched['end_time']}"
                self.schedule_table.setItem(i, 4, QTableWidgetItem(time_str))
                
                self.schedule_table.setItem(i, 5, QTableWidgetItem(sched['room_location']))
                self.schedule_table.setItem(i, 6, QTableWidgetItem(sched['academic_year']))
                self.schedule_table.setItem(i, 7, QTableWidgetItem(sched['semester_num']))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load schedules: {str(e)}")
    
    def on_show(self):
        """Called when frame is shown"""
        self.load_schedules()
        self.delete_btn.setEnabled(False)
        self.selected_schedule_id = None