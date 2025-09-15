#!/usr/bin/env python3
"""
Script to help set up Gmail credentials for email notifications
"""

import os
import getpass

def setup_gmail_credentials():
    """Interactive setup for Gmail credentials"""
    print("🔧 Gmail Email Setup")
    print("=" * 50)
    print()
    print("This script will help you set up Gmail credentials for email notifications.")
    print("You'll need:")
    print("1. A Gmail account with 2-Factor Authentication enabled")
    print("2. An App Password (not your regular password)")
    print()
    
    # Get Gmail address
    gmail_address = input("Enter your Gmail address: ").strip()
    if not gmail_address or '@gmail.com' not in gmail_address:
        print("❌ Please enter a valid Gmail address")
        return False
    
    # Get App Password
    print()
    print("📱 App Password Setup:")
    print("1. Go to https://myaccount.google.com/security")
    print("2. Click '2-Step Verification' (enable if not already)")
    print("3. Click 'App passwords'")
    print("4. Select 'Mail' and 'Other (Custom name)'")
    print("5. Enter name: 'Assignment System'")
    print("6. Copy the 16-character password")
    print()
    
    app_password = getpass.getpass("Enter your 16-character App Password: ").strip()
    if len(app_password) != 16 or ' ' in app_password:
        print("❌ App Password should be 16 characters without spaces")
        return False
    
    # Create .env file
    env_content = f"""# Gmail SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME={gmail_address}
MAIL_PASSWORD={app_password}
MAIL_DEFAULT_SENDER={gmail_address}
MAIL_SUPPRESS_SEND=false

# Application Configuration
BASE_URL=https://your-app.railway.app
SECRET_KEY=your-secret-key-here
"""
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print()
    print("✅ Gmail credentials configured!")
    print("📁 Created .env file with your credentials")
    print()
    print("🚀 Next steps:")
    print("1. For local testing: Run 'python app.py'")
    print("2. For Railway deployment: Set these as environment variables in Railway dashboard")
    print("3. Test email sending with: python test_email_comprehensive.py")
    print()
    
    return True

def test_email_with_new_credentials():
    """Test email sending with the new credentials"""
    print("🧪 Testing Email with New Credentials")
    print("=" * 50)
    
    # Load environment variables from .env file
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    # Test email sending
    try:
        from app import app, send_email, User
        
        with app.app_context():
            user = User.query.filter_by(role='student').first()
            if not user:
                print("❌ No test user found")
                return False
            
            test_email = input("Enter your email to test: ").strip()
            if not test_email:
                print("❌ No email provided")
                return False
            
            # Temporarily change user email for testing
            original_email = user.email
            user.email = test_email
            
            result = send_email(
                to_email=test_email,
                subject="Test Email from Assignment System",
                template='welcome.html',
                user=user
            )
            
            # Restore original email
            user.email = original_email
            
            if result:
                print("✅ Email sent successfully!")
                print(f"📬 Check your inbox at {test_email}")
                return True
            else:
                print("❌ Email sending failed")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("📧 Gmail Email Setup & Test")
    print("=" * 60)
    print()
    
    # Setup credentials
    if setup_gmail_credentials():
        print()
        test_now = input("Test email sending now? (y/n): ").strip().lower()
        if test_now == 'y':
            test_email_with_new_credentials()
    
    print()
    print("🎉 Setup complete!")
