import sqlite3
import os

def create_database():
    """Create the database schema based on the ERD"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    # Create Faculty table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faculty (
        office_id INTEGER PRIMARY KEY,
        office_name VARCHAR(20) NOT NULL,
        building_num INTEGER,
        room_num INTEGER
    )
    ''')
    
    # Create Professors table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS professors (
        faculty_id INTEGER PRIMARY KEY,
        f_name VARCHAR(100) NOT NULL,
        l_name VARCHAR(100) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        office_id INTEGER,
        subject_id VARCHAR(50),
        FOREIGN KEY (office_id) REFERENCES faculty(office_id)
    )
    ''')
    
    # Create Courses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        course_code VARCHAR(20) PRIMARY KEY,
        course_name VARCHAR(50)
    )
    ''')
    
    # Create Professor Schedule table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS professor_sched (
        schedule_id INTEGER PRIMARY KEY,
        faculty_id INTEGER,
        day_of_week TEXT CHECK(day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')),
        start_time TEXT,
        end_time TEXT,
        room_location VARCHAR(20),
        academic_year TEXT NOT NULL,
        semester_num TEXT CHECK(semester_num IN ('1st', '2nd', 'Summer')),
        course_code VARCHAR(20),
        FOREIGN KEY (faculty_id) REFERENCES professors(faculty_id),
        FOREIGN KEY (course_code) REFERENCES courses(course_code)
    )
    ''')
    
    # Create Admin Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin_users (
        admin_id INTEGER PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name VARCHAR(100),
        email VARCHAR(100),
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT 1
    )
    ''')
    
    conn.commit()
    conn.close()

def populate_sample_data():
    """Populate the database with sample data"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    # Insert sample faculty offices
    faculty_offices = [
        (1, 'Computer Engineering', 1, 101),
        (2, 'Software Engineering', 1, 102),
        (3, 'Network Engineering', 1, 103),
        (4, 'Hardware Engineering', 2, 201),
        (5, 'Systems Engineering', 2, 202)
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO faculty (office_id, office_name, building_num, room_num)
    VALUES (?, ?, ?, ?)
    ''', faculty_offices)
    
    # Insert sample professors
    professors = [
        (1, 'John', 'Smith', 'john.smith@university.edu', 1, 'Programming'),
        (2, 'Emily', 'Johnson', 'emily.johnson@university.edu', 2, 'Software Design'),
        (3, 'Michael', 'Williams', 'michael.williams@university.edu', 3, 'Networking'),
        (4, 'Sarah', 'Brown', 'sarah.brown@university.edu', 4, 'Hardware'),
        (5, 'David', 'Jones', 'david.jones@university.edu', 5, 'Systems')
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO professors (faculty_id, f_name, l_name, email, office_id, subject_id)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', professors)
    
    # Insert sample courses
    courses = [
        ('CS101', 'Introduction to Programming'),
        ('CS201', 'Data Structures and Algorithms'),
        ('CS301', 'Database Systems'),
        ('CS401', 'Computer Networks'),
        ('CS501', 'Computer Architecture')
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO courses (course_code, course_name)
    VALUES (?, ?)
    ''', courses)
    
    # Insert sample schedules
    schedules = [
        (1, 1, 'Monday', '08:00', '10:00', 'Room 101', '2023-2024', '1st', 'CS101'),
        (2, 1, 'Wednesday', '10:00', '12:00', 'Room 102', '2023-2024', '1st', 'CS201'),
        (3, 2, 'Tuesday', '09:00', '11:00', 'Room 103', '2023-2024', '1st', 'CS301'),
        (4, 3, 'Thursday', '13:00', '15:00', 'Room 201', '2023-2024', '1st', 'CS401'),
        (5, 4, 'Friday', '14:00', '16:00', 'Room 202', '2023-2024', '1st', 'CS501'),
        (6, 5, 'Monday', '15:00', '17:00', 'Room 101', '2023-2024', '1st', 'CS101')
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO professor_sched (schedule_id, faculty_id, day_of_week, start_time, end_time, 
                                         room_location, academic_year, semester_num, course_code)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', schedules)
    
    # Insert default admin user (username: admin, password: admin123)
    import hashlib
    default_username = 'admin'
    default_password = 'admin123'
    password_hash = hashlib.sha256(default_password.encode()).hexdigest()
    
    cursor.execute('''
    INSERT OR IGNORE INTO admin_users (username, password_hash, full_name, email)
    VALUES (?, ?, ?, ?)
    ''', (default_username, password_hash, 'Administrator', 'admin@university.edu'))
    
    conn.commit()
    conn.close()

def get_all_professors():
    """Get all professors from the database"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT p.faculty_id, p.f_name, p.l_name, p.email, p.subject_id,
           f.office_name, f.building_num, f.room_num
    FROM professors p
    LEFT JOIN faculty f ON p.office_id = f.office_id
    ORDER BY p.l_name, p.f_name
    ''')
    
    professors = cursor.fetchall()
    conn.close()
    
    return professors

def get_professor_by_id(faculty_id):
    """Get professor details by ID"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT p.faculty_id, p.f_name, p.l_name, p.email, p.subject_id,
           f.office_name, f.building_num, f.room_num
    FROM professors p
    LEFT JOIN faculty f ON p.office_id = f.office_id
    WHERE p.faculty_id = ?
    ''', (faculty_id,))
    
    professor = cursor.fetchone()
    conn.close()
    
    return professor

def get_professor_schedule(faculty_id):
    """Get schedule for a professor"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT ps.schedule_id, ps.day_of_week, ps.start_time, ps.end_time,
           ps.room_location, ps.academic_year, ps.semester_num,
           c.course_code, c.course_name
    FROM professor_sched ps
    LEFT JOIN courses c ON ps.course_code = c.course_code
    WHERE ps.faculty_id = ?
    ORDER BY 
        CASE ps.day_of_week
            WHEN 'Monday' THEN 1
            WHEN 'Tuesday' THEN 2
            WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4
            WHEN 'Friday' THEN 5
            WHEN 'Saturday' THEN 6
        END,
        ps.start_time
    ''', (faculty_id,))
    
    schedule = cursor.fetchall()
    conn.close()
    
    return schedule

