#!/usr/bin/env python3
"""
Test if the database fix worked
"""

import os
import sys

def test_database_connection():
    """Test database connection with the fixed URI"""
    print("🧪 TESTING DATABASE CONNECTION")
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
        from app import app, db, User
        
        with app.app_context():
            print("✅ Flask app context loaded")
            print(f"✅ Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
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
    """Run database test"""
    success = test_database_connection()
    
    print("\n🎯 SUMMARY:")
    print("=" * 30)
    if success:
        print("✅ DATABASE CONNECTION FIXED!")
        print("✅ Database URI corrected")
        print("✅ Database operations working")
        print()
        print("🚀 READY TO START SERVER:")
        print("The database connection issue has been resolved!")
    else:
        print("❌ Database still has issues")
        print("💡 May need further investigation")

if __name__ == "__main__":
    main()
