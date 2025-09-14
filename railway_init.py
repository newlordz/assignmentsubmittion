#!/usr/bin/env python3
"""
Railway database initialization script
Run this manually on Railway if demo accounts are missing
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Initialize database for Railway"""
    print("🚀 Railway Database Initialization")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print()
    
    try:
        from app import app, db, User
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            print("🔧 Creating database tables...")
            db.create_all()
            print("✅ Database tables created")
            
            # Create admin user if not exists
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@university.edu',
                    password_hash=generate_password_hash('admin123'),
                    role='admin',
                    first_name='System',
                    last_name='Administrator'
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created")
            else:
                print("✅ Admin user already exists")
            
            # Create demo accounts if they don't exist
            demo_user = User.query.filter_by(username='student1').first()
            if not demo_user:
                print("🚀 Creating demo accounts...")
                
                # Demo accounts data
                demo_accounts = [
                    # Students
                    {'username': 'student1', 'email': 'student1@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'John', 'last_name': 'Doe'},
                    {'username': 'student2', 'email': 'student2@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'Jane', 'last_name': 'Smith'},
                    {'username': 'student3', 'email': 'student3@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'Mike', 'last_name': 'Johnson'},
                    {'username': 'student4', 'email': 'student4@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'Sarah', 'last_name': 'Wilson'},
                    {'username': 'student5', 'email': 'student5@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'David', 'last_name': 'Brown'},
                    
                    # Lecturers
                    {'username': 'lecturer1', 'email': 'lecturer1@demo.com', 'password': 'lecturer123', 'role': 'lecturer', 'first_name': 'Professor', 'last_name': 'Jones'},
                    {'username': 'lecturer2', 'email': 'lecturer2@demo.com', 'password': 'lecturer123', 'role': 'lecturer', 'first_name': 'Dr. Maria', 'last_name': 'Garcia'},
                    {'username': 'lecturer3', 'email': 'lecturer3@demo.com', 'password': 'lecturer123', 'role': 'lecturer', 'first_name': 'Professor', 'last_name': 'Lee'},
                ]
                
                for account_data in demo_accounts:
                    new_user = User(
                        username=account_data['username'],
                        email=account_data['email'],
                        password_hash=generate_password_hash(account_data['password']),
                        role=account_data['role'],
                        first_name=account_data['first_name'],
                        last_name=account_data['last_name'],
                        is_active=True
                    )
                    db.session.add(new_user)
                
                db.session.commit()
                print("✅ Demo accounts created successfully!")
            else:
                print("✅ Demo accounts already exist")
            
            # Verify initialization
            total_users = User.query.count()
            students = User.query.filter_by(role='student').count()
            lecturers = User.query.filter_by(role='lecturer').count()
            admins = User.query.filter_by(role='admin').count()
            
            print(f"\n📊 Database Status:")
            print(f"  Total users: {total_users}")
            print(f"  Students: {students}")
            print(f"  Lecturers: {lecturers}")
            print(f"  Admins: {admins}")
            
            print(f"\n🎉 Database initialization completed successfully!")
            print("Demo accounts are now available for testing.")
            
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()