def search_professors(search_term):
    """Search professors by name, email, or subject"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    search_pattern = f'%{search_term}%'
    
    # Check if search term contains a space (might be a full name)
    if ' ' in search_term:
        # Split the search term into parts (assuming first and last name)
        name_parts = search_term.split()
        if len(name_parts) >= 2:
            first_name_pattern = f'%{name_parts[0]}%'
            last_name_pattern = f'%{name_parts[1]}%'
            
            # Search for both first and last name match
            cursor.execute('''
            SELECT p.faculty_id, p.f_name, p.l_name, p.email, p.subject_id,
                   f.office_name, f.building_num, f.room_num
            FROM professors p
            LEFT JOIN faculty f ON p.office_id = f.office_id
            WHERE (p.f_name LIKE ? AND p.l_name LIKE ?) OR p.email LIKE ? OR p.subject_id LIKE ?
            ORDER BY p.l_name, p.f_name
            ''', (first_name_pattern, last_name_pattern, search_pattern, search_pattern))
    else:
        # Regular search for single terms
        cursor.execute('''
        SELECT p.faculty_id, p.f_name, p.l_name, p.email, p.subject_id,
               f.office_name, f.building_num, f.room_num
        FROM professors p
        LEFT JOIN faculty f ON p.office_id = f.office_id
        WHERE p.f_name LIKE ? OR p.l_name LIKE ? OR p.email LIKE ? OR p.subject_id LIKE ?
        ORDER BY p.l_name, p.f_name
        ''', (search_pattern, search_pattern, search_pattern, search_pattern))
    
    professors = cursor.fetchall()
    conn.close()
    
    return professors

def filter_professors_by_faculty(office_name):
    """Filter professors by faculty office"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT p.faculty_id, p.f_name, p.l_name, p.email, p.subject_id,
           f.office_name, f.building_num, f.room_num
    FROM professors p
    LEFT JOIN faculty f ON p.office_id = f.office_id
    WHERE f.office_name = ?
    ORDER BY p.l_name, p.f_name
    ''', (office_name,))
    
    professors = cursor.fetchall()
    conn.close()
    
    return professors

def filter_professors_by_course(course_name):
    """Filter professors by course they teach"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT DISTINCT p.faculty_id, p.f_name, p.l_name, p.email, p.subject_id,
           f.office_name, f.building_num, f.room_num
    FROM professors p
    LEFT JOIN faculty f ON p.office_id = f.office_id
    JOIN professor_sched ps ON p.faculty_id = ps.faculty_id
    JOIN courses c ON ps.course_code = c.course_code
    WHERE c.course_name = ?
    ORDER BY p.l_name, p.f_name
    ''', (course_name,))
    
    professors = cursor.fetchall()
    conn.close()
    
    return professors

