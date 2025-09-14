#!/usr/bin/env python3
"""
Test demo login functionality
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import check_password_hash

def test_demo_login():
    """Test demo login functionality"""
    
    with app.app_context():
        print("🔍 Testing demo login functionality...")
        
        # Test credentials
        test_credentials = [
            ('student1', 'student123'),
            ('lecturer1', 'lecturer123'),
            ('admin', 'admin123')
        ]
        
        for username, password in test_credentials:
            print(f"\nTesting: {username}")
            
            # Find user
            user = User.query.filter_by(username=username).first()
            
            if user:
                print(f"  ✅ User found: {user.first_name} {user.last_name} ({user.role})")
                print(f"  ✅ Email: {user.email}")
                print(f"  ✅ Active: {user.is_active}")
                
                # Test password
                if check_password_hash(user.password_hash, password):
                    print(f"  ✅ Password correct")
                else:
                    print(f"  ❌ Password incorrect")
            else:
                print(f"  ❌ User not found")
        
        print("\n" + "="*50)
        print("Testing database queries...")
        
        # Test dashboard queries
        try:
            total_students = User.query.filter_by(role='student').count()
            print(f"✅ Students count: {total_students}")
            
            total_lecturers = User.query.filter_by(role='lecturer').count()
            print(f"✅ Lecturers count: {total_lecturers}")
            
            total_admins = User.query.filter_by(role='admin').count()
            print(f"✅ Admins count: {total_admins}")
            
        except Exception as e:
            print(f"❌ Database query error: {e}")
        
        print("\n" + "="*50)
        print("Testing template rendering...")
        
        # Test if templates exist
        template_dir = 'templates'
        required_templates = [
            'login.html',
            'demo_login.html',
            'student_dashboard.html',
            'lecturer_dashboard.html',
            'admin_dashboard.html'
        ]
        
        for template in required_templates:
            template_path = os.path.join(template_dir, template)
            if os.path.exists(template_path):
                print(f"✅ Template exists: {template}")
            else:
                print(f"❌ Template missing: {template}")

def main():
    """Main function"""
    print("🚀 Testing Demo Login Functionality")
    print("=" * 50)
    
    try:
        test_demo_login()
        print("\n🎉 Demo login test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
