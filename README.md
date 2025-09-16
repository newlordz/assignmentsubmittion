# E-Assignment Submission System

A comprehensive web-based assignment management platform built with Python Flask backend and modern HTML/CSS frontend. This system streamlines academic workflow for students, lecturers, and administrators with AI-powered plagiarism detection and automated notifications.

## 🚀 Features

### For Students
- **Easy Assignment Submission**: User-friendly interface for uploading assignments
- **Advanced Plagiarism Detection**: Dual-mode detection using Dolos (for code) and local algorithms (for text)
- **Automated Deadline Reminders**: Timely alerts to avoid missing deadlines
- **Real-time Grade Tracking**: Access grades and feedback instantly
- **Submission History**: View past assignments and feedback for self-review

### For Lecturers
- **Assignment Management**: Create and manage assignments with deadlines
- **Automated Deadline Enforcement**: System blocks late submissions automatically
- **Built-in Grading System**: Grade submissions directly within the platform
- **Advanced Plagiarism Reports**: Multi-method plagiarism detection with detailed analysis
- **Student Progress Tracking**: Monitor submission status and performance

### For Administrators
- **User Account Management**: Create and manage student/lecturer accounts
- **System Configuration**: Set rules for deadlines, notifications, and grading
- **Performance Monitoring**: View system logs and detect issues
- **Analytics & Reporting**: Generate data on submission rates and performance trends
- **Data Security**: Maintain backup and privacy of academic content

### 🔍 Advanced Plagiarism Detection
- **Dolos Integration**: State-of-the-art code plagiarism detection for programming assignments
- **Multi-Language Support**: Detects plagiarism in Python, JavaScript, Java, C/C++, and more
- **Local Fallback**: Comprehensive text-based plagiarism detection using 5 different algorithms
- **Detailed Reports**: Provides similarity scores, matched fragments, and analysis details
- **Automatic Language Detection**: Intelligently detects programming language and applies appropriate analysis

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Plagiarism Detection**: 
  - **Dolos**: Advanced code plagiarism detection (Node.js/TypeScript)
  - **Local Algorithms**: TF-IDF, Semantic Similarity, Content Fingerprinting, Phrase Matching, Structure Analysis
- **AI/ML**: scikit-learn, NLTK for text analysis
- **File Processing**: Pillow, python-magic
- **Authentication**: Flask-Login with password hashing

## 📦 Installation

### 🚀 Quick Start (One-Click Installation)

**For Windows (Command Prompt/PowerShell):**
```bash
python -c "
import subprocess, sys, os, platform
print('🎓 E-Assignment System - Installing...')
packages = ['flask', 'flask-sqlalchemy', 'flask-login', 'flask-mail', 'werkzeug', 'scikit-learn', 'numpy', 'beautifulsoup4', 'requests', 'python-dotenv']
for pkg in packages:
    print(f'Installing {pkg}...')
    subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=True)
print('✅ All packages installed!')
print('🚀 Starting application...')
subprocess.run([sys.executable, 'app.py'])
"
```

**For Mac/Linux (Terminal):**
```bash
python3 -c "
import subprocess, sys, os, platform
print('🎓 E-Assignment System - Installing...')
packages = ['flask', 'flask-sqlalchemy', 'flask-login', 'flask-mail', 'werkzeug', 'scikit-learn', 'numpy', 'beautifulsoup4', 'requests', 'python-dotenv']
for pkg in packages:
    print(f'Installing {pkg}...')
    subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=True)
print('✅ All packages installed!')
print('🚀 Starting application...')
subprocess.run([sys.executable, 'app.py'])
"
```

### 📋 Manual Installation

**Prerequisites:**
- Python 3.8 or higher
- pip (Python package installer)

**Step-by-Step Setup:**