def get_all_faculties():
    """Get all faculty offices"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM faculty ORDER BY office_name')
    
    faculties = cursor.fetchall()
    conn.close()
    
    return faculties

def get_all_courses():
    """Get all courses"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM courses ORDER BY course_code')
    
    courses = cursor.fetchall()
    conn.close()
    
    return courses


def add_professor(f_name, l_name, email, office_id, subject_id):
    """Add a new professor to the database"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO professors (f_name, l_name, email, office_id, subject_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (f_name, l_name, email, office_id, subject_id))
        conn.commit()
        conn.close()
        return True, "Professor added successfully."
    except sqlite3.IntegrityError as e:
        conn.close()
        if 'UNIQUE constraint failed: professors.email' in str(e):
            return False, f"Error: Email '{email}' already exists."
        else:
            return False, f"Database integrity error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def get_all_departments():
    """Get all unique departments/office names"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT DISTINCT office_id, office_name
    FROM faculty
    ORDER BY office_name
    ''')
    
    departments = cursor.fetchall()
    conn.close()
    
    return departments

def get_professors_by_department(department_name):
    """Get all professors in a specific department"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT p.faculty_id, p.l_name, p.f_name, p.email, p.subject_id,
           f.office_name, f.building_num, f.room_num
    FROM professors p
    JOIN faculty f ON p.office_id = f.office_id
    WHERE f.office_name = ?
    ORDER BY p.l_name, p.f_name
    ''', (department_name,))
    
    professors = cursor.fetchall()
    conn.close()
    
    return professors

# Admin authentication functions
def authenticate_admin(username, password):
    """Authenticate an admin user"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    # Hash the provided password
    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
    SELECT admin_id, username, full_name
    FROM admin_users
    WHERE username = ? AND password_hash = ? AND is_active = 1
    ''', (username, password_hash))
    
    admin = cursor.fetchone()
    
    if admin:
        # Update last login time
        import datetime
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
        UPDATE admin_users SET last_login = ? WHERE admin_id = ?
        ''', (current_time, admin[0]))
        conn.commit()
    
    conn.close()
    return admin

def update_admin_password(admin_id, current_password, new_password):
    """Update an admin user's password"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    # Verify current password
    import hashlib
    current_hash = hashlib.sha256(current_password.encode()).hexdigest()
    
    cursor.execute('''
    SELECT admin_id FROM admin_users
    WHERE admin_id = ? AND password_hash = ?
    ''', (admin_id, current_hash))
    
    admin = cursor.fetchone()
    
    if not admin:
        conn.close()
        return False, "Current password is incorrect"
    
    # Update to new password
    new_hash = hashlib.sha256(new_password.encode()).hexdigest()
    
    cursor.execute('''
    UPDATE admin_users SET password_hash = ? WHERE admin_id = ?
    ''', (new_hash, admin_id))
    
    conn.commit()
    conn.close()
    
    return True, "Password updated successfully"

