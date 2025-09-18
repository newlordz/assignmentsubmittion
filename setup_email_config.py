#!/usr/bin/env python3
"""
Setup email configuration for E-Assignment system
"""

import os

def setup_email_config():
    """Setup email configuration"""
    print("📧 EMAIL CONFIGURATION SETUP")
    print("=" * 50)
    
    # Set environment variables
    os.environ['MAIL_SERVER'] = 'smtp.gmail.com'
    os.environ['MAIL_PORT'] = '587'
    os.environ['MAIL_USE_TLS'] = 'true'
    os.environ['MAIL_USE_SSL'] = 'false'
    os.environ['MAIL_USERNAME'] = 'enochessel5@gmail.com'
    os.environ['MAIL_PASSWORD'] = 'xgac cef cwlh aabb'
    os.environ['MAIL_DEFAULT_SENDER'] = 'E-Assignment.edu.gh <enochessel5@gmail.com>'
    os.environ['MAIL_SUPPRESS_SEND'] = 'false'
    
    print("✅ Email configuration set:")
    print(f"   Server: {os.environ['MAIL_SERVER']}")
    print(f"   Port: {os.environ['MAIL_PORT']}")
    print(f"   Username: {os.environ['MAIL_USERNAME']}")
    print(f"   Password: {os.environ['MAIL_PASSWORD'][:10]}...")
    print(f"   Sender: {os.environ['MAIL_DEFAULT_SENDER']}")
    print()
    
    # Test email configuration
    print("🧪 Testing email configuration...")
    
    try:
        from app import app, mail
        with app.app_context():
            # Test mail configuration
            print(f"   Mail server: {app.config['MAIL_SERVER']}")
            print(f"   Mail port: {app.config['MAIL_PORT']}")
            print(f"   Mail username: {app.config['MAIL_USERNAME']}")
            print(f"   Mail password: {app.config['MAIL_PASSWORD'][:10]}...")
            print(f"   Mail sender: {app.config['MAIL_DEFAULT_SENDER']}")
            print()
            
            # Test connection
            print("🔗 Testing SMTP connection...")
            try:
                with mail.connect() as conn:
                    print("   ✅ SMTP connection successful!")
                    print("   ✅ Email configuration is working!")
            except Exception as e:
                print(f"   ❌ SMTP connection failed: {e}")
                print("   💡 Check your Gmail App Password")
                
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")

def create_env_file():
    """Create .env file with email configuration"""
    print("\n📝 Creating .env file...")
    
    env_content = """# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=enochessel5@gmail.com
MAIL_PASSWORD=xgac cef cwlh aabb
MAIL_DEFAULT_SENDER=E-Assignment.edu.gh <enochessel5@gmail.com>
MAIL_SUPPRESS_SEND=false

# SendGrid Configuration (optional)
SENDGRID_API_KEY=
SENDGRID_FROM_EMAIL=noreply@university.edu

# PlagiarismCheck.org API (optional)
PLAGIARISM_CHECK_API_TOKEN=nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4
PLAGIARISM_CHECK_API_URL=https://api.plagiarismcheck.org
USE_PLAGIARISM_CHECK_API=false

# Database
DATABASE_URL=sqlite:///instance/assignment_system.db

# Security
SECRET_KEY=your-secret-key-here
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("   ✅ .env file created successfully!")
        print("   💡 Restart the server to load the new configuration")
    except Exception as e:
        print(f"   ❌ Failed to create .env file: {e}")
        print("   💡 You may need to create it manually")

def main():
    """Run email setup"""
    setup_email_config()
    create_env_file()
    
    print("\n🎯 SUMMARY:")
    print("=" * 30)
    print("✅ Email configuration updated")
    print("✅ Environment variables set")
    print("✅ .env file created")
    print()
    print("💡 NEXT STEPS:")
    print("1. Restart the server to load new configuration")
    print("2. Test email functionality")
    print("3. Check if welcome emails work")

if __name__ == "__main__":
    main()
