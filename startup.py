#!/usr/bin/env python3
"""
Startup script for Railway deployment
This ensures the database is initialized before starting the app
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def initialize_database():
    """Initialize database and demo accounts"""
    try:
        from app import app, db, User
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            print("🚀 Initializing database for Railway...")
            
            # Create all tables
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
            
            # Verify initialization
            total_users = User.query.count()
            students = User.query.filter_by(role='student').count()
            lecturers = User.query.filter_by(role='lecturer').count()
            admins = User.query.filter_by(role='admin').count()
            
            print(f"📊 Database initialized:")
            print(f"  Total users: {total_users}")
            print(f"  Students: {students}")
            print(f"  Lecturers: {lecturers}")
            print(f"  Admins: {admins}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Railway Startup Script")
    print("=" * 50)
    
    success = initialize_database()
    if success:
        print("✅ Database initialization completed!")
        print("🚀 Starting Flask application...")
        
        # Import and run the app
        from app import app
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        print("❌ Failed to initialize database!")
        sys.exit(1)