def get_all_admin_users():
    """Get all admin users"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT admin_id, username, full_name, email, last_login, is_active
    FROM admin_users
    ORDER BY username
    ''')
    
    admins = cursor.fetchall()
    conn.close()
    
    return admins

def create_admin_user(username, password, full_name, email):
    """Create a new admin user"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Hash the password
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
        INSERT INTO admin_users (username, password_hash, full_name, email, is_active)
        VALUES (?, ?, ?, ?, 1)
        ''', (username, password_hash, full_name, email))
        
        conn.commit()
        conn.close()
        return True, "Admin user created successfully"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists"
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def update_professor(faculty_id, f_name, l_name, email, office_id, subject_id):
    """Update an existing professor"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if the email already exists for a different professor
        cursor.execute('''
        SELECT faculty_id FROM professors WHERE email = ? AND faculty_id != ?
        ''', (email, faculty_id))
        
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return False, f"Email '{email}' is already in use by another professor"
        
        # Update the professor
        cursor.execute('''
        UPDATE professors
        SET f_name = ?, l_name = ?, email = ?, office_id = ?, subject_id = ?
        WHERE faculty_id = ?
        ''', (f_name, l_name, email, office_id, subject_id, faculty_id))
        
        conn.commit()
        conn.close()
        return True, "Professor updated successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def delete_professor(faculty_id):
    """Delete a professor and related data"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if professor exists
        cursor.execute('SELECT faculty_id FROM professors WHERE faculty_id = ?', (faculty_id,))
        professor = cursor.fetchone()
        
        if not professor:
            conn.close()
            return False, "Professor not found"
        
        # Begin transaction
        conn.execute('BEGIN TRANSACTION')
        
        # Delete associated schedules first (foreign key constraint)
        cursor.execute('DELETE FROM professor_sched WHERE faculty_id = ?', (faculty_id,))
        
        # Delete the professor
        cursor.execute('DELETE FROM professors WHERE faculty_id = ?', (faculty_id,))
        
        # Commit transaction
        conn.commit()
        conn.close()
        return True, "Professor deleted successfully"
    except sqlite3.Error as e:
        # Rollback on error
        conn.rollback()
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        # Rollback on error
        conn.rollback()
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def ensure_admin_table_exists():
    """Ensure that the admin_users table exists and has a default admin user"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    # Check if admin_users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin_users'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        # Create Admin Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            admin_id INTEGER PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name VARCHAR(100),
            email VARCHAR(100),
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
        ''')
        
        # Insert default admin user (username: admin, password: admin123)
        import hashlib
        default_username = 'admin'
        default_password = 'admin123'
        password_hash = hashlib.sha256(default_password.encode()).hexdigest()
        
        cursor.execute('''
        INSERT OR IGNORE INTO admin_users (username, password_hash, full_name, email)
        VALUES (?, ?, ?, ?)
        ''', (default_username, password_hash, 'Administrator', 'admin@university.edu'))
        
        conn.commit()
        print("Admin users table created and default admin user added.")
    
    conn.close()

