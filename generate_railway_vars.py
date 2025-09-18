#!/usr/bin/env python3
"""
Generate Railway Environment Variables
This script generates the exact environment variables you need for Railway deployment.
"""

import secrets
import os

def generate_secret_key():
    """Generate a secure secret key for Flask."""
    return secrets.token_urlsafe(32)

def generate_railway_variables():
    """Generate all Railway environment variables."""
    print("🚀 Railway Environment Variables Generator")
    print("=" * 50)
    print()
    
    # Generate a secure secret key
    secret_key = generate_secret_key()
    
    print("📋 COPY THESE VARIABLES TO RAILWAY:")
    print("=" * 40)
    print()
    
    # Critical variables
    print("🔐 CRITICAL VARIABLES (Must Set):")
    print("-" * 35)
    print(f"SECRET_KEY={secret_key}")
    print("FLASK_ENV=production")
    print("FLASK_DEBUG=False")
    print()
    
    # Email configuration
    print("📧 EMAIL CONFIGURATION:")
    print("-" * 25)
    print("MAIL_SERVER=smtp.gmail.com")
    print("MAIL_PORT=587")
    print("MAIL_USE_TLS=True")
    print("MAIL_USE_SSL=False")
    print("MAIL_USERNAME=enochessel5@gmail.com")
    print("MAIL_PASSWORD=xgaq ceff cwlh aabb")
    print("MAIL_DEFAULT_SENDER=E-Assignment.edu.gh <enochessel5@gmail.com>")
    print("MAIL_SUPPRESS_SEND=False")
    print()
    
    # Plagiarism detection
    print("🔍 PLAGIARISM DETECTION:")
    print("-" * 25)
    print("PLAGIARISM_CHECK_API_TOKEN=nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4")
    print("USE_PLAGIARISM_CHECK_API=True")
    print("PLAGIARISM_CHECK_API_URL=https://plagiarismcheck.org/api/org/text/check/")
    print()
    
    # Optional variables
    print("⚙️ OPTIONAL VARIABLES:")
    print("-" * 20)
    print("QUETEXT_API_KEY=")
    print("USE_QUETEXT_API=False")
    print("DUPLICHECKER_API_KEY=")
    print("USE_DUPLICHECKER_API=False")
    print("SENDGRID_API_KEY=")
    print("USE_SENDGRID=False")
    print("SENDGRID_FROM_EMAIL=noreply@university.edu")
    print()
    
    print("📝 INSTRUCTIONS:")
    print("=" * 15)
    print("1. Go to your Railway project dashboard")
    print("2. Click on your service")
    print("3. Go to the 'Variables' tab")
    print("4. Click 'New Variable' for each variable above")
    print("5. Copy the Variable Name and Value exactly as shown")
    print("6. Save each variable")
    print("7. Railway will auto-redeploy your app")
    print()
    
    print("✅ PRIORITY ORDER:")
    print("=" * 18)
    print("1. Set SECRET_KEY first (critical for security)")
    print("2. Set email variables (MAIL_USERNAME, MAIL_PASSWORD, etc.)")
    print("3. Set plagiarism detection variables")
    print("4. Set optional variables if needed")
    print()
    
    print("🚨 IMPORTANT NOTES:")
    print("=" * 18)
    print("• Your Gmail App Password: xgaq ceff cwlh aabb")
    print("• Your PlagiarismCheck.org API Token: nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4")
    print("• Make sure there are NO SPACES in the MAIL_PASSWORD")
    print("• The SECRET_KEY above is unique and secure - use it exactly")
    print("• Railway will auto-set DATABASE_URL - don't override it")
    print()
    
    return {
        'SECRET_KEY': secret_key,
        'MAIL_USERNAME': 'enochessel5@gmail.com',
        'MAIL_PASSWORD': 'xgaq ceff cwlh aabb',
        'MAIL_DEFAULT_SENDER': 'E-Assignment.edu.gh <enochessel5@gmail.com>',
        'PLAGIARISM_CHECK_API_TOKEN': 'nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4'
    }

def create_env_file():
    """Create a .env file for local testing."""
    print("📄 Creating .env file for local testing...")
    
    vars = generate_railway_variables()
    
    env_content = f"""# E-Assignment System - Local Development
# Copy these variables to Railway for production deployment

# Application Security
SECRET_KEY={vars['SECRET_KEY']}
FLASK_ENV=development
FLASK_DEBUG=True

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME={vars['MAIL_USERNAME']}
MAIL_PASSWORD={vars['MAIL_PASSWORD']}
MAIL_DEFAULT_SENDER={vars['MAIL_DEFAULT_SENDER']}
MAIL_SUPPRESS_SEND=False

# Plagiarism Detection
PLAGIARISM_CHECK_API_TOKEN={vars['PLAGIARISM_CHECK_API_TOKEN']}
USE_PLAGIARISM_CHECK_API=True
PLAGIARISM_CHECK_API_URL=https://plagiarismcheck.org/api/org/text/check/

# Database (local)
DATABASE_URL=sqlite:///assignment_system.db
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 You can now test locally with: python app.py")
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")

def main():
    """Main function."""
    print("🎓 E-Assignment System - Railway Environment Setup")
    print("=" * 55)
    print()
    
    # Generate variables
    generate_railway_variables()
    
    # Ask if user wants to create .env file
    print("🤔 Do you want to create a .env file for local testing? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['y', 'yes']:
            create_env_file()
        else:
            print("📝 Skipping .env file creation")
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
        return
    
    print()
    print("🎉 Setup complete! Follow the instructions above to configure Railway.")
    print("🚀 After setting variables, your app will be ready for production!")

if __name__ == "__main__":
    main()
