# E-Assignment Submission System

A comprehensive web-based assignment management platform built with Python Flask backend and modern HTML/CSS frontend. This system streamlines academic workflow for students, lecturers, and administrators with AI-powered plagiarism detection and automated notifications.

## 🚀 Features

### For Students
- **Easy Assignment Submission**: User-friendly interface for uploading assignments
- **AI-Powered Plagiarism Detection**: Built-in originality checking before submission
- **Automated Deadline Reminders**: Timely alerts to avoid missing deadlines
- **Real-time Grade Tracking**: Access grades and feedback instantly
- **Submission History**: View past assignments and feedback for self-review

### For Lecturers
- **Assignment Management**: Create and manage assignments with deadlines
- **Automated Deadline Enforcement**: System blocks late submissions automatically
- **Built-in Grading System**: Grade submissions directly within the platform
- **Plagiarism Reports**: AI-generated originality results for academic integrity
- **Student Progress Tracking**: Monitor submission status and performance

### For Administrators
- **User Account Management**: Create and manage student/lecturer accounts
- **System Configuration**: Set rules for deadlines, notifications, and grading
- **Performance Monitoring**: View system logs and detect issues
- **Analytics & Reporting**: Generate data on submission rates and performance trends
- **Data Security**: Maintain backup and privacy of academic content

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **AI/ML**: scikit-learn, NLTK for plagiarism detection
- **File Processing**: Pillow, python-magic
- **Authentication**: Flask-Login with password hashing

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assignment-submission-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python app.py
   ```
   This will create the SQLite database and an admin user.

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

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
