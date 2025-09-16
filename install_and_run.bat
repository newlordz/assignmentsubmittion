@echo off
echo.
echo ========================================
echo   E-Assignment System - Quick Install
echo ========================================
echo.
echo This script will install all required packages and start the application.
echo.
pause

echo.
echo Installing Python packages...
echo.

python -c "
import subprocess, sys, os, platform
print('🎓 E-Assignment System - Installing...')
packages = ['flask', 'flask-sqlalchemy', 'flask-login', 'flask-mail', 'werkzeug', 'scikit-learn', 'numpy', 'beautifulsoup4', 'requests', 'python-dotenv']
for pkg in packages:
    print(f'Installing {pkg}...')
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=True)
    except:
        print(f'Failed to install {pkg}')
print('✅ Python packages installed!')
"

echo.
echo Checking for Node.js (required for advanced plagiarism detection)...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Node.js not found. Advanced plagiarism detection will not be available.
    echo You can install Node.js from: https://nodejs.org/
    echo.
) else (
    echo ✅ Node.js found - Advanced plagiarism detection available
    echo.
    echo Setting up Dolos plagiarism detection...
    python setup_dolos.py
)

if %errorlevel% neq 0 (
    echo.
    echo ❌ Installation failed. Trying alternative method...
    echo.
    pip install flask flask-sqlalchemy flask-login flask-mail werkzeug scikit-learn numpy beautifulsoup4 requests python-dotenv
)

echo.
echo 🚀 Starting E-Assignment System...
echo.
echo The application will open in your default browser at:
echo http://localhost:5000
echo.
echo Demo Accounts:
echo Admin: admin@demo.com / admin123
echo Lecturer: lecturer@demo.com / lecturer123
echo Student: student@demo.com / student123
echo.
echo Press Ctrl+C to stop the application
echo.

python app.py

echo.
echo Application stopped.
pause