# Department management functions
def add_department(office_name, building_num, room_num):
    """Add a new department"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if department name already exists
        cursor.execute('SELECT office_id FROM faculty WHERE office_name = ?', (office_name,))
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return False, f"Department '{office_name}' already exists"
        
        # Insert the new department
        cursor.execute('''
        INSERT INTO faculty (office_name, building_num, room_num)
        VALUES (?, ?, ?)
        ''', (office_name, building_num, room_num))
        
        conn.commit()
        conn.close()
        return True, "Department added successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def update_department(office_id, office_name, building_num, room_num):
    """Update an existing department"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if department exists
        cursor.execute('SELECT office_id FROM faculty WHERE office_id = ?', (office_id,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            return False, "Department not found"
        
        # Check if the new name conflicts with another department
        cursor.execute('SELECT office_id FROM faculty WHERE office_name = ? AND office_id != ?', 
                      (office_name, office_id))
        name_conflict = cursor.fetchone()
        if name_conflict:
            conn.close()
            return False, f"Department name '{office_name}' is already in use"
        
        # Update the department
        cursor.execute('''
        UPDATE faculty 
        SET office_name = ?, building_num = ?, room_num = ?
        WHERE office_id = ?
        ''', (office_name, building_num, room_num, office_id))
        
        conn.commit()
        conn.close()
        return True, "Department updated successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def delete_department(office_id):
    """Delete a department and update related professors"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if department exists
        cursor.execute('SELECT office_id FROM faculty WHERE office_id = ?', (office_id,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            return False, "Department not found"
        
        # Begin transaction
        conn.execute('BEGIN TRANSACTION')
        
        # Check for professors in this department
        cursor.execute('SELECT faculty_id FROM professors WHERE office_id = ?', (office_id,))
        affected_professors = cursor.fetchall()
        
        # Update professors to set office_id to NULL
        if affected_professors:
            cursor.execute('''
            UPDATE professors SET office_id = NULL
            WHERE office_id = ?
            ''', (office_id,))
        
        # Delete the department
        cursor.execute('DELETE FROM faculty WHERE office_id = ?', (office_id,))
        
        # Commit the transaction
        conn.commit()
        conn.close()
        
        affected_count = len(affected_professors)
        if affected_count > 0:
            return True, f"Department deleted successfully. {affected_count} professor(s) were affected."
        else:
            return True, "Department deleted successfully"
    except sqlite3.Error as e:
        # Rollback on error
        conn.rollback()
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        # Rollback on error
        conn.rollback()
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

# Course management functions
def add_course(course_code, course_name):
    """Add a new course"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if course code already exists
        cursor.execute('SELECT course_code FROM courses WHERE course_code = ?', (course_code,))
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return False, f"Course code '{course_code}' already exists"
        
        # Insert the new course
        cursor.execute('''
        INSERT INTO courses (course_code, course_name)
        VALUES (?, ?)
        ''', (course_code, course_name))
        
        conn.commit()
        conn.close()
        return True, "Course added successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def update_course(course_code, course_name):
    """Update an existing course (only name can be changed, not code)"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if course exists
        cursor.execute('SELECT course_code FROM courses WHERE course_code = ?', (course_code,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            return False, "Course not found"
        
        # Update the course name
        cursor.execute('''
        UPDATE courses 
        SET course_name = ?
        WHERE course_code = ?
        ''', (course_name, course_code))
        
        conn.commit()
        conn.close()
        return True, "Course updated successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def delete_course(course_code):
    """Delete a course and remove references in schedules"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if course exists
        cursor.execute('SELECT course_code FROM courses WHERE course_code = ?', (course_code,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            return False, "Course not found"
        
        # Begin transaction
        conn.execute('BEGIN TRANSACTION')
        
        # Check for schedule entries with this course
        cursor.execute('SELECT schedule_id FROM professor_sched WHERE course_code = ?', (course_code,))
        affected_schedules = cursor.fetchall()
        
        # Remove course from schedules or delete schedule entries
        if affected_schedules:
            cursor.execute('''
            DELETE FROM professor_sched
            WHERE course_code = ?
            ''', (course_code,))
        
        # Delete the course
        cursor.execute('DELETE FROM courses WHERE course_code = ?', (course_code,))
        
        # Commit the transaction
        conn.commit()
        conn.close()
        
        affected_count = len(affected_schedules)
        if affected_count > 0:
            return True, f"Course deleted successfully. {affected_count} schedule entries were removed."
        else:
            return True, "Course deleted successfully"
    except sqlite3.Error as e:
        # Rollback on error
        conn.rollback()
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        # Rollback on error
        conn.rollback()
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

# Schedule management functions
def add_schedule_item(faculty_id, day_of_week, start_time, end_time, room_location, academic_year, semester_num, course_code):
    """Add a new schedule item for a professor"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if professor exists
        cursor.execute('SELECT faculty_id FROM professors WHERE faculty_id = ?', (faculty_id,))
        existing_prof = cursor.fetchone()
        if not existing_prof:
            conn.close()
            return False, "Professor not found"
        
        # Check if course exists
        cursor.execute('SELECT course_code FROM courses WHERE course_code = ?', (course_code,))
        existing_course = cursor.fetchone()
        if not existing_course:
            conn.close()
            return False, "Course not found"
        
        # Check for schedule conflicts
        cursor.execute('''
        SELECT schedule_id FROM professor_sched 
        WHERE faculty_id = ? AND day_of_week = ? AND 
        ((start_time <= ? AND end_time > ?) OR 
         (start_time < ? AND end_time >= ?) OR
         (start_time >= ? AND end_time <= ?))
        ''', (faculty_id, day_of_week, start_time, start_time, end_time, end_time, start_time, end_time))
        
        conflict = cursor.fetchone()
        if conflict:
            conn.close()
            return False, f"Schedule conflict: Professor already has a class during this time on {day_of_week}"
        
        # Validate day of week
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if day_of_week not in valid_days:
            conn.close()
            return False, f"Invalid day of week. Must be one of: {', '.join(valid_days)}"
        
        # Validate semester
        valid_semesters = ['1st', '2nd', 'Summer']
        if semester_num not in valid_semesters:
            conn.close()
            return False, f"Invalid semester. Must be one of: {', '.join(valid_semesters)}"
        
        # Insert the new schedule item
        cursor.execute('''
        INSERT INTO professor_sched (faculty_id, day_of_week, start_time, end_time, 
                                   room_location, academic_year, semester_num, course_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (faculty_id, day_of_week, start_time, end_time, room_location, 
             academic_year, semester_num, course_code))
        
        conn.commit()
        conn.close()
        return True, "Schedule item added successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def update_schedule_item(schedule_id, faculty_id, day_of_week, start_time, end_time, room_location, academic_year, semester_num, course_code):
    """Update an existing schedule item"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if schedule item exists
        cursor.execute('SELECT schedule_id FROM professor_sched WHERE schedule_id = ?', (schedule_id,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            return False, "Schedule item not found"
        
        # Check if professor exists
        cursor.execute('SELECT faculty_id FROM professors WHERE faculty_id = ?', (faculty_id,))
        existing_prof = cursor.fetchone()
        if not existing_prof:
            conn.close()
            return False, "Professor not found"
        
        # Check if course exists
        cursor.execute('SELECT course_code FROM courses WHERE course_code = ?', (course_code,))
        existing_course = cursor.fetchone()
        if not existing_course:
            conn.close()
            return False, "Course not found"
        
        # Check for schedule conflicts with other schedule items
        cursor.execute('''
        SELECT schedule_id FROM professor_sched 
        WHERE faculty_id = ? AND day_of_week = ? AND schedule_id != ? AND 
        ((start_time <= ? AND end_time > ?) OR 
         (start_time < ? AND end_time >= ?) OR
         (start_time >= ? AND end_time <= ?))
        ''', (faculty_id, day_of_week, schedule_id, start_time, start_time, end_time, end_time, start_time, end_time))
        
        conflict = cursor.fetchone()
        if conflict:
            conn.close()
            return False, f"Schedule conflict: Professor already has a class during this time on {day_of_week}"
        
        # Validate day of week
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if day_of_week not in valid_days:
            conn.close()
            return False, f"Invalid day of week. Must be one of: {', '.join(valid_days)}"
        
        # Validate semester
        valid_semesters = ['1st', '2nd', 'Summer']
        if semester_num not in valid_semesters:
            conn.close()
            return False, f"Invalid semester. Must be one of: {', '.join(valid_semesters)}"
        
        # Update the schedule item
        cursor.execute('''
        UPDATE professor_sched 
        SET faculty_id = ?, day_of_week = ?, start_time = ?, end_time = ?, 
            room_location = ?, academic_year = ?, semester_num = ?, course_code = ?
        WHERE schedule_id = ?
        ''', (faculty_id, day_of_week, start_time, end_time, room_location, 
             academic_year, semester_num, course_code, schedule_id))
        
        conn.commit()
        conn.close()
        return True, "Schedule item updated successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def delete_schedule_item(schedule_id):
    """Delete a schedule item"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if schedule item exists
        cursor.execute('SELECT schedule_id FROM professor_sched WHERE schedule_id = ?', (schedule_id,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            return False, "Schedule item not found"
        
        # Delete the schedule item
        cursor.execute('DELETE FROM professor_sched WHERE schedule_id = ?', (schedule_id,))
        
        conn.commit()
        conn.close()
        return True, "Schedule item deleted successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

