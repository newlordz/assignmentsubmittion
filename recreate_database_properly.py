#!/usr/bin/env python3
"""
Properly recreate the database with all tables and data
"""

import os
import sys
import shutil

def backup_existing_database():
    """Backup the existing database"""
    print("💾 BACKING UP EXISTING DATABASE")
    print("=" * 40)
    
    db_path = "instance/assignment_system.db"
    backup_path = "instance/assignment_system.db.backup"
    
    if os.path.exists(db_path):
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
        return True
    else:
        print("ℹ️ No existing database to backup")
        return True

def recreate_database():
    """Recreate the database with proper initialization"""
    print("\n🔄 RECREATING DATABASE")
    print("=" * 40)
    
    # Set environment variables
    os.environ['MAIL_SERVER'] = 'smtp.gmail.com'
    os.environ['MAIL_PORT'] = '587'
    os.environ['MAIL_USE_TLS'] = 'true'
    os.environ['MAIL_USE_SSL'] = 'false'
    os.environ['MAIL_USERNAME'] = 'enochessel5@gmail.com'
    os.environ['MAIL_PASSWORD'] = 'kimqkfbvnxooychr'
    os.environ['MAIL_DEFAULT_SENDER'] = 'E-Assignment.edu.gh <enochessel5@gmail.com>'
    os.environ['MAIL_SUPPRESS_SEND'] = 'false'
    
    try:
        from app import app, db
        
        with app.app_context():
            print("✅ Flask app context loaded")
            
            # Drop all tables
            print("🗑️ Dropping all existing tables...")
            db.drop_all()
            
            # Create all tables
            print("🏗️ Creating all tables...")
            db.create_all()
            
            # Commit the changes
            db.session.commit()
            print("✅ Database tables created successfully!")
            
            return True
            
    except Exception as e:
        print(f"❌ Database recreation failed: {e}")
        return False

def restore_data_from_backup():
    """Restore data from backup if available"""
    print("\n📥 RESTORING DATA FROM BACKUP")
    print("=" * 40)
    
    backup_path = "instance/assignment_system.db.backup"
    db_path = "instance/assignment_system.db"
    
    if os.path.exists(backup_path):
        try:
            # Copy backup to main database
            shutil.copy2(backup_path, db_path)
            print("✅ Data restored from backup!")
            return True
        except Exception as e:
            print(f"❌ Failed to restore from backup: {e}")
            return False
    else:
        print("ℹ️ No backup available to restore")
        return True

def test_database():
    """Test the recreated database"""
    print("\n🧪 TESTING RECREATED DATABASE")
    print("=" * 40)
    
    try:
        from app import app, db, User
        
        with app.app_context():
            print("✅ Flask app context loaded")
            
            # Test database connection
            try:
                # Try to query the User table
                user_count = User.query.count()
                print(f"✅ Database connection successful!")
                print(f"✅ Found {user_count} users in database")
                
                # Test creating a test user
                test_user = User(
                    username="test_user",
                    email="test@example.com",
                    password_hash="test_hash",
                    role="student"
                )
                db.session.add(test_user)
                db.session.commit()
                print("✅ Test user created successfully!")
                
                # Clean up test user
                db.session.delete(test_user)
                db.session.commit()
                print("✅ Test user cleaned up")
                
                return True
                
            except Exception as e:
                print(f"❌ Database test failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Database test setup failed: {e}")
        return False

def main():
    """Run database recreation"""
    print("🔧 DATABASE RECREATION")
    print("=" * 50)
    
    # Step 1: Backup existing database
    if not backup_existing_database():
        print("❌ Backup failed")
        return
    
    # Step 2: Recreate database
    if not recreate_database():
        print("❌ Database recreation failed")
        return
    
    # Step 3: Restore data from backup
    if not restore_data_from_backup():
        print("❌ Data restoration failed")
        return
    
    # Step 4: Test database
    if not test_database():
        print("❌ Database test failed")
        return
    
    print("\n🎯 SUMMARY:")
    print("=" * 30)
    print("✅ Database backed up")
    print("✅ Database recreated")
    print("✅ Data restored")
    print("✅ Database tested")
    print()
    print("🚀 READY TO START SERVER:")
    print("The database is now properly initialized and ready to use!")

if __name__ == "__main__":
    main()
