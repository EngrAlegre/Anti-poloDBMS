# Faculty Finder

A desktop application designed to help students easily find and connect with faculty members at the university. Built with PyQt5 and SQLite.

![Faculty Finder]

## Features

- **Department Browsing**: Navigate through university departments
- **Faculty Profiles**: View detailed information about professors including:
  - Contact information
  - Office location
  - Department affiliation
  - Academic specialties
- **Teaching Schedules**: Check faculty teaching schedules and office hours
- **Admin Interface**: Secure admin section for maintaining faculty data

## Installation

### Prerequisites

- Python 3.6+
- PyQt5
- SQLite3

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/EngrAlegre/Anti-poloDBMS.git
   cd Anti-poloDBMS
   ```

2. Install required dependencies:
   ```
   pip install PyQt5
   ```

3. Run the application:
   ```
   python main.py
   ```

On first run, the application will automatically create a database with sample data.

## Usage

### Student View

1. **Browse Departments**: Click on the "Faculty" tab to see a list of all departments
2. **View Department Details**: Click on a department to see all faculty members in that department
3. **Faculty Profile**: Click on a faculty card to view their detailed profile
4. **View Schedule**: On a faculty profile, click "View Schedule" to see teaching hours

### Admin View

1. Click the "Admin" tab
2. Log in with admin credentials (default: admin/password)
3. Manage faculty, departments, courses, and schedules

## Project Structure

- `main.py`: Application entry point
- `database.py`: Database operations
- `ui/`: UI components
  - `departments_list.py`: Department browsing interface
  - `department_detail.py`: Department details with faculty listing
  - `faculty_detail.py`: Faculty member details
  - `schedule_view.py`: Faculty schedule display
  - `admin_*.py`: Admin interfaces

## Database Schema

The application uses SQLite with the following key tables:
- Professors
- Departments
- Courses
- Schedules
- Admin Users

## Development

This application was developed as part of the Database Management Systems course project using:

- PyQt5 for the user interface
- SQLite for data storage
- Object-oriented design principles

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- [EngrAlegre](https://github.com/EngrAlegre)

## Acknowledgments

- Thanks to all who contributed to the development of this project
- PyQt team for the excellent GUI framework 
