#!/usr/bin/env python3
"""
Update email configuration with new Gmail App Password
"""

import os

def update_email_config():
    """Update email configuration with new password"""
    print("📧 UPDATING EMAIL CONFIGURATION")
    print("=" * 50)
    
    # New Gmail App Password
    new_password = "kimqkfbvnxooychr"
    
    print(f"✅ New App Password: {new_password}")
    print(f"   Length: {len(new_password)} characters")
    print(f"   Has spaces: {'Yes' if ' ' in new_password else 'No'}")
    print()
    
    # Set environment variables
    os.environ['MAIL_SERVER'] = 'smtp.gmail.com'
    os.environ['MAIL_PORT'] = '587'
    os.environ['MAIL_USE_TLS'] = 'true'
    os.environ['MAIL_USE_SSL'] = 'false'
    os.environ['MAIL_USERNAME'] = 'enochessel5@gmail.com'
    os.environ['MAIL_PASSWORD'] = new_password
    os.environ['MAIL_DEFAULT_SENDER'] = 'E-Assignment.edu.gh <enochessel5@gmail.com>'
    os.environ['MAIL_SUPPRESS_SEND'] = 'false'
    
    print("✅ Environment variables updated:")
    print(f"   Username: {os.environ['MAIL_USERNAME']}")
    print(f"   Password: {os.environ['MAIL_PASSWORD']}")
    print(f"   Sender: {os.environ['MAIL_DEFAULT_SENDER']}")
    print()
    
    # Update .env file
    print("📝 Updating .env file...")
    
    env_content = f"""# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=enochessel5@gmail.com
MAIL_PASSWORD={new_password}
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
        print("   ✅ .env file updated successfully!")
    except Exception as e:
        print(f"   ❌ Failed to update .env file: {e}")
    
    return new_password

def test_email_connection():
    """Test email connection with new password"""
    print("\n🧪 TESTING EMAIL CONNECTION")
    print("=" * 40)
    
    try:
        from app import app, mail
        with app.app_context():
            print("✅ App context loaded")
            print(f"   Mail server: {app.config['MAIL_SERVER']}")
            print(f"   Mail username: {app.config['MAIL_USERNAME']}")
            print(f"   Mail password: {app.config['MAIL_PASSWORD'][:10]}...")
            print()
            
            print("🔗 Testing SMTP connection...")
            try:
                with mail.connect() as conn:
                    print("   ✅ SMTP connection successful!")
                    print("   ✅ Gmail authentication working!")
                    print("   ✅ Email configuration is ready!")
                    return True
            except Exception as e:
                print(f"   ❌ SMTP connection failed: {e}")
                return False
                
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")
        return False

def main():
    """Run email update and test"""
    # Update configuration
    new_password = update_email_config()
    
    # Test connection
    success = test_email_connection()
    
    print("\n🎯 SUMMARY:")
    print("=" * 30)
    if success:
        print("✅ Email configuration updated successfully!")
        print("✅ Gmail authentication working!")
        print("✅ Ready to send emails!")
        print()
        print("💡 NEXT STEPS:")
        print("1. Restart the server to load new configuration")
        print("2. Test email functionality (registration, notifications)")
        print("3. Check if welcome emails work")
    else:
        print("❌ Email configuration still has issues")
        print("💡 Check if 2-Factor Authentication is enabled")
        print("💡 Verify the App Password is correct")

if __name__ == "__main__":
    main()
