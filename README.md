# Faculty Finder Application

A desktop application to help students easily find faculty members at the university, view their details, and check their teaching schedules.

## Features

- Browse faculty members across departments
- View faculty details including contact information and profile photos
- Check faculty teaching schedules
- Search for specific faculty members
- Admin panel for managing faculty, departments, courses, and schedules
- Complete schedule management system for adding and removing faculty schedules

## Technology Stack

- **Python**: Core programming language
- **PyQt5**: GUI framework
- **SQLite**: Database engine

## Installation and Setup

1. Ensure you have Python 3.7 or higher installed
2. Install required dependencies:
   ```bash
   pip install PyQt5 sqlite3
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Database Structure

The application uses SQLite for data storage with the following tables:
- `faculty`: Departments and office information
- `professors`: Faculty member details
- `courses`: Course information
- `professor_sched`: Teaching schedules
- `admin_users`: Admin authentication

## Recent Updates

- Added complete schedule management with Add Schedule functionality
- Improved UI with consistent yellow accent color (#FFDD00) across the application
- Added faculty photo display functionality
- Fixed indentation issues in Python files
- Added comprehensive database documentation
- Resolved ERD discrepancies

## Admin Access

Default admin credentials:
- Username: admin
- Password: admin123

## Development

To modify or extend the application:

1. Clone the repository
2. Make changes to the relevant files:
   - `main.py`: Application entry point and main window setup
   - `database.py`: Database operations
   - `ui/` directory: Individual UI components

## License

This project is licensed under the MIT License.

## Contributors

- [EngrAlegre](https://github.com/EngrAlegre)

## Acknowledgments

- Thanks to all who contributed to the development of this project
- PyQt team for the excellent GUI framework 
