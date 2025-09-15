#!/bin/bash

echo ""
echo "========================================"
echo "  E-Assignment System - Quick Install"
echo "========================================"
echo ""
echo "This script will install all required packages and start the application."
echo ""
read -p "Press Enter to continue..."

echo ""
echo "Installing Python packages..."
echo ""

python3 -c "
import subprocess, sys, os, platform
print('🎓 E-Assignment System - Installing...')
packages = ['flask', 'flask-sqlalchemy', 'flask-login', 'flask-mail', 'werkzeug', 'scikit-learn', 'numpy', 'beautifulsoup4', 'requests', 'python-dotenv']
for pkg in packages:
    print(f'Installing {pkg}...')
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=True)
    except:
        print(f'Failed to install {pkg}')
print('✅ Installation complete!')
"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Installation failed. Trying alternative method..."
    echo ""
    pip3 install flask flask-sqlalchemy flask-login flask-mail werkzeug scikit-learn numpy beautifulsoup4 requests python-dotenv
fi

echo ""
echo "🚀 Starting E-Assignment System..."
echo ""
echo "The application will open in your default browser at:"
echo "http://localhost:5000"
echo ""
echo "Demo Accounts:"
echo "Admin: admin@demo.com / admin123"
echo "Lecturer: lecturer@demo.com / lecturer123"
echo "Student: student@demo.com / student123"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

python3 app.py

echo ""
echo "Application stopped."
