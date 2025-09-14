#!/usr/bin/env python3
"""
Create demo accounts for testing the system
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def create_demo_accounts():
    """Create demo accounts for testing"""
    
    with app.app_context():
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
        
        print(f"\n📊 Summary:")
        print(f"  Created: {created_count} accounts")
        print(f"  Updated: {updated_count} accounts")
        print(f"  Total: {len(demo_accounts)} demo accounts")
        
        return True

def verify_demo_accounts():
    """Verify that demo accounts exist and can be accessed"""
    
    with app.app_context():
        print("\n🔍 Verifying demo accounts...")
        
        demo_usernames = [
            'student1', 'student2', 'student3', 'student4', 'student5',
            'lecturer1', 'lecturer2', 'lecturer3', 'admin'
        ]
        
        for username in demo_usernames:
            user = User.query.filter_by(username=username).first()
            if user:
                print(f"  ✅ {username}: {user.role} - {user.first_name} {user.last_name}")
            else:
                print(f"  ❌ {username}: NOT FOUND")

def main():
    """Main function"""
    print("🚀 Creating Demo Accounts")
    print("=" * 50)
    
    try:
        # Create demo accounts
        success = create_demo_accounts()
        
        if success:
            # Verify accounts
            verify_demo_accounts()
            print("\n🎉 Demo accounts setup completed successfully!")
            print("You can now use the demo login page to test the system.")
        else:
            print("\n💥 Failed to create demo accounts!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()