1. **Install Python packages**
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-mail werkzeug scikit-learn numpy beautifulsoup4 requests python-dotenv
   ```

2. **Run the application**
   ```bash
   python app.py
   ```

3. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### 🎯 Demo Accounts

The system comes with pre-configured demo accounts:

**Admin Account:**
- Email: `admin@demo.com`
- Password: `admin123`

**Lecturer Account:**
- Email: `lecturer@demo.com`
- Password: `lecturer123`

**Student Account:**
- Email: `student@demo.com`
- Password: `student123`

### 🔍 Advanced Plagiarism Detection Setup (Optional)

For advanced code plagiarism detection using Dolos:

1. **Install Node.js** (if not already installed):
   - Download from: https://nodejs.org/
   - Install the LTS version

2. **Run Dolos setup**:
   ```bash
   python setup_dolos.py
   ```

3. **What you get:**
   - ✅ Advanced code plagiarism detection for programming assignments
   - ✅ Support for 20+ programming languages
   - ✅ Detailed similarity analysis and reports
   - ✅ Automatic fallback to local detection if Dolos unavailable

### 📧 Email Configuration (Optional)

To enable email notifications:

1. **Create `.env` file** in the project root:
   ```env
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_gmail_app_password
   MAIL_DEFAULT_SENDER=your_email@gmail.com
   ```

2. **Gmail Setup:**
   - Enable 2-Factor Authentication
   - Generate App Password: Google Account → Security → 2-Step Verification → App passwords
   - Use the App Password in `.env` file

### 🔧 Troubleshooting

**If you get import errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If database errors occur:**
- Delete `assignment_system.db` file
- Restart the application (it will recreate the database)

## 🔐 Default Admin Account

- **Username**: admin
- **Password**: admin123

**Important**: Change the admin password immediately after first login!

## 📁 Project Structure

```
assignment-submission-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── script.js     # JavaScript functionality
│   └── uploads/          # File upload directory
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── student_dashboard.html
│   ├── lecturer_dashboard.html
│   ├── admin_dashboard.html
│   ├── create_assignment.html
│   ├── submit_assignment.html
│   └── grade_submission.html
└── assignment_system.db  # SQLite database (created on first run)
```

## 🎨 Design Features

- **Modern UI/UX**: Clean, professional design with smooth animations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Accessibility**: WCAG compliant with keyboard navigation support
- **Dark/Light Theme**: Automatic theme detection with smooth transitions
- **Interactive Elements**: Hover effects, loading states, and micro-interactions

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///assignment_system.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### Database Configuration
The system uses SQLite by default for development. For production, update the `SQLALCHEMY_DATABASE_URI` in `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
```

## 🚀 Deployment

### Heroku Deployment
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Add PostgreSQL addon:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

### Docker Deployment
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```

2. Build and run:
   ```bash
   docker build -t assignment-system .
   docker run -p 5000:5000 assignment-system
   ```

## 🔒 Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **File Validation**: Validates file types and sizes before upload
- **SQL Injection Protection**: Uses SQLAlchemy ORM
- **XSS Protection**: Template auto-escaping enabled
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Role-based Access Control**: Different permissions for different user types

## 📊 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Assignments
- `GET /assignment/create` - Create assignment form
- `POST /assignment/create` - Create new assignment
- `GET /assignment/submit/<id>` - Submit assignment form
- `POST /assignment/submit/<id>` - Submit assignment

### Grading
- `GET /submission/grade/<id>` - Grade submission form
- `POST /submission/grade/<id>` - Grade submission

### API
- `GET /api/plagiarism-check/<id>` - Check plagiarism score

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@assignment-system.com or create an issue in the repository.

## 🔮 Future Enhancements

- [ ] Real-time notifications with WebSockets
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Integration with Learning Management Systems
- [ ] Multi-language support
- [ ] Advanced plagiarism detection with external APIs
- [ ] Video assignment support
- [ ] Peer review functionality

## 📞 Contact

- **Developer**: Your Name
- **Email**: your.email@example.com
- **Project Link**: [https://github.com/yourusername/assignment-submission-system](https://github.com/yourusername/assignment-submission-system)

---

Made with ❤️ for educational institutions worldwide.
