#!/usr/bin/env python3
"""
Complete Setup Script for E-Assignment System
Run this script to install all dependencies and set up the application
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("Please install Python 3.8 or higher")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_requirements():
    """Install all required packages"""
    print("\n📦 Installing required packages...")
    
    # Core packages
    packages = [
        "flask",
        "flask-sqlalchemy", 
        "flask-login",
        "flask-mail",
        "werkzeug",
        "scikit-learn",
        "numpy",
        "beautifulsoup4",
        "requests",
        "python-dotenv"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, trying alternative method...")
            if not run_command(f"python -m pip install {package}", f"Installing {package} (alternative)"):
                print(f"❌ Could not install {package}")
                return False
    
    return True

def create_env_file():
    """Create .env file with default settings"""
    print("\n⚙️  Creating environment configuration...")
    
    env_content = """# E-Assignment System Configuration
# Copy this file and update with your actual values

# Database Configuration
DATABASE_URL=sqlite:///assignment_system.db

# Email Configuration (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
MAIL_SUPPRESS_SEND=False

# Application Configuration
SECRET_KEY=your-secret-key-here-change-this
FLASK_ENV=development
FLASK_DEBUG=True

# Plagiarism Detection (Local - No API needed)
USE_PLAGIARISM_CHECK_API=False
PLAGIARISM_CHECK_API_TOKEN=

# Optional: SendGrid Configuration (if you want to use SendGrid instead of Gmail)
SENDGRID_API_KEY=
USE_SENDGRID=False
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("📝 Please edit .env file with your actual email credentials")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_run_script():
    """Create a simple run script"""
    print("\n🚀 Creating run script...")
    
    if platform.system() == "Windows":
        run_script = """@echo off
echo Starting E-Assignment System...
echo.
echo Make sure you have:
echo 1. Updated .env file with your email credentials
echo 2. Internet connection for email functionality
echo.
python app.py
pause
"""
        script_name = "run.bat"
    else:
        run_script = """#!/bin/bash
echo "Starting E-Assignment System..."
echo ""
echo "Make sure you have:"
echo "1. Updated .env file with your email credentials"
echo "2. Internet connection for email functionality"
echo ""
python3 app.py
"""
        script_name = "run.sh"
    
    try:
        with open(script_name, 'w') as f:
            f.write(run_script)
        
        if platform.system() != "Windows":
            os.chmod(script_name, 0o755)
        
        print(f"✅ {script_name} created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create run script: {e}")
        return False

def create_instructions():
    """Create setup instructions"""
    print("\n📋 Creating setup instructions...")
    
    instructions = """# E-Assignment System - Setup Instructions

## 🚀 Quick Start

1. **Run the setup script** (already done if you're reading this):
   ```bash
   python setup.py
   ```

2. **Configure your email** (IMPORTANT):
   - Open the `.env` file
   - Update `MAIL_USERNAME` with your Gmail address
   - Update `MAIL_PASSWORD` with your Gmail App Password
   - Update `MAIL_DEFAULT_SENDER` with your Gmail address

3. **Start the application**:
   - Windows: Double-click `run.bat`
   - Mac/Linux: Run `./run.sh` or `python app.py`

4. **Access the application**:
   - Open your browser
   - Go to `http://localhost:5000`

## 📧 Email Setup (Gmail)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in `.env` file

## 👥 Demo Accounts

The system comes with pre-configured demo accounts:

**Admin Account:**
- Email: admin@demo.com
- Password: admin123

**Lecturer Account:**
- Email: lecturer@demo.com  
- Password: lecturer123

**Student Account:**
- Email: student@demo.com
- Password: student123

## 🎯 Features

- ✅ User registration and authentication
- ✅ Class and course management
- ✅ Assignment creation and submission
- ✅ Comprehensive plagiarism detection (5 methods)
- ✅ Email notifications
- ✅ Grade management
- ✅ Student dashboard

## 🔧 Troubleshooting

**If you get import errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If email doesn't work:**
- Check your Gmail App Password
- Ensure 2FA is enabled
- Verify `.env` file settings

**If database errors occur:**
- Delete `assignment_system.db` file
- Restart the application (it will recreate the database)

## 📞 Support

For issues or questions, check the application logs or contact the developer.

---
**E-Assignment System v2.0**
*Comprehensive Local Plagiarism Detection*
"""
    
    try:
        with open('SETUP_INSTRUCTIONS.md', 'w') as f:
            f.write(instructions)
        print("✅ Setup instructions created")
        return True
    except Exception as e:
        print(f"❌ Failed to create instructions: {e}")
        return False

def main():
    """Main setup function"""
    print("🎓 E-Assignment System Setup")
    print("=" * 50)
    print("This script will install all dependencies and configure the system")
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during package installation")
        return False
    
    # Create configuration files
    if not create_env_file():
        print("\n❌ Setup failed during configuration")
        return False
    
    # Create run script
    if not create_run_script():
        print("\n❌ Setup failed during run script creation")
        return False
    
    # Create instructions
    if not create_instructions():
        print("\n❌ Setup failed during instructions creation")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 50)
    print("📋 Next steps:")
    print("1. Edit .env file with your Gmail credentials")
    print("2. Run the application using run.bat (Windows) or run.sh (Mac/Linux)")
    print("3. Open http://localhost:5000 in your browser")
    print("4. Use demo accounts to test the system")
    print()
    print("📧 Demo Accounts:")
    print("Admin: admin@demo.com / admin123")
    print("Lecturer: lecturer@demo.com / lecturer123") 
    print("Student: student@demo.com / student123")
    print()
    print("📖 Read SETUP_INSTRUCTIONS.md for detailed information")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
