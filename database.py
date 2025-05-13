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
        photo_url TEXT,
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
    
    # Ensure photos directory exists
    ensure_photos_directory_exists()

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
    SELECT p.faculty_id, p.f_name as first_name, p.l_name as last_name, p.email, p.subject_id,
           f.office_name as department_name, f.building_num, f.room_num, p.photo_url
    FROM professors p
    LEFT JOIN faculty f ON p.office_id = f.office_id
    ORDER BY p.l_name, p.f_name
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert sqlite3.Row objects to dictionaries and add phone numbers
    professors = []
    phil_prefixes = ["+63", "09"]
    import random
    
    for row in rows:
        prof_dict = dict(row)
        # Generate a random Philippine phone number
        prefix = random.choice(phil_prefixes)
        if prefix == "+63":
            # Format: +63 XXX XXX XXXX
            phone_number = f"{prefix} {random.randint(900, 999)} {random.randint(100, 999)} {random.randint(1000, 9999)}"
        else:
            # Format: 09XX XXX XXXX
            phone_number = f"{prefix}{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}"
        
        prof_dict['phone'] = phone_number
        professors.append(prof_dict)
    
    return professors

def get_professor_by_id(faculty_id):
    """Get professor details by ID"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT p.faculty_id, p.f_name as first_name, p.l_name as last_name, p.email, p.subject_id,
           f.office_name as department_name, f.building_num, f.room_num, p.photo_url
    FROM professors p
    LEFT JOIN faculty f ON p.office_id = f.office_id
    WHERE p.faculty_id = ?
    ''', (faculty_id,))
    
    professor = cursor.fetchone()
    conn.close()
    
    # Convert to dictionary to make it easier to work with
    if professor:
        professor_dict = dict(professor)
        return professor_dict
    return None

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
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to dictionaries
    schedule = [dict(row) for row in rows]
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
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to dictionaries
    faculties = [dict(row) for row in rows]
    return faculties

def get_all_courses():
    """Get all courses"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM courses ORDER BY course_code')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to dictionaries
    courses = [dict(row) for row in rows]
    return courses

def ensure_photos_directory_exists():
    """Ensure the photos directory exists for faculty photos"""
    photos_dir = "assets/photos"
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir, exist_ok=True)
    return photos_dir

def add_professor(first_name, last_name, email, phone, department_name, specialty=None, photo_url=None):
    """Add a new professor"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Ensure photos directory exists
        ensure_photos_directory_exists()
        
        # Get office_id from department name
        cursor.execute('SELECT office_id FROM faculty WHERE office_name = ?', (department_name,))
        office_row = cursor.fetchone()
        
        if not office_row:
            raise ValueError(f"Department '{department_name}' not found")
        
        office_id = office_row[0]
        
        # Insert the new professor
        cursor.execute('''
        INSERT INTO professors (f_name, l_name, email, office_id, subject_id, photo_url)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, office_id, specialty, photo_url))
        
        faculty_id = cursor.lastrowid
        conn.commit()
        
        return faculty_id
    
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE constraint failed: professors.email" in str(e):
            raise ValueError(f"Email '{email}' is already in use by another professor")
        else:
            raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_all_departments():
    """Get all departments"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT f.office_id, f.office_name, f.building_num, f.room_num,
           COUNT(p.faculty_id) as faculty_count
    FROM faculty f
    LEFT JOIN professors p ON f.office_id = p.office_id
    GROUP BY f.office_id
    ORDER BY f.office_name
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to dictionaries
    departments = [dict(row) for row in rows]
    return departments

