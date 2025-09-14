#!/usr/bin/env python3
"""
Database Migration Script
Adds the missing 'content' column to the submission table
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add the content column to the submission table"""
    
    # Database path
    db_path = os.path.join('instance', 'assignment_system.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if content column already exists
        cursor.execute("PRAGMA table_info(submission)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'content' in columns:
            print("Content column already exists in submission table")
            conn.close()
            return True
        
        print("Adding content column to submission table...")
        
        # Add the content column
        cursor.execute("""
            ALTER TABLE submission 
            ADD COLUMN content TEXT
        """)
        
        # Commit changes
        conn.commit()
        print("✅ Successfully added content column to submission table")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(submission)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'content' in columns:
            print("✅ Verification successful: content column exists")
        else:
            print("❌ Verification failed: content column not found")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    print(f"Timestamp: {datetime.now()}")
    print("-" * 50)
    
    success = migrate_database()
    
    print("-" * 50)
    if success:
        print("🎉 Database migration completed successfully!")
        print("You can now run your Flask application without errors.")
    else:
        print("💥 Database migration failed!")
        print("Please check the error messages above.")
