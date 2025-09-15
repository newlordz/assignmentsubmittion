# 🚀 E-Assignment System - Quick Install Guide

## 📋 What You Need
- Python 3.8 or higher installed on your computer
- Internet connection for downloading packages

## 🎯 Super Quick Start (Copy & Paste)

### For Windows Users:
1. **Open Command Prompt or PowerShell**
2. **Navigate to the project folder**
3. **Copy and paste this entire command:**

```bash
python -c "import subprocess, sys; packages = ['flask', 'flask-sqlalchemy', 'flask-login', 'flask-mail', 'werkzeug', 'scikit-learn', 'numpy', 'beautifulsoup4', 'requests', 'python-dotenv']; [subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=True) for pkg in packages]; print('✅ All packages installed!'); subprocess.run([sys.executable, 'app.py'])"
```

### For Mac/Linux Users:
1. **Open Terminal**
2. **Navigate to the project folder**
3. **Copy and paste this entire command:**

```bash
python3 -c "import subprocess, sys; packages = ['flask', 'flask-sqlalchemy', 'flask-login', 'flask-mail', 'werkzeug', 'scikit-learn', 'numpy', 'beautifulsoup4', 'requests', 'python-dotenv']; [subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=True) for pkg in packages]; print('✅ All packages installed!'); subprocess.run([sys.executable, 'app.py'])"
```

## 🖱️ Even Easier - Double Click Method

### Windows:
- **Double-click** `install_and_run.bat`
- Wait for installation to complete
- Application will start automatically

### Mac/Linux:
- **Right-click** `install_and_run.sh` → "Open with Terminal"
- Or run: `./install_and_run.sh`

## 📝 Step-by-Step Method (If Above Doesn't Work)

1. **Install packages one by one:**
   ```bash
   pip install flask
   pip install flask-sqlalchemy
   pip install flask-login
   pip install flask-mail
   pip install werkzeug
   pip install scikit-learn
   pip install numpy
   pip install beautifulsoup4
   pip install requests
   pip install python-dotenv
   ```

2. **Start the application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   - Go to: `http://localhost:5000`

## 🎯 Demo Accounts (Ready to Use!)

**Admin Account:**
- Email: `admin@demo.com`
- Password: `admin123`

**Lecturer Account:**
- Email: `lecturer@demo.com`
- Password: `lecturer123`

**Student Account:**
- Email: `student@demo.com`
- Password: `student123`

## 🔧 Troubleshooting

### "Python not found" error:
- Install Python from: https://python.org
- Make sure to check "Add Python to PATH" during installation

### "pip not found" error:
- Try: `python -m pip install package_name`
- Or: `python3 -m pip install package_name`

### "Permission denied" error:
- Try: `pip install --user package_name`
- Or run as administrator (Windows) / with sudo (Mac/Linux)

### "Module not found" error:
- Make sure you're in the correct folder
- Try: `pip install --upgrade pip`
- Then reinstall packages

## 📧 Email Setup (Optional)

To enable email notifications:

1. **Create `.env` file** in the project folder:
   ```
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_gmail_app_password
   MAIL_DEFAULT_SENDER=your_email@gmail.com
   ```

2. **Gmail App Password Setup:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in `.env` file

## 🎉 That's It!

Once the application starts:
1. Open your browser
2. Go to `http://localhost:5000`
3. Use the demo accounts to test the system
4. Create your own accounts as needed

## 🆘 Need Help?

If you encounter any issues:
1. Check the error messages in the terminal
2. Make sure Python 3.8+ is installed
3. Try the step-by-step method above
4. Check the main README.md for more details

---
**E-Assignment System v2.0** - *Comprehensive Local Plagiarism Detection*
