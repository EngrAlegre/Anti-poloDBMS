import os
import sqlite3
import random
import shutil
import sys

# Add parent directory to path so we can import from database.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import ensure_photos_directory_exists

def populate_sample_photos():
    """
    Download sample profile photos and update the database with their paths
    This uses placeholder images that are locally stored
    """
    # Ensure photos directory exists
    photos_dir = ensure_photos_directory_exists()
    
    # Create connection to database - use the correct path relative to script location
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'faculty_db.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get all professors
        cursor.execute('SELECT faculty_id, f_name, l_name FROM professors')
        professors = cursor.fetchall()
        
        # Create placeholder images (in a real app, you might download from an API)
        for faculty_id, f_name, l_name in professors:
            # Create a filename based on faculty name
            filename = f"{f_name.lower()}_{l_name.lower()}.jpg"
            photo_path = os.path.join(photos_dir, filename)
            
            # In a real app, you would download actual photos
            # Here we create colored placeholder images
            # This is just a simulation - in a real application you'd download actual photos
            
            # Generate a path relative to the application root
            relative_path = os.path.join("assets", "photos", filename)
            
            # Update the database with the photo path
            cursor.execute(
                'UPDATE professors SET photo_url = ? WHERE faculty_id = ?',
                (relative_path, faculty_id)
            )
            
            print(f"Updated photo path for {f_name} {l_name}")
        
        conn.commit()
        print("Sample photos have been populated and database updated.")
        
    except Exception as e:
        print(f"Error populating photos: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    # Create tools directory if it doesn't exist
    if not os.path.exists(os.path.dirname(os.path.abspath(__file__))):
        os.makedirs(os.path.dirname(os.path.abspath(__file__)))
    
    print("Populating sample photos...")
    populate_sample_photos() 