def get_professors_by_department(department_name):
    """Get all professors in a specific department"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT p.faculty_id, p.f_name as first_name, p.l_name as last_name, p.email, p.subject_id,
           f.office_name as department_name, f.building_num, f.room_num, p.photo_url
    FROM professors p
    JOIN faculty f ON p.office_id = f.office_id
    WHERE f.office_name = ?
    ORDER BY p.l_name, p.f_name
    ''', (department_name,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to dictionaries
    professors = [dict(row) for row in rows]
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

def update_professor(faculty_id, first_name, last_name, email, phone, department_name, specialty=None, photo_url=None):
    """Update an existing professor"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Ensure photos directory exists
        ensure_photos_directory_exists()
        
        # Get office_id from department name
        cursor.execute('SELECT office_id FROM faculty WHERE office_name = ?', (department_name,))
        office_row = cursor.fetchone()
        
        if not office_row:
            raise ValueError(f"Department '{department_name}' not found")
        
        office_id = office_row[0]
        
        # Check if faculty_id exists
        cursor.execute('SELECT faculty_id FROM professors WHERE faculty_id = ?', (faculty_id,))
        if not cursor.fetchone():
            raise ValueError(f"Professor with ID {faculty_id} not found")
        
        # Update the professor
        cursor.execute('''
        UPDATE professors 
        SET f_name = ?, l_name = ?, email = ?, office_id = ?, subject_id = ?, photo_url = ?
        WHERE faculty_id = ?
        ''', (first_name, last_name, email, office_id, specialty, photo_url, faculty_id))
        
        conn.commit()
        return True
    
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE constraint failed: professors.email" in str(e):
            raise ValueError(f"Email '{email}' is already in use by another professor")
        else:
            raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_professor(faculty_id):
    """Delete a professor"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if professor exists
        cursor.execute('SELECT faculty_id FROM professors WHERE faculty_id = ?', (faculty_id,))
        professor = cursor.fetchone()
        if not professor:
            conn.close()
            return False, "Professor does not exist"
        
        # Delete professor's schedules first
        cursor.execute('DELETE FROM professor_sched WHERE faculty_id = ?', (faculty_id,))
        
        # Delete the professor
        cursor.execute('DELETE FROM professors WHERE faculty_id = ?', (faculty_id,))
        
        conn.commit()
        conn.close()
        return True, "Professor deleted successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def ensure_photo_url_column():
    """Ensure that the professors table has a photo_url column"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    # Check if photo_url column exists in professors table
    cursor.execute("PRAGMA table_info(professors)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    
    if 'photo_url' not in column_names:
        try:
            # Add photo_url column
            cursor.execute("ALTER TABLE professors ADD COLUMN photo_url TEXT")
            conn.commit()
            print("Added photo_url column to professors table")
        except sqlite3.Error as e:
            print(f"Error adding photo_url column: {e}")
    
    conn.close()

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
        
        # Add default admin user
        import hashlib
        default_username = 'admin'
        default_password = 'admin123'
        password_hash = hashlib.sha256(default_password.encode()).hexdigest()
        
        cursor.execute('''
        INSERT INTO admin_users (username, password_hash, full_name, email, is_active)
        VALUES (?, ?, ?, ?, 1)
        ''', (default_username, password_hash, 'Administrator', 'admin@university.edu'))
        
        conn.commit()
        print("Created admin_users table and added default admin user")
    
    conn.close()
    
    # Also ensure photo_url column exists
    ensure_photo_url_column()

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
        department = cursor.fetchone()
        if not department:
            conn.close()
            return False, "Department does not exist"
        
        # Check if new name already exists for another department
        cursor.execute('SELECT office_id FROM faculty WHERE office_name = ? AND office_id != ?', 
                       (office_name, office_id))
        existing = cursor.fetchone()
        if existing:
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
    """Delete a department"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if department exists
        cursor.execute('SELECT office_id FROM faculty WHERE office_id = ?', (office_id,))
        department = cursor.fetchone()
        if not department:
            conn.close()
            return False, "Department does not exist"
        
        # Check if there are professors in this department
        cursor.execute('SELECT COUNT(*) FROM professors WHERE office_id = ?', (office_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            # This implementation deletes professors in the department
            
            # Get faculty IDs in this department
            cursor.execute('SELECT faculty_id FROM professors WHERE office_id = ?', (office_id,))
            faculty_ids = [row[0] for row in cursor.fetchall()]
            
            # Delete schedules for these faculty
            for faculty_id in faculty_ids:
                cursor.execute('DELETE FROM professor_sched WHERE faculty_id = ?', (faculty_id,))
            
            # Delete professors in this department
            cursor.execute('DELETE FROM professors WHERE office_id = ?', (office_id,))
        
        # Delete the department
        cursor.execute('DELETE FROM faculty WHERE office_id = ?', (office_id,))
        
        conn.commit()
        conn.close()
        return True, "Department deleted successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
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
    """Update an existing course"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if course exists
        cursor.execute('SELECT course_code FROM courses WHERE course_code = ?', (course_code,))
        course = cursor.fetchone()
        if not course:
            conn.close()
            return False, f"Course '{course_code}' does not exist"
        
        # Update the course
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
    """Delete a course"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if course exists
        cursor.execute('SELECT course_code FROM courses WHERE course_code = ?', (course_code,))
        course = cursor.fetchone()
        if not course:
            conn.close()
            return False, f"Course '{course_code}' does not exist"
        
        # Check if there are schedules using this course
        cursor.execute('SELECT COUNT(*) FROM professor_sched WHERE course_code = ?', (course_code,))
        count = cursor.fetchone()[0]
        if count > 0:
            # Delete schedules using this course
            cursor.execute('DELETE FROM professor_sched WHERE course_code = ?', (course_code,))
        
        # Delete the course
        cursor.execute('DELETE FROM courses WHERE course_code = ?', (course_code,))
        
        conn.commit()
        conn.close()
        return True, "Course deleted successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
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

def get_all_schedules():
    """Get all professor schedules"""
    conn = sqlite3.connect('faculty_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT s.schedule_id, s.faculty_id, p.f_name as first_name, p.l_name as last_name,
           s.day_of_week, s.start_time, s.end_time, s.room_location,
           s.academic_year, s.semester_num, s.course_code
    FROM professor_sched s
    JOIN professors p ON s.faculty_id = p.faculty_id
    ORDER BY p.l_name, p.f_name, s.day_of_week, s.start_time
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to dictionaries
    schedules = [dict(row) for row in rows]
    return schedules

def add_schedule(faculty_id, day_of_week, start_time, end_time, room_location, 
                academic_year, semester_num, course_code):
    """Add a new schedule for a professor"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if professor exists
        cursor.execute('SELECT faculty_id FROM professors WHERE faculty_id = ?', (faculty_id,))
        professor = cursor.fetchone()
        if not professor:
            conn.close()
            return False, "Professor does not exist"
        
        # Check if course exists
        cursor.execute('SELECT course_code FROM courses WHERE course_code = ?', (course_code,))
        course = cursor.fetchone()
        if not course:
            conn.close()
            return False, f"Course '{course_code}' does not exist"
        
        # Check for scheduling conflicts
        cursor.execute('''
        SELECT COUNT(*) FROM professor_sched
        WHERE faculty_id = ? AND day_of_week = ? AND 
              ((start_time <= ? AND end_time > ?) OR 
               (start_time < ? AND end_time >= ?) OR
               (start_time >= ? AND end_time <= ?))
        ''', (faculty_id, day_of_week, start_time, start_time, 
              end_time, end_time, start_time, end_time))
        
        conflicts = cursor.fetchone()[0]
        if conflicts > 0:
            conn.close()
            return False, "Schedule conflicts with an existing schedule for this professor"
        
        # Insert the new schedule
        cursor.execute('''
        INSERT INTO professor_sched (faculty_id, day_of_week, start_time, end_time, 
                                   room_location, academic_year, semester_num, course_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (faculty_id, day_of_week, start_time, end_time, 
             room_location, academic_year, semester_num, course_code))
        
        conn.commit()
        conn.close()
        return True, "Schedule added successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def update_schedule(schedule_id, faculty_id, day_of_week, start_time, end_time, 
                   room_location, academic_year, semester_num, course_code):
    """Update an existing schedule"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if schedule exists
        cursor.execute('SELECT schedule_id FROM professor_sched WHERE schedule_id = ?', (schedule_id,))
        schedule = cursor.fetchone()
        if not schedule:
            conn.close()
            return False, "Schedule does not exist"
        
        # Check if professor exists
        cursor.execute('SELECT faculty_id FROM professors WHERE faculty_id = ?', (faculty_id,))
        professor = cursor.fetchone()
        if not professor:
            conn.close()
            return False, "Professor does not exist"
        
        # Check if course exists
        cursor.execute('SELECT course_code FROM courses WHERE course_code = ?', (course_code,))
        course = cursor.fetchone()
        if not course:
            conn.close()
            return False, f"Course '{course_code}' does not exist"
        
        # Check for scheduling conflicts (excluding this schedule)
        cursor.execute('''
        SELECT COUNT(*) FROM professor_sched
        WHERE faculty_id = ? AND day_of_week = ? AND schedule_id != ? AND
              ((start_time <= ? AND end_time > ?) OR 
               (start_time < ? AND end_time >= ?) OR
               (start_time >= ? AND end_time <= ?))
        ''', (faculty_id, day_of_week, schedule_id, start_time, start_time, 
              end_time, end_time, start_time, end_time))
        
        conflicts = cursor.fetchone()[0]
        if conflicts > 0:
            conn.close()
            return False, "Schedule conflicts with an existing schedule for this professor"
        
        # Update the schedule
        cursor.execute('''
        UPDATE professor_sched 
        SET faculty_id = ?, day_of_week = ?, start_time = ?, end_time = ?,
            room_location = ?, academic_year = ?, semester_num = ?, course_code = ?
        WHERE schedule_id = ?
        ''', (faculty_id, day_of_week, start_time, end_time, room_location, 
             academic_year, semester_num, course_code, schedule_id))
        
        conn.commit()
        conn.close()
        return True, "Schedule updated successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

def delete_schedule(schedule_id):
    """Delete a schedule"""
    conn = sqlite3.connect('faculty_db.sqlite')
    cursor = conn.cursor()
    
    try:
        # Check if schedule exists
        cursor.execute('SELECT schedule_id FROM professor_sched WHERE schedule_id = ?', (schedule_id,))
        schedule = cursor.fetchone()
        if not schedule:
            conn.close()
            return False, "Schedule does not exist"
        
        # Delete the schedule
        cursor.execute('DELETE FROM professor_sched WHERE schedule_id = ?', (schedule_id,))
        
        conn.commit()
        conn.close()
        return True, "Schedule deleted successfully"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {str(e)}"

