#!/usr/bin/env python3
"""
Fix database connection issues
"""

import os
import sqlite3
import sys

def check_database_file():
    """Check if database file is accessible"""
    print("🔍 CHECKING DATABASE FILE")
    print("=" * 40)
    
    db_path = "instance/assignment_system.db"
    
    print(f"Database path: {db_path}")
    print(f"File exists: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        file_size = os.path.getsize(db_path)
        print(f"File size: {file_size} bytes")
        
        # Check if file is readable
        try:
            with open(db_path, 'rb') as f:
                f.read(1)
            print("✅ File is readable")
        except Exception as e:
            print(f"❌ File is not readable: {e}")
            return False
    
    return True

def test_sqlite_connection():
    """Test direct SQLite connection"""
    print("\n🔗 TESTING SQLITE CONNECTION")
    print("=" * 40)
    
    db_path = "instance/assignment_system.db"
    
    try:
        # Test direct SQLite connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test a simple query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"✅ SQLite connection successful!")
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ SQLite connection failed: {e}")
        return False

def fix_database_permissions():
    """Fix database file permissions"""
    print("\n🔧 FIXING DATABASE PERMISSIONS")
    print("=" * 40)
    
    db_path = "instance/assignment_system.db"
    
    try:
        # Make sure the instance directory exists
        os.makedirs("instance", exist_ok=True)
        
        # Check current permissions
        if os.path.exists(db_path):
            stat_info = os.stat(db_path)
            print(f"Current permissions: {oct(stat_info.st_mode)}")
            
            # Try to make it writable
            os.chmod(db_path, 0o666)
            print("✅ Set database file permissions to 666")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix permissions: {e}")
        return False

def recreate_database():
    """Recreate database if needed"""
    print("\n🔄 RECREATING DATABASE")
    print("=" * 40)
    
    db_path = "instance/assignment_system.db"
    
    try:
        # Backup existing database
        if os.path.exists(db_path):
            backup_path = f"{db_path}.backup"
            os.rename(db_path, backup_path)
            print(f"✅ Backed up existing database to {backup_path}")
        
        # Create new database
        conn = sqlite3.connect(db_path)
        conn.close()
        print("✅ Created new database file")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to recreate database: {e}")
        return False

def test_flask_database():
    """Test Flask database connection"""
    print("\n🧪 TESTING FLASK DATABASE")
    print("=" * 40)
    
    try:
        # Set environment variables
        os.environ['MAIL_SERVER'] = 'smtp.gmail.com'
        os.environ['MAIL_PORT'] = '587'
        os.environ['MAIL_USE_TLS'] = 'true'
        os.environ['MAIL_USE_SSL'] = 'false'
        os.environ['MAIL_USERNAME'] = 'enochessel5@gmail.com'
        os.environ['MAIL_PASSWORD'] = 'kimqkfbvnxooychr'
        os.environ['MAIL_DEFAULT_SENDER'] = 'E-Assignment.edu.gh <enochessel5@gmail.com>'
        os.environ['MAIL_SUPPRESS_SEND'] = 'false'
        
        from app import app, db
        
        with app.app_context():
            print("✅ Flask app context loaded")
            
            # Test database connection
            try:
                db.engine.execute("SELECT 1")
                print("✅ Database connection successful!")
                return True
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Flask database test failed: {e}")
        return False

def main():
    """Run database fix"""
    print("🔧 DATABASE CONNECTION FIX")
    print("=" * 50)
    
    # Step 1: Check database file
    if not check_database_file():
        print("❌ Database file check failed")
        return
    
    # Step 2: Test SQLite connection
    if not test_sqlite_connection():
        print("❌ SQLite connection failed")
        return
    
    # Step 3: Fix permissions
    if not fix_database_permissions():
        print("❌ Permission fix failed")
        return
    
    # Step 4: Test Flask database
    if not test_flask_database():
        print("❌ Flask database test failed")
        print("💡 Trying to recreate database...")
        
        if recreate_database():
            print("✅ Database recreated, testing again...")
            if test_flask_database():
                print("✅ Database is now working!")
            else:
                print("❌ Database still not working")
        else:
            print("❌ Failed to recreate database")
        return
    
    print("\n🎯 SUMMARY:")
    print("=" * 30)
    print("✅ Database file accessible")
    print("✅ SQLite connection working")
    print("✅ Permissions fixed")
    print("✅ Flask database working")
    print()
    print("🚀 READY TO START SERVER:")
    print("The database connection issue has been resolved!")

if __name__ == "__main__":
    main()
