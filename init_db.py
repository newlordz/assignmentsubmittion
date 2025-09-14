#!/usr/bin/env python3
"""
Database initialization script for Railway deployment
This script creates demo accounts and initializes the database
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with demo accounts"""
    
    with app.app_context():
        print("🚀 Initializing database for Railway deployment...")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
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
            
            # Admin
            {'username': 'admin', 'email': 'admin@demo.com', 'password': 'admin123', 'role': 'admin', 'first_name': 'System', 'last_name': 'Administrator'},
        ]
        
        created_count = 0
        updated_count = 0
        
        for account_data in demo_accounts:
            # Check if user already exists
            existing_user = User.query.filter_by(username=account_data['username']).first()
            
            if existing_user:
                # Update existing user
                existing_user.email = account_data['email']
                existing_user.password_hash = generate_password_hash(account_data['password'])
                existing_user.role = account_data['role']
                existing_user.first_name = account_data['first_name']
                existing_user.last_name = account_data['last_name']
                existing_user.is_active = True
                updated_count += 1
                print(f"✅ Updated: {account_data['username']} ({account_data['role']})")
            else:
                # Create new user
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
                created_count += 1
                print(f"🆕 Created: {account_data['username']} ({account_data['role']})")
        
        # Commit all changes
        db.session.commit()
        
        print(f"\n📊 Database Initialization Summary:")
        print(f"  Created: {created_count} accounts")
        print(f"  Updated: {updated_count} accounts")
        print(f"  Total: {len(demo_accounts)} demo accounts")
        
        # Verify accounts
        print(f"\n🔍 Verifying accounts...")
        total_users = User.query.count()
        students = User.query.filter_by(role='student').count()
        lecturers = User.query.filter_by(role='lecturer').count()
        admins = User.query.filter_by(role='admin').count()
        
        print(f"  Total users: {total_users}")
        print(f"  Students: {students}")
        print(f"  Lecturers: {lecturers}")
        print(f"  Admins: {admins}")
        
        print(f"\n🎉 Database initialization completed successfully!")
        return True

def main():
    """Main function"""
    print("🚀 Railway Database Initialization")
    print("=" * 50)
    
    try:
        success = init_database()
        if success:
            print("\n✅ Database is ready for Railway deployment!")
        else:
            print("\n❌ Database initialization failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()
