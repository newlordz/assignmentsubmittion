#!/usr/bin/env python3
"""
Create a fresh database with proper initialization
"""

import os
import sys
import shutil

def create_fresh_database():
    """Create a fresh database"""
    print("🔄 CREATING FRESH DATABASE")
    print("=" * 50)
    
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
        # Remove existing database files
        db_path = "instance/assignment_system.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"✅ Removed existing database: {db_path}")
        
        # Make sure instance directory exists
        os.makedirs("instance", exist_ok=True)
        print("✅ Created instance directory")
        
        from app import app, db, User, Course, Class, Assignment, Submission, Grade
        
        with app.app_context():
            print("✅ Flask app context loaded")
            print(f"✅ Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Create all tables
            print("🏗️ Creating database tables...")
            db.create_all()
            db.session.commit()
            print("✅ Database tables created successfully!")
            
            # Create a test admin user
            print("👤 Creating test admin user...")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password_hash="admin123",  # In real app, this would be hashed
                role="lecturer",
                name="Admin User"
            )
            db.session.add(admin_user)
            
            # Create a test student
            print("👤 Creating test student...")
            student_user = User(
                username="student",
                email="student@example.com", 
                password_hash="student123",  # In real app, this would be hashed
                role="student",
                name="Test Student"
            )
            db.session.add(student_user)
            
            db.session.commit()
            print("✅ Test users created successfully!")
            
            # Verify the database
            user_count = User.query.count()
            print(f"✅ Database verification: {user_count} users found")
            
            return True
            
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test the created database"""
    print("\n🧪 TESTING DATABASE CONNECTION")
    print("=" * 50)
    
    try:
        from app import app, db, User
        
        with app.app_context():
            print("✅ Flask app context loaded")
            
            # Test database connection
            try:
                user_count = User.query.count()
                print(f"✅ Database connection successful!")
                print(f"✅ Found {user_count} users in database")
                
                # List all users
                users = User.query.all()
                for user in users:
                    print(f"   - {user.username} ({user.role})")
                
                return True
                
            except Exception as e:
                print(f"❌ Database test failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Database test setup failed: {e}")
        return False

def main():
    """Run database creation"""
    print("🔧 FRESH DATABASE CREATION")
    print("=" * 50)
    
    # Step 1: Create fresh database
    if not create_fresh_database():
        print("❌ Database creation failed")
        return
    
    # Step 2: Test database
    if not test_database_connection():
        print("❌ Database test failed")
        return
    
    print("\n🎯 SUMMARY:")
    print("=" * 30)
    print("✅ Fresh database created")
    print("✅ All tables initialized")
    print("✅ Test users created")
    print("✅ Database connection working")
    print()
    print("🚀 READY TO START SERVER:")
    print("The database is now properly initialized and ready to use!")
    print()
    print("📋 TEST CREDENTIALS:")
    print("Admin: username='admin', password='admin123'")
    print("Student: username='student', password='student123'")

if __name__ == "__main__":
    main()
