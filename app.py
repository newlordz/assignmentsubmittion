from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import sendgrid
from sendgrid.helpers.mail import Mail as SendGridMail, Email, To, Content
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
import hashlib
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time
import shutil
import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler

# Import Dolos integration
try:
    from dolos_integration import DolosIntegration
    DOLOS_AVAILABLE = True
except ImportError:
    DOLOS_AVAILABLE = False
    print("Dolos integration not available - using local plagiarism detection only")

# Load environment variables from .env file
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///assignment_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your_email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your_app_password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'E-Assignment.edu.gh <enochessel5@gmail.com>')
app.config['MAIL_SUPPRESS_SEND'] = os.environ.get('MAIL_SUPPRESS_SEND', 'false').lower() in ['true', 'on', '1']

# SendGrid Configuration
app.config['SENDGRID_API_KEY'] = os.environ.get('SENDGRID_API_KEY', '')
app.config['SENDGRID_FROM_EMAIL'] = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@university.edu')
app.config['USE_SENDGRID'] = os.environ.get('USE_SENDGRID', 'false').lower() in ['true', 'on', '1']

# PlagiarismCheck.org API Configuration
app.config['PLAGIARISM_CHECK_API_TOKEN'] = os.environ.get('PLAGIARISM_CHECK_API_TOKEN', '')
app.config['PLAGIARISM_CHECK_API_URL'] = 'https://plagiarismcheck.org/api/org/text/check/'
app.config['USE_PLAGIARISM_CHECK_API'] = os.environ.get('USE_PLAGIARISM_CHECK_API', 'false').lower() in ['true', 'on', '1']

# Quetext API Configuration
app.config['QUETEXT_API_KEY'] = os.environ.get('QUETEXT_API_KEY', '')
app.config['QUETEXT_API_URL'] = 'https://api.quetext.com/v1/plagiarism'
app.config['USE_QUETEXT_API'] = os.environ.get('USE_QUETEXT_API', 'false').lower() in ['true', 'on', '1']

# DupliChecker API Configuration
app.config['DUPLICHECKER_API_KEY'] = os.environ.get('DUPLICHECKER_API_KEY', '')
app.config['DUPLICHECKER_API_URL'] = 'https://www.duplichecker.com/api/plagiarism-check'
app.config['USE_DUPLICHECKER_API'] = os.environ.get('USE_DUPLICHECKER_API', 'false').lower() in ['true', 'on', '1']

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Dolos integration
dolos_integration = None
if DOLOS_AVAILABLE:
    try:
        dolos_integration = DolosIntegration()
        if dolos_integration.is_available():
            print("✅ Dolos integration available - advanced plagiarism detection enabled")
        else:
            print("⚠️ Dolos integration not properly configured - using local detection only")
            dolos_integration = None
    except Exception as e:
        print(f"⚠️ Error initializing Dolos integration: {e}")
        dolos_integration = None

# Initialize scheduler for automated tasks
scheduler = BackgroundScheduler()
scheduler.start()

def initialize_database():
    """Initialize database with demo accounts"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            
            # Create admin user if not exists
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@university.edu',
                    password_hash=generate_password_hash('admin123'),
                    role='admin',
                    first_name='System',
                    last_name='Administrator'
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created")
            
            # Create demo accounts if they don't exist
            demo_user = User.query.filter_by(username='student1').first()
            if not demo_user:
                print("🚀 Creating demo accounts...")
                
                # Demo accounts data
                demo_accounts = [
                    # Students
                    {'username': 'student1', 'email': 'student1@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'John', 'last_name': 'Doe'},
                    {'username': 'student2', 'email': 'student2@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'Jane', 'last_name': 'Smith'},
                    {'username': 'student3', 'email': 'student3@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'Mike', 'last_name': 'Johnson'},
                    {'username': 'student4', 'email': 'student4@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'Sarah', 'last_name': 'Wilson'},
                    {'username': 'student5', 'email': 'student5@demo.com', 'password': 'student123', 'role': 'student', 'first_name': 'David', 'last_name': 'Brown'},
                    
                    # Lecturers
                    {'username': 'lecturer1', 'email': 'lecturer1@demo.com', 'password': 'lecturer123', 'role': 'lecturer', 'first_name': 'Professor', 'last_name': 'Jones'},
                    {'username': 'lecturer2', 'email': 'lecturer2@demo.com', 'password': 'lecturer123', 'role': 'lecturer', 'first_name': 'Dr. Maria', 'last_name': 'Garcia'},
                    {'username': 'lecturer3', 'email': 'lecturer3@demo.com', 'password': 'lecturer123', 'role': 'lecturer', 'first_name': 'Professor', 'last_name': 'Lee'},
                ]
                
                for account_data in demo_accounts:
                    new_user = User(
                        username=account_data['username'],
                        email=account_data['email'],
                        password_hash=generate_password_hash(account_data['password']),
                        role=account_data['role'],
                        first_name=account_data['first_name'],
                        last_name=account_data['last_name'],
                        is_active=True
                    )
                    db.session.add(new_user)
                
                db.session.commit()
                print("✅ Demo accounts created successfully!")
            
            # Create demo courses if they don't exist
            existing_course = Course.query.first()
            if not existing_course:
                print("🚀 Creating demo courses...")
                create_demo_courses()
                print("✅ Demo courses created successfully!")
            
            # Create demo assignments and submissions if they don't exist
            existing_assignment = Assignment.query.filter_by(title='Introduction to Programming').first()
            if not existing_assignment:
                print("🚀 Creating demo assignments and submissions...")
                create_demo_assignments_and_submissions()
                print("✅ Demo assignments and submissions created successfully!")
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            import traceback
            traceback.print_exc()

def create_demo_courses():
    """Create demo classes and courses, enroll students"""
    try:
        # Get admin and lecturers
        admin = User.query.filter_by(username='admin').first()
        lecturer1 = User.query.filter_by(username='lecturer1').first()
        lecturer2 = User.query.filter_by(username='lecturer2').first()
        
        if not admin or not lecturer1 or not lecturer2:
            print("❌ Demo users not found")
            return
        
        # Create demo classes (admin creates classes)
        demo_classes = [
            {
                'name': 'Computer Science Year 1',
                'code': 'CS1A',
                'description': 'First year computer science students',
                'created_by': admin.id
            },
            {
                'name': 'Computer Science Year 2',
                'code': 'CS2A',
                'description': 'Second year computer science students',
                'created_by': admin.id
            }
        ]
        
        created_classes = []
        for class_data in demo_classes:
            # Check if class already exists
            existing_class = Class.query.filter_by(code=class_data['code']).first()
            if not existing_class:
                new_class = Class(**class_data)
                db.session.add(new_class)
                db.session.flush()  # Get the class ID
                created_classes.append(new_class)
            else:
                created_classes.append(existing_class)
        
        # Create demo courses
        courses = [
            {
                'name': 'Introduction to Programming',
                'code': 'CS101',
                'description': 'Learn the fundamentals of programming with Python',
                'lecturer_id': lecturer1.id,
                'class_id': created_classes[0].id
            },
            {
                'name': 'Web Development',
                'code': 'CS201',
                'description': 'Build modern web applications with HTML, CSS, and JavaScript',
                'lecturer_id': lecturer1.id,
                'class_id': created_classes[0].id
            },
            {
                'name': 'Database Systems',
                'code': 'CS301',
                'description': 'Design and implement database systems',
                'lecturer_id': lecturer2.id,
                'class_id': created_classes[1].id
            },
            {
                'name': 'Software Engineering',
                'code': 'CS401',
                'description': 'Software development methodologies and best practices',
                'lecturer_id': lecturer2.id,
                'class_id': created_classes[1].id
            }
        ]
        
        created_courses = []
        for course_data in courses:
            # Check if course already exists
            existing_course = Course.query.filter_by(code=course_data['code']).first()
            if not existing_course:
                course = Course(**course_data)
                db.session.add(course)
                created_courses.append(course)
            else:
                created_courses.append(existing_course)
        
        db.session.commit()
        
        # Assign students to classes and enroll them in courses
        students = User.query.filter_by(role='student').all()
        if students:
            mid_point = len(students) // 2
            for i, student in enumerate(students):
                if i < mid_point:
                    student.class_id = created_classes[0].id
                    # Enroll in courses for class 1
                    for course in created_courses[:2]:
                        if course not in student.enrolled_courses:
                            course.students.append(student)
                else:
                    student.class_id = created_classes[1].id
                    # Enroll in courses for class 2
                    for course in created_courses[2:]:
                        if course not in student.enrolled_courses:
                            course.students.append(student)
        
        db.session.commit()
        print("✅ Demo classes and courses created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating demo classes and courses: {e}")
        db.session.rollback()

def create_demo_assignments_and_submissions():
    """Create demo assignments and submissions"""
    try:
        # Get demo users and courses
        lecturer1 = User.query.filter_by(username='lecturer1').first()
        lecturer2 = User.query.filter_by(username='lecturer2').first()
        students = User.query.filter_by(role='student').all()
        
        # Get courses
        cs101 = Course.query.filter_by(code='CS101').first()
        cs201 = Course.query.filter_by(code='CS201').first()
        cs301 = Course.query.filter_by(code='CS301').first()
        cs401 = Course.query.filter_by(code='CS401').first()
        
        if not lecturer1 or not students or not cs101:
            return
        
        # Create sample assignments
        assignments_data = [
            {
                'title': 'Introduction to Programming',
                'description': 'Write a simple Python program that calculates the factorial of a number.',
                'instructions': 'Create a Python script that:\n1. Takes a number as input\n2. Calculates its factorial\n3. Displays the result\n\nSubmit your .py file.',
                'due_date': datetime.utcnow() + timedelta(days=7),
                'max_marks': 100,
                'file_requirements': 'Python files (.py)',
                'created_by': lecturer1.id,
                'course_id': cs101.id
            },
            {
                'title': 'Web Development Project',
                'description': 'Create a simple HTML/CSS website with at least 3 pages.',
                'instructions': 'Build a personal portfolio website with:\n1. Home page\n2. About page\n3. Contact page\n\nInclude CSS styling and make it responsive.',
                'due_date': datetime.utcnow() + timedelta(days=14),
                'max_marks': 150,
                'file_requirements': 'HTML, CSS files',
                'created_by': lecturer1.id,
                'course_id': cs201.id
            },
            {
                'title': 'Database Design Assignment',
                'description': 'Design a database schema for a library management system.',
                'instructions': 'Create an ER diagram and SQL schema for:\n1. Books table\n2. Members table\n3. Borrowing records\n\nSubmit the SQL file and ER diagram.',
                'due_date': datetime.utcnow() + timedelta(days=10),
                'max_marks': 120,
                'file_requirements': 'SQL files, images',
                'created_by': lecturer2.id if lecturer2 else lecturer1.id,
                'course_id': cs301.id if cs301 else cs101.id
            }
        ]
        
        sample_files = {
            'factorial.py': '''def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Test the function
number = int(input("Enter a number: "))
result = factorial(number)
print(f"The factorial of {number} is {result}")''',
            
            'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Welcome to My Portfolio</h1>
        <nav>
            <a href="index.html">Home</a>
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
        </nav>
    </header>
    <main>
        <h2>Hello, I'm a Web Developer</h2>
        <p>This is my portfolio website showcasing my projects and skills.</p>
    </main>
</body>
</html>''',
            
            'library_schema.sql': '''-- Library Management System Database Schema

CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publication_year INT,
    available_copies INT DEFAULT 1
);

CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    join_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE borrowing_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    book_id INT,
    borrow_date DATE DEFAULT CURRENT_DATE,
    return_date DATE,
    due_date DATE,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);'''
        }
        
        # Create assignments
        for i, assignment_data in enumerate(assignments_data):
            assignment = Assignment(**assignment_data)
            db.session.add(assignment)
            db.session.flush()  # Get the ID
            
            # Create submissions for first 3 students
            filename = list(sample_files.keys())[i]
            content = list(sample_files.values())[i]
            
            for j, student in enumerate(students[:3]):
                submission = Submission(
                    assignment_id=assignment.id,
                    student_id=student.id,
                    file_path=f'static/uploads/demo_{filename}',
                    file_name=filename,
                    file_size=len(content),
                    is_late=datetime.utcnow() > assignment.due_date,
                    content=content
                )
                db.session.add(submission)
        
        db.session.commit()
        
    except Exception as e:
        print(f"Error creating demo assignments: {e}")
        db.session.rollback()

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, lecturer, admin
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=True)  # For students
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    assignments_created = db.relationship('Assignment', backref='creator', lazy=True)
    submissions = db.relationship('Submission', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='grader', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)  # Course belongs to a class
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lecturer = db.relationship('User', backref='taught_courses', foreign_keys=[lecturer_id])
    students = db.relationship('User', secondary='course_enrollment', backref='enrolled_courses')
    
    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'

# Class model for organizing students
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Computer Science Year 1"
    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g., "CS1A"
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_classes', foreign_keys=[created_by])
    students = db.relationship('User', backref='student_class', foreign_keys='User.class_id')
    courses = db.relationship('Course', backref='class_group')
    
    def __repr__(self):
        return f'<Class {self.code}: {self.name}>'

# Course enrollment table (many-to-many relationship)
course_enrollment = db.Table('course_enrollment',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('enrolled_at', db.DateTime, default=datetime.utcnow)
)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    file_requirements = db.Column(db.String(200), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)  # Add course relationship
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    course = db.relationship('Course', backref='assignments')  # Add course relationship
    submissions = db.relationship('Submission', backref='assignment', lazy=True)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_late = db.Column(db.Boolean, default=False)
    plagiarism_score = db.Column(db.Float, default=0.0)
    plagiarism_report = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)  # Store file content for plagiarism detection
    
    # Relationships
    grades = db.relationship('Grade', backref='submission', lazy=True)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    grader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    marks = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    graded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notification_type = db.Column(db.String(50), nullable=False)  # deadline, grade, feedback, etc.

class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize database when app is created (after models are defined)
# Note: This will be called when the app starts

# Utility Functions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip', 'rar'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file_content(file_path):
    """Read file content for plagiarism detection, handling different file types"""
    try:
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension == 'txt':
            # Read text files
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif file_extension in ['pdf', 'doc', 'docx', 'ppt', 'pptx']:
            # For binary files, return a placeholder message
            return f"Binary file detected ({file_extension.upper()}). Content analysis not available for this file type."
        elif file_extension in ['zip', 'rar']:
            # For archive files
            return f"Archive file detected ({file_extension.upper()}). Content analysis not available for this file type."
        else:
            # Try to read as text with different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                        # Check if content is readable text
                        if content.isprintable() or len(content.strip()) > 0:
                            return content
                except:
                    continue
            return "Unable to read file content - unsupported file type or encoding"
            
    except Exception as e:
        return f"Error reading file: {str(e)}"

def check_plagiarism_simple_web(content):
    """Simple web-based plagiarism check using search engines"""
    try:
        import requests
        from urllib.parse import quote
        import time
        import re
        
        # Extract meaningful phrases (10+ words)
        text = re.sub(r'[^\w\s]', ' ', content)
        words = text.split()
        
        if len(words) < 10:
            return {
                'score': 0.0,
                'report': 'Text too short for meaningful plagiarism check',
                'status': 'too_short'
            }
        
        # Take first 50 words as sample
        sample_text = ' '.join(words[:50])
        
        # Simple search using DuckDuckGo
        search_url = f"https://html.duckduckgo.com/html/?q={quote(sample_text)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Simple check - if we get results, there might be similarity
            if 'No results found' in response.text:
                return {
                    'score': 0.0,
                    'report': 'No similar content found in web search',
                    'status': 'original'
                }
            else:
                return {
                    'score': 25.0,  # Conservative estimate
                    'report': 'Similar content found in web search - manual review recommended',
                    'status': 'similarity_detected'
                }
        else:
            return {
                'score': 0.0,
                'report': 'Web search failed - unable to check',
                'status': 'search_failed'
            }
            
    except Exception as e:
        return {
            'score': 0.0,
            'report': f'Web plagiarism check failed: {str(e)}',
            'status': 'error'
        }

def check_plagiarism_with_api(content, author_email, author_name=None):
    """Check plagiarism using PlagiarismCheck.org API"""
    try:
        if not app.config['USE_PLAGIARISM_CHECK_API'] or not app.config['PLAGIARISM_CHECK_API_TOKEN']:
            print("⚠️ PlagiarismCheck.org API not configured, falling back to local check")
            return None
        
        # Prepare API request data
        data = {
            'group_token': app.config['PLAGIARISM_CHECK_API_TOKEN'],
            'author': author_email,
            'text': content
        }
        
        if author_name:
            data['custom_author'] = author_name
        
        # Make API request
        response = requests.post(
            app.config['PLAGIARISM_CHECK_API_URL'],
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'check_id' in result:
                print(f"✅ Plagiarism check submitted successfully. Check ID: {result['check_id']}")
                return {
                    'check_id': result['check_id'],
                    'status': 'submitted',
                    'message': 'Plagiarism check submitted successfully'
                }
            else:
                print(f"❌ API response error: {result}")
                return None
        else:
            print(f"❌ API request failed with status {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ PlagiarismCheck.org API request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ PlagiarismCheck.org API request failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error in plagiarism API check: {e}")
        return None

def get_plagiarism_report(check_id):
    """Get plagiarism report from PlagiarismCheck.org API"""
    try:
        if not app.config['USE_PLAGIARISM_CHECK_API'] or not app.config['PLAGIARISM_CHECK_API_TOKEN']:
            return None
        
        # API endpoint for getting report
        report_url = f"https://plagiarismcheck.org/api/org/text/report/{check_id}/"
        
        headers = {
            'Authorization': f"Token {app.config['PLAGIARISM_CHECK_API_TOKEN']}"
        }
        
        response = requests.get(report_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get plagiarism report: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting plagiarism report: {e}")
        return None

def calculate_plagiarism_score(content, other_submissions):
    """Calculate comprehensive plagiarism score using Dolos (if available) or local methods"""
    if not other_submissions or not content:
        return 0.0
    
    # Try Dolos integration first (for code submissions)
    if dolos_integration and dolos_integration.is_available():
        try:
            # Prepare submissions for Dolos analysis
            submissions = [{"id": "current", "content": content}]
            for i, sub in enumerate(other_submissions):
                if hasattr(sub, 'content') and sub.content and len(sub.content.strip()) > 10:
                    submissions.append({"id": f"sub_{i}", "content": sub.content})
            
            if len(submissions) >= 2:
                # Run Dolos analysis
                dolos_results = dolos_integration.analyze_submissions(submissions)
                
                if "error" not in dolos_results and "plagiarism_scores" in dolos_results:
                    # Extract score for current submission
                    current_score = dolos_results["plagiarism_scores"].get("current", 0.0)
                    print(f"🔍 Dolos analysis completed - Score: {current_score}%")
                    return round(current_score, 2)
                else:
                    print(f"⚠️ Dolos analysis failed: {dolos_results.get('error', 'Unknown error')}")
                    print("🔄 Falling back to local plagiarism detection...")
        except Exception as e:
            print(f"⚠️ Dolos integration error: {e}")
            print("🔄 Falling back to local plagiarism detection...")
    
    # Fallback to local comprehensive plagiarism detection
    return calculate_local_plagiarism_score(content, other_submissions)

def calculate_local_plagiarism_score(content, other_submissions):
    """Calculate comprehensive plagiarism score using multiple local methods"""
    if not other_submissions or not content:
        return 0.0
    
    # Prepare documents - filter out empty or invalid content
    documents = [content]
    for sub in other_submissions:
        if hasattr(sub, 'content') and sub.content and len(sub.content.strip()) > 10:
            documents.append(sub.content)
    
    if len(documents) < 2:
        return 0.0
    
    try:
        # Method 1: Enhanced TF-IDF with multiple n-grams
        tfidf_score = calculate_tfidf_similarity(documents)
        
        # Method 2: Semantic similarity using word contexts
        semantic_score = calculate_semantic_similarity(documents)
        
        # Method 3: Content fingerprinting
        fingerprint_score = calculate_fingerprint_similarity(documents)
        
        # Method 4: Phrase matching
        phrase_score = calculate_phrase_similarity(documents)
        
        # Method 5: Structure similarity
        structure_score = calculate_structure_similarity(documents)
        
        # Weighted combination of all methods
        weights = {
            'tfidf': 0.3,
            'semantic': 0.25,
            'fingerprint': 0.2,
            'phrase': 0.15,
            'structure': 0.1
        }
        
        final_score = (
            tfidf_score * weights['tfidf'] +
            semantic_score * weights['semantic'] +
            fingerprint_score * weights['fingerprint'] +
            phrase_score * weights['phrase'] +
            structure_score * weights['structure']
        )
        
        print(f"🔍 Local plagiarism analysis completed - Score: {final_score}%")
        return round(final_score, 2)
        
    except Exception as e:
        print(f"Error in comprehensive plagiarism calculation: {e}")
        return calculate_simple_similarity(content, other_submissions)

def calculate_tfidf_similarity(documents):
    """Enhanced TF-IDF similarity calculation"""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        
        # Create enhanced TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 4),  # Use 1-4 word combinations
            max_features=2000,
            lowercase=True,
            strip_accents='unicode',
            min_df=1,
            max_df=0.95
        )
        
        # Fit and transform documents
    tfidf_matrix = vectorizer.fit_transform(documents)
    
        # Calculate cosine similarity between first document and all others
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        # Get maximum similarity score
        max_similarity = np.max(similarities) if similarities.size > 0 else 0.0
        
        return max_similarity * 100
        
    except ImportError:
        return calculate_simple_similarity(documents[0], documents[1:])
    except Exception as e:
        print(f"TF-IDF calculation error: {e}")
        return 0.0

def calculate_semantic_similarity(documents):
    """Calculate semantic similarity using word frequency and context"""
    try:
        import re
        from collections import Counter
        
        def preprocess_text(text):
            # Clean and tokenize text
            text = re.sub(r'[^\w\s]', ' ', text.lower())
            words = text.split()
            return [word for word in words if len(word) > 2]
        
        def get_word_contexts(text, window_size=3):
            """Get word contexts for semantic analysis"""
            words = preprocess_text(text)
            contexts = {}
            for i, word in enumerate(words):
                start = max(0, i - window_size)
                end = min(len(words), i + window_size + 1)
                context = words[start:end]
                if word not in contexts:
                    contexts[word] = []
                contexts[word].extend(context)
            return contexts
        
        # Get contexts for all documents
        all_contexts = []
        for doc in documents:
            contexts = get_word_contexts(doc)
            all_contexts.append(contexts)
        
        # Calculate semantic overlap
        if len(all_contexts) < 2:
            return 0.0
        
        main_contexts = all_contexts[0]
        max_similarity = 0.0
        
        for other_contexts in all_contexts[1:]:
            similarity = 0.0
            total_words = 0
            
            for word, contexts in main_contexts.items():
                if word in other_contexts:
                    # Calculate context similarity
                    main_context_counter = Counter(contexts)
                    other_context_counter = Counter(other_contexts[word])
                    
                    # Jaccard similarity of contexts
                    intersection = sum((main_context_counter & other_context_counter).values())
                    union = sum((main_context_counter | other_context_counter).values())
                    
                    if union > 0:
                        similarity += intersection / union
                    total_words += 1
            
            if total_words > 0:
                avg_similarity = similarity / total_words
                max_similarity = max(max_similarity, avg_similarity)
        
        return max_similarity * 100
        
    except Exception as e:
        print(f"Semantic similarity error: {e}")
        return 0.0

def calculate_fingerprint_similarity(documents):
    """Calculate similarity using content fingerprinting"""
    try:
        import hashlib
        import re
        
        def create_fingerprint(text, n=5):
            """Create content fingerprint using n-grams"""
            # Clean text
            text = re.sub(r'[^\w\s]', ' ', text.lower())
            words = text.split()
            
            # Create n-grams
            ngrams = []
            for i in range(len(words) - n + 1):
                ngram = ' '.join(words[i:i+n])
                ngrams.append(ngram)
            
            # Hash n-grams
            fingerprints = set()
            for ngram in ngrams:
                fingerprint = hashlib.md5(ngram.encode()).hexdigest()
                fingerprints.add(fingerprint)
            
            return fingerprints
        
        if len(documents) < 2:
            return 0.0
        
        main_fingerprints = create_fingerprint(documents[0])
        max_similarity = 0.0
        
        for doc in documents[1:]:
            other_fingerprints = create_fingerprint(doc)
            
            # Calculate Jaccard similarity
            intersection = len(main_fingerprints & other_fingerprints)
            union = len(main_fingerprints | other_fingerprints)
            
            if union > 0:
                similarity = intersection / union
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity * 100
        
    except Exception as e:
        print(f"Fingerprint similarity error: {e}")
        return 0.0

def calculate_phrase_similarity(documents):
    """Calculate similarity based on common phrases"""
    try:
        import re
        from collections import Counter
        
        def extract_phrases(text, min_length=3, max_length=8):
            """Extract meaningful phrases from text"""
            # Clean text
            text = re.sub(r'[^\w\s]', ' ', text.lower())
            words = text.split()
            
            phrases = []
            for length in range(min_length, min(max_length + 1, len(words) + 1)):
                for i in range(len(words) - length + 1):
                    phrase = ' '.join(words[i:i+length])
                    if len(phrase.strip()) > 0:
                        phrases.append(phrase)
            
            return Counter(phrases)
        
        if len(documents) < 2:
            return 0.0
        
        main_phrases = extract_phrases(documents[0])
        max_similarity = 0.0
        
        for doc in documents[1:]:
            other_phrases = extract_phrases(doc)
            
            # Calculate phrase overlap
            common_phrases = main_phrases & other_phrases
            total_phrases = main_phrases | other_phrases
            
            if len(total_phrases) > 0:
                similarity = sum(common_phrases.values()) / sum(total_phrases.values())
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity * 100
        
    except Exception as e:
        print(f"Phrase similarity error: {e}")
        return 0.0

def calculate_structure_similarity(documents):
    """Calculate similarity based on document structure"""
    try:
        import re
        
        def analyze_structure(text):
            """Analyze document structure"""
            structure = {
                'paragraphs': len(re.split(r'\n\s*\n', text)),
                'sentences': len(re.split(r'[.!?]+', text)),
                'words': len(text.split()),
                'avg_sentence_length': 0,
                'avg_paragraph_length': 0
            }
            
            if structure['sentences'] > 0:
                structure['avg_sentence_length'] = structure['words'] / structure['sentences']
            
            if structure['paragraphs'] > 0:
                structure['avg_paragraph_length'] = structure['words'] / structure['paragraphs']
            
            return structure
        
        if len(documents) < 2:
            return 0.0
        
        main_structure = analyze_structure(documents[0])
        max_similarity = 0.0
        
        for doc in documents[1:]:
            other_structure = analyze_structure(doc)
            
            # Calculate structural similarity
            similarities = []
            
            # Compare ratios
            if other_structure['avg_sentence_length'] > 0 and main_structure['avg_sentence_length'] > 0:
                sent_sim = 1 - abs(main_structure['avg_sentence_length'] - other_structure['avg_sentence_length']) / max(main_structure['avg_sentence_length'], other_structure['avg_sentence_length'])
                similarities.append(sent_sim)
            
            if other_structure['avg_paragraph_length'] > 0 and main_structure['avg_paragraph_length'] > 0:
                para_sim = 1 - abs(main_structure['avg_paragraph_length'] - other_structure['avg_paragraph_length']) / max(main_structure['avg_paragraph_length'], other_structure['avg_paragraph_length'])
                similarities.append(para_sim)
            
            if similarities:
                avg_similarity = sum(similarities) / len(similarities)
                max_similarity = max(max_similarity, avg_similarity)
        
        return max_similarity * 100
        
    except Exception as e:
        print(f"Structure similarity error: {e}")
        return 0.0

def generate_detailed_plagiarism_report(content, other_contents, plagiarism_score):
    """Generate detailed plagiarism report with analysis"""
    try:
        report = f"COMPREHENSIVE PLAGIARISM ANALYSIS REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # Basic information
        report += f"📊 Overall Plagiarism Score: {plagiarism_score:.2f}%\n"
        report += f"📝 Documents Compared: {len(other_contents) + 1}\n"
        report += f"🔍 Analysis Methods: 5 (TF-IDF, Semantic, Fingerprint, Phrase, Structure)\n\n"
        
        # Risk assessment
        if plagiarism_score >= 80:
            report += "🚨 HIGH RISK: Significant similarity detected\n"
            report += "   Recommendation: Immediate review required\n"
        elif plagiarism_score >= 50:
            report += "⚠️  MEDIUM RISK: Moderate similarity detected\n"
            report += "   Recommendation: Manual review recommended\n"
        elif plagiarism_score >= 20:
            report += "🔍 LOW RISK: Minor similarity detected\n"
            report += "   Recommendation: Quick review suggested\n"
        else:
            report += "✅ LOW RISK: Minimal similarity detected\n"
            report += "   Recommendation: Content appears original\n"
        
        report += "\n"
        
        # Analysis breakdown
        report += "📋 ANALYSIS BREAKDOWN:\n"
        report += "-" * 30 + "\n"
        
        # Calculate individual method scores for breakdown
        try:
            documents = [content] + other_contents
            tfidf_score = calculate_tfidf_similarity(documents)
            semantic_score = calculate_semantic_similarity(documents)
            fingerprint_score = calculate_fingerprint_similarity(documents)
            phrase_score = calculate_phrase_similarity(documents)
            structure_score = calculate_structure_similarity(documents)
            
            report += f"• TF-IDF Similarity: {tfidf_score:.1f}% (Word frequency analysis)\n"
            report += f"• Semantic Similarity: {semantic_score:.1f}% (Context and meaning)\n"
            report += f"• Fingerprint Match: {fingerprint_score:.1f}% (Content fingerprinting)\n"
            report += f"• Phrase Overlap: {phrase_score:.1f}% (Common phrases)\n"
            report += f"• Structure Similarity: {structure_score:.1f}% (Document structure)\n"
        except:
            report += "• Analysis breakdown unavailable\n"
        
        report += "\n"
        
        # Content analysis
        report += "📄 CONTENT ANALYSIS:\n"
        report += "-" * 30 + "\n"
        report += f"• Word Count: {len(content.split())} words\n"
        report += f"• Character Count: {len(content)} characters\n"
        report += f"• Sentence Count: {len([s for s in content.split('.') if s.strip()])} sentences\n"
        
        # Common words analysis
        try:
            import re
            from collections import Counter
            words = re.findall(r'\b\w+\b', content.lower())
            word_freq = Counter(words)
            common_words = word_freq.most_common(5)
            report += f"• Most Common Words: {', '.join([f'{word}({count})' for word, count in common_words])}\n"
        except:
            pass
        
        report += "\n"
        
        # Recommendations
        report += "💡 RECOMMENDATIONS:\n"
        report += "-" * 30 + "\n"
        
        if plagiarism_score >= 50:
            report += "• Review the submission for potential plagiarism\n"
            report += "• Check for proper citations and references\n"
            report += "• Consider discussing with the student\n"
        elif plagiarism_score >= 20:
            report += "• Verify originality of similar sections\n"
            report += "• Check for proper attribution\n"
        else:
            report += "• Content appears to be original\n"
            report += "• No immediate action required\n"
        
        report += "\n"
        report += "🔧 TECHNICAL DETAILS:\n"
        report += "-" * 30 + "\n"
        report += "• Detection Engine: Multi-method Local Analysis\n"
        report += "• Comparison Database: Student submissions only\n"
        report += "• Analysis Date: " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n"
        report += "• Confidence Level: High (Local analysis)\n"
        
        return report
        
    except Exception as e:
        return f"Plagiarism Analysis Report\nScore: {plagiarism_score:.2f}%\nError generating detailed report: {str(e)}"

def calculate_simple_similarity(content, other_submissions):
    """Simple fallback similarity calculation"""
    try:
        import re
        from collections import Counter
        
        def get_word_frequency(text):
            # Clean and tokenize text
            text = re.sub(r'[^\w\s]', ' ', text.lower())
            words = text.split()
            return Counter(words)
        
        main_words = get_word_frequency(content)
        max_similarity = 0.0
        
        for sub in other_submissions:
            if hasattr(sub, 'content') and sub.content:
                other_words = get_word_frequency(sub.content)
                
                # Calculate Jaccard similarity
                intersection = len(set(main_words.keys()) & set(other_words.keys()))
                union = len(set(main_words.keys()) | set(other_words.keys()))
                
                if union > 0:
                    similarity = intersection / union
                    max_similarity = max(max_similarity, similarity)
        
        return max_similarity * 100
        
    except Exception as e:
        print(f"Simple similarity error: {e}")
        return 0.0

def send_notification(user_id, title, message, notification_type):
    """Send notification to user"""
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type
    )
    db.session.add(notification)
    db.session.commit()

def send_email(to_email, subject, template, **kwargs):
    """Send email using SendGrid or Flask-Mail"""
    try:
        if app.config['MAIL_SUPPRESS_SEND']:
            print(f"📧 Email suppressed: {subject} to {to_email}")
            return True
        
        # Add base URL for email templates
        base_url = os.environ.get('BASE_URL', 'http://localhost:5000')
        kwargs['base_url'] = base_url
        
        # Render email template
        html_content = render_template(f'emails/{template}', **kwargs)
        
        # Use SendGrid if configured
        if app.config['USE_SENDGRID'] and app.config['SENDGRID_API_KEY']:
            return send_email_sendgrid(to_email, subject, html_content)
        
        # Fallback to Flask-Mail
        return send_email_flask_mail(to_email, subject, html_content)
        
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

def send_email_sendgrid(to_email, subject, html_content):
    """Send email using SendGrid API"""
    try:
        sg = sendgrid.SendGridAPIClient(api_key=app.config['SENDGRID_API_KEY'])
        
        from_email = Email(app.config['SENDGRID_FROM_EMAIL'])
        to_email_obj = To(to_email)
        content = Content("text/html", html_content)
        
        mail = SendGridMail(from_email, to_email_obj, subject, content)
        
        # Send email in background thread
        def send_async_sendgrid():
            try:
                response = sg.send(mail)
                print(f"📧 SendGrid email sent: {subject} to {to_email} (Status: {response.status_code})")
                return True
            except Exception as e:
                print(f"❌ SendGrid email failed: {e}")
                return False
        
        thread = threading.Thread(target=send_async_sendgrid)
        thread.start()
        
        return True
        
    except Exception as e:
        print(f"❌ SendGrid setup failed: {e}")
        return False

def send_email_flask_mail(to_email, subject, html_content):
    """Send email using Flask-Mail (fallback)"""
    try:
        if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
            print(f"⚠️ Email not configured: {subject} to {to_email}")
            return False
            
        # Use proper sender format with name
        sender = app.config['MAIL_DEFAULT_SENDER']
        if not sender.startswith('E-Assignment.edu.gh'):
            sender = f"E-Assignment.edu.gh <{app.config['MAIL_USERNAME']}>"
        
        msg = Message(
            subject=subject,
            recipients=[to_email],
            sender=sender
        )
        
        msg.html = html_content
        
        # Send email in background thread
        def send_async_email(app, msg):
            with app.app_context():
                mail.send(msg)
        
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.start()
        
        print(f"📧 Flask-Mail email sent: {subject} to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Flask-Mail failed: {e}")
        return False

def send_assignment_notification(assignment, students):
    """Send email notification about new assignment"""
    results = []
    for student in students:
        result = send_email(
            to_email=student.email,
            subject=f"New Assignment: {assignment.title}",
            template='new_assignment.html',
            student=student,
            assignment=assignment
        )
        results.append(result)
    return all(results)

def send_submission_notification(submission):
    """Send email notification about submission"""
    # Notify the lecturer who created the assignment
    lecturer = User.query.get(submission.assignment.created_by)
    if lecturer:
        return send_email(
            to_email=lecturer.email,
            subject=f"New Submission: {submission.assignment.title}",
            template='new_submission.html',
            lecturer=lecturer,
            submission=submission,
            student=submission.student,
            assignment=submission.assignment
        )
    return False

def send_grade_notification(grade):
    """Send email notification about grade"""
    try:
        # Access student through submission relationship
        student = grade.submission.student
        assignment = grade.submission.assignment
        
        if student and assignment and grade:
            send_email(
                to_email=student.email,
                subject=f"Grade Posted: {assignment.title}",
                template='grade_notification.html',
                student=student,
                grade=grade,
                assignment=assignment
            )
            return True
    except Exception as e:
        print(f"Error sending grade notification: {e}")
        return False

def send_deadline_reminder(assignment, students):
    """Send deadline reminder emails"""
    results = []
    for student in students:
        # Check if student has already submitted
        existing_submission = Submission.query.filter_by(
            assignment_id=assignment.id,
            student_id=student.id
        ).first()
        
        if not existing_submission:
            result = send_email(
                to_email=student.email,
                subject=f"Deadline Reminder: {assignment.title}",
                template='deadline_reminder.html',
                student=student,
                assignment=assignment
            )
            results.append(result)
    return all(results) if results else True

def send_welcome_email(user):
    """Send welcome email to new user"""
    return send_email(
        to_email=user.email,
        subject="Welcome to E-Assignment Submission System",
        template='welcome.html',
        user=user
    )

def check_deadline_reminders():
    """Check for upcoming deadlines and send reminders"""
    with app.app_context():
        # Get assignments due in the next 24 hours
        tomorrow = datetime.utcnow() + timedelta(days=1)
        upcoming_assignments = Assignment.query.filter(
            Assignment.due_date <= tomorrow,
            Assignment.due_date > datetime.utcnow(),
            Assignment.is_active == True
        ).all()
        
        for assignment in upcoming_assignments:
            # Get all students who haven't submitted
            submitted_student_ids = [s.student_id for s in assignment.submissions]
            students = User.query.filter(
                User.role == 'student',
                User.is_active == True,
                ~User.id.in_(submitted_student_ids)
            ).all()
            
            for student in students:
                # Check if we already sent a reminder for this assignment
                existing_reminder = Notification.query.filter_by(
                    user_id=student.id,
                    notification_type='deadline',
                    title=f"Deadline Reminder: {assignment.title}"
                ).first()
                
                if not existing_reminder:
                    hours_until_due = (assignment.due_date - datetime.utcnow()).total_seconds() / 3600
                    
                    if hours_until_due <= 24:  # Send reminder if due within 24 hours
                        send_notification(
                            student.id,
                            f"Deadline Reminder: {assignment.title}",
                            f"Assignment '{assignment.title}' is due in {hours_until_due:.1f} hours. Don't forget to submit!",
                            'deadline'
                        )
                        
                        # Send email reminder
                        send_deadline_reminder(assignment, [student])

def check_overdue_assignments():
    """Check for overdue assignments and send notifications"""
    with app.app_context():
        # Get assignments that are past due
        overdue_assignments = Assignment.query.filter(
            Assignment.due_date < datetime.utcnow(),
            Assignment.is_active == True
        ).all()
        
        for assignment in overdue_assignments:
            # Get all students who haven't submitted
            submitted_student_ids = [s.student_id for s in assignment.submissions]
            students = User.query.filter(
                User.role == 'student',
                User.is_active == True,
                ~User.id.in_(submitted_student_ids)
            ).all()
            
            for student in students:
                # Check if we already sent an overdue notification
                existing_notification = Notification.query.filter_by(
                    user_id=student.id,
                    notification_type='deadline',
                    title=f"Overdue: {assignment.title}"
                ).first()
                
                if not existing_notification:
                    hours_overdue = (datetime.utcnow() - assignment.due_date).total_seconds() / 3600
                    send_notification(
                        student.id,
                        f"Overdue: {assignment.title}",
                        f"Assignment '{assignment.title}' was due {hours_overdue:.1f} hours ago. Please submit as soon as possible.",
                        'deadline'
                    )

# Schedule automated tasks
scheduler.add_job(
    func=check_deadline_reminders,
    trigger="interval",
    hours=1,  # Check every hour
    id='deadline_reminders'
)

scheduler.add_job(
    func=check_overdue_assignments,
    trigger="interval",
    hours=6,  # Check every 6 hours
    id='overdue_assignments'
)

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password) and user.is_active:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/demo-login')
def demo_login():
    """Demo login page with clickable account buttons"""
    return render_template('demo_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            first_name=first_name,
            last_name=last_name
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Send welcome email
        send_welcome_email(user)
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        return redirect(url_for('student_dashboard'))
    elif current_user.role == 'lecturer':
        return redirect(url_for('lecturer_dashboard'))
    elif current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    return redirect(url_for('index'))

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get student's submissions
    submissions = Submission.query.filter_by(student_id=current_user.id).all()
    
    # Get available assignments
    assignments = Assignment.query.filter_by(is_active=True).all()
    
    # Get notifications
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).limit(5).all()
    
    return render_template('student_dashboard.html', 
                         submissions=submissions, 
                         assignments=assignments,
                         notifications=notifications)

@app.route('/student/assignments')
@login_required
def student_assignments():
    """Student assignments page - shows assignments from enrolled courses only"""
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get assignments only from courses the student is enrolled in
    enrolled_course_ids = [course.id for course in current_user.enrolled_courses]
    assignments = Assignment.query.filter(
        Assignment.course_id.in_(enrolled_course_ids),
        Assignment.is_active == True
    ).all()
    
    # Get student's submissions to show status
    submissions = Submission.query.filter_by(student_id=current_user.id).all()
    
    return render_template('student_assignments.html', 
                         assignments=assignments, 
                         submissions=submissions)

@app.route('/lecturer/dashboard')
@login_required
def lecturer_dashboard():
    if current_user.role != 'lecturer':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get lecturer's assignments
    assignments = Assignment.query.filter_by(created_by=current_user.id).all()
    
    # Get all submissions for grading
    submissions = Submission.query.join(Assignment).filter(Assignment.created_by == current_user.id).all()
    
    return render_template('lecturer_dashboard.html', 
                         assignments=assignments, 
                         submissions=submissions)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get system statistics
    total_students = User.query.filter_by(role='student').count()
    total_lecturers = User.query.filter_by(role='lecturer').count()
    total_assignments = Assignment.query.count()
    total_submissions = Submission.query.count()
    
    # Get recent activity
    recent_submissions = Submission.query.order_by(Submission.submitted_at.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_students=total_students,
                         total_lecturers=total_lecturers,
                         total_assignments=total_assignments,
                         total_submissions=total_submissions,
                         recent_submissions=recent_submissions)

@app.route('/assignment/create', methods=['GET', 'POST'])
@login_required
def create_assignment():
    if current_user.role not in ['lecturer', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        instructions = request.form['instructions']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')
        max_marks = int(request.form['max_marks'])
        file_requirements = request.form['file_requirements']
        course_id = int(request.form['course_id'])
        
        assignment = Assignment(
            title=title,
            description=description,
            instructions=instructions,
            due_date=due_date,
            max_marks=max_marks,
            file_requirements=file_requirements,
            created_by=current_user.id,
            course_id=course_id
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        # Get course and students enrolled in this course
        course = Course.query.get(course_id)
        students = course.students if course else []
        
        # Send notifications only to students in this course
        for student in students:
            send_notification(
                student.id,
                f"New Assignment: {title}",
                f"A new assignment '{title}' has been created for {course.name}. Due date: {due_date.strftime('%Y-%m-%d %H:%M')}",
                'assignment'
            )
        
        # Send email notifications only to students in this course
        send_assignment_notification(assignment, students)
        
        flash(f'Assignment created successfully for {course.name}!', 'success')
        return redirect(url_for('lecturer_dashboard'))
    
    # Get courses taught by current lecturer
    courses = Course.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('create_assignment.html', courses=courses)

@app.route('/class/create', methods=['GET', 'POST'])
@login_required
def create_class():
    if current_user.role != 'admin':
        flash('Access denied. Only administrators can create classes.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code'].upper()
        description = request.form.get('description', '')
        
        # Check if class code already exists
        existing_class = Class.query.filter_by(code=code).first()
        if existing_class:
            flash('Class code already exists!', 'error')
            return render_template('create_class.html')
        
        # Create new class
        new_class = Class(
            name=name,
            code=code,
            description=description,
            created_by=current_user.id
        )
        
        db.session.add(new_class)
        db.session.commit()
        
        flash(f'Class "{name}" created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('create_class.html')

@app.route('/course/create', methods=['GET', 'POST'])
@login_required
def create_course():
    if current_user.role not in ['lecturer', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all classes (admin creates classes, lecturers select from them)
    classes = Class.query.all()
    
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code'].upper()
        description = request.form.get('description', '')
        class_id = request.form.get('class_id')
        
        if not class_id:
            flash('Please select a class for this course!', 'error')
            return render_template('create_course.html', classes=classes)
        
        # Check if course code already exists
        existing_course = Course.query.filter_by(code=code).first()
        if existing_course:
            flash('Course code already exists!', 'error')
            return render_template('create_course.html', classes=classes)
        
        # Create new course
        course = Course(
            name=name,
            code=code,
            description=description,
            lecturer_id=current_user.id,
            class_id=int(class_id)
        )
        
        db.session.add(course)
        db.session.commit()
        
        flash(f'Course "{name}" created successfully!', 'success')
        return redirect(url_for('lecturer_dashboard'))
    
    return render_template('create_course.html', classes=classes)

@app.route('/class/select', methods=['GET', 'POST'])
@login_required
def select_class():
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all available classes
    available_classes = Class.query.all()
    
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        
        if not class_id:
            flash('Please select a class.', 'error')
            return render_template('select_class.html', available_classes=available_classes)
        
        # Assign student to class
        current_user.class_id = int(class_id)
        db.session.commit()
        
        selected_class = Class.query.get(int(class_id))
        flash(f'Successfully joined {selected_class.name} ({selected_class.code})!', 'success')
        return redirect(url_for('enroll_course'))
    
    return render_template('select_class.html', available_classes=available_classes)

@app.route('/course/enroll', methods=['GET', 'POST'])
@login_required
def enroll_course():
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if student has selected a class
    if not current_user.class_id:
        flash('Please select your class first.', 'info')
        return redirect(url_for('select_class'))
    
    # Get available courses for the student's class (courses they're not already enrolled in)
    enrolled_course_ids = [course.id for course in current_user.enrolled_courses]
    available_courses = Course.query.filter(
        Course.class_id == current_user.class_id,
        ~Course.id.in_(enrolled_course_ids)
    ).all()
    
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        
        if not course_id:
            flash('Please select a course to enroll in.', 'error')
            return render_template('enroll_course.html', available_courses=available_courses)
        
        # Find course by ID
        course = Course.query.get(int(course_id))
        
        if not course:
            flash('Course not found. Please try again.', 'error')
            return render_template('enroll_course.html', available_courses=available_courses)
        
        # Check if already enrolled (double-check)
        if course in current_user.enrolled_courses:
            flash('You are already enrolled in this course!', 'error')
            return render_template('enroll_course.html', available_courses=available_courses)
        
        # Enroll student
        course.students.append(current_user)
        db.session.commit()
        
        flash(f'Successfully enrolled in {course.name} ({course.code})!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('enroll_course.html', available_courses=available_courses)

@app.route('/course/available')
@login_required
def available_courses():
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all courses not enrolled by current student
    enrolled_course_ids = [course.id for course in current_user.enrolled_courses]
    available_courses = Course.query.filter(~Course.id.in_(enrolled_course_ids)).all()
    
    return render_template('available_courses.html', courses=available_courses)

@app.route('/assignment/submit/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def submit_assignment(assignment_id):
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Check if submission is late
            is_late = datetime.utcnow() > assignment.due_date
            
            # Read file content for plagiarism detection
            file_content = read_file_content(file_path)
            
            # Create submission record
            try:
                submission = Submission(
                    assignment_id=assignment_id,
                    student_id=current_user.id,
                    file_path=file_path,
                    file_name=file.filename,
                    file_size=os.path.getsize(file_path),
                    is_late=is_late,
                    content=file_content if len(file_content) < 10000 else file_content[:10000]  # Limit content size
                )
            except TypeError:
                # Fallback if content column doesn't exist
            submission = Submission(
                assignment_id=assignment_id,
                student_id=current_user.id,
                file_path=file_path,
                file_name=file.filename,
                file_size=os.path.getsize(file_path),
                is_late=is_late
            )
            
            db.session.add(submission)
            db.session.commit()
            
            # Send notification to lecturer
            send_notification(
                assignment.created_by,
                f"New Submission: {assignment.title}",
                f"{current_user.first_name} {current_user.last_name} has submitted '{assignment.title}'",
                'submission'
            )
            
            # Send email notification
            send_submission_notification(submission)
            
            flash('Assignment submitted successfully!', 'success')
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid file type', 'error')
    
    return render_template('submit_assignment.html', assignment=assignment)

@app.route('/submission/grade/<int:submission_id>', methods=['GET', 'POST'])
@login_required
def grade_submission(submission_id):
    if current_user.role not in ['lecturer', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    submission = Submission.query.get_or_404(submission_id)
    
    if request.method == 'POST':
        marks = float(request.form['marks'])
        feedback = request.form['feedback']
        
        # Check if already graded
        existing_grade = Grade.query.filter_by(submission_id=submission_id).first()
        if existing_grade:
            existing_grade.marks = marks
            existing_grade.feedback = feedback
            existing_grade.grader_id = current_user.id
        else:
            grade = Grade(
                submission_id=submission_id,
                grader_id=current_user.id,
                marks=marks,
                feedback=feedback
            )
            db.session.add(grade)
        
        db.session.commit()
        
        # Send notification to student
        try:
        send_notification(
            submission.student_id,
            f"Grade Received: {submission.assignment.title}",
            f"Your submission for '{submission.assignment.title}' has been graded. Marks: {marks}",
            'grade'
        )
        except Exception as e:
            print(f"Notification sending failed: {e}")
            # Don't fail the grading process if notification fails
        
        # Send email notification
        grade = Grade.query.filter_by(submission_id=submission_id).first()
        if grade:
            try:
                send_grade_notification(grade)
            except Exception as e:
                print(f"Email notification failed: {e}")
                # Don't fail the grading process if email fails
        
        flash('Submission graded successfully!', 'success')
        return redirect(url_for('lecturer_dashboard'))
    
    return render_template('grade_submission.html', submission=submission)

@app.route('/assignment/<int:assignment_id>/submissions')
@login_required
def view_assignment_submissions(assignment_id):
    """View all submissions for a specific assignment"""
    if current_user.role not in ['lecturer', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Check if current user created this assignment or is admin
    if assignment.created_by != current_user.id and current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all submissions for this assignment
    submissions = Submission.query.filter_by(assignment_id=assignment_id).all()
    
    return render_template('view_submissions.html', 
                         assignment=assignment, 
                         submissions=submissions)

@app.route('/submission/<int:submission_id>/view')
@login_required
def view_submission_details(submission_id):
    """View detailed information about a specific submission"""
    submission = Submission.query.get_or_404(submission_id)
    
    # Check access permissions
    can_view = False
    if current_user.role == 'student' and submission.student_id == current_user.id:
        can_view = True
    elif current_user.role in ['lecturer', 'admin']:
        if current_user.role == 'admin' or submission.assignment.created_by == current_user.id:
            can_view = True
    
    if not can_view:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('view_submission_details.html', submission=submission)

@app.route('/assignment/<int:assignment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_assignment(assignment_id):
    """Edit assignment details"""
    if current_user.role not in ['lecturer', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Check if current user created this assignment or is admin
    if assignment.created_by != current_user.id and current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        assignment.title = request.form['title']
        assignment.description = request.form['description']
        assignment.instructions = request.form['instructions']
        assignment.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')
        assignment.max_marks = int(request.form['max_marks'])
        assignment.file_requirements = request.form['file_requirements']
        
        db.session.commit()
        
        flash('Assignment updated successfully!', 'success')
        return redirect(url_for('view_assignment_submissions', assignment_id=assignment.id))
    
    return render_template('edit_assignment.html', assignment=assignment)

@app.route('/api/plagiarism-check/<int:submission_id>')
@login_required
def plagiarism_check(submission_id):
    try:
    submission = Submission.query.get_or_404(submission_id)
    
        # Use stored content or read from file (with fallback for missing column)
        try:
            content = submission.content or read_file_content(submission.file_path)
        except AttributeError:
            # Fallback if content column doesn't exist
            content = read_file_content(submission.file_path)
        
        # Check if content is readable for plagiarism detection
        if not content or "Binary file detected" in content or "Archive file detected" in content or "Unable to read" in content:
            submission.plagiarism_score = 0.0
            submission.plagiarism_report = f"Plagiarism check skipped: {content or 'No content available'}"
            db.session.commit()
            
            return jsonify({
                'plagiarism_score': 0.0,
                'report': submission.plagiarism_report,
                'status': 'skipped',
                'reason': content or 'No content available'
            })
        
        # Use comprehensive local plagiarism detection
        print("Running comprehensive local plagiarism detection...")
    
    # Get other submissions for comparison
    other_submissions = Submission.query.filter(
        Submission.assignment_id == submission.assignment_id,
        Submission.id != submission_id
    ).all()
    
        # Use stored content from other submissions
        other_contents = []
        for other_sub in other_submissions:
            try:
                other_content = other_sub.content or read_file_content(other_sub.file_path)
            except AttributeError:
                # Fallback if content column doesn't exist
                other_content = read_file_content(other_sub.file_path)
            
            if other_content and not any(msg in other_content for msg in ["Binary file detected", "Archive file detected", "Unable to read"]):
                other_contents.append(other_content)
    
    # Calculate plagiarism score
        plagiarism_score = calculate_plagiarism_score(content, other_contents)
        
        # Generate detailed plagiarism report
        plagiarism_report = generate_detailed_plagiarism_report(content, other_contents, plagiarism_score)
    
    # Update submission record
    submission.plagiarism_score = plagiarism_score
        submission.plagiarism_report = plagiarism_report
    db.session.commit()
    
    return jsonify({
        'plagiarism_score': plagiarism_score,
            'report': plagiarism_report,
            'status': 'completed_comprehensive'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Plagiarism check failed: {str(e)}',
            'plagiarism_score': 0.0,
            'report': 'Plagiarism check failed due to an error',
            'status': 'error'
        }), 500

@app.route('/api/plagiarism-report/<check_id>')
@login_required
def get_plagiarism_report_route(check_id):
    """Get plagiarism report from PlagiarismCheck.org API"""
    try:
        if not app.config['USE_PLAGIARISM_CHECK_API'] or not app.config['PLAGIARISM_CHECK_API_TOKEN']:
            return jsonify({
                'error': 'PlagiarismCheck.org API not configured',
                'status': 'error'
            }), 400
        
        # Get report from API
        report = get_plagiarism_report(check_id)
        
        if report:
            return jsonify({
                'report': report,
                'status': 'success'
            })
        else:
            return jsonify({
                'error': 'Failed to retrieve plagiarism report',
                'status': 'error'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving plagiarism report: {str(e)}',
            'status': 'error'
        }), 500

# Password Reset Routes
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
            # Remove any existing reset tokens for this user
            PasswordReset.query.filter_by(user_id=user.id).delete()
            
            # Create new reset token
            reset_token = PasswordReset(
                user_id=user.id,
                token=token,
                expires_at=expires_at
            )
            db.session.add(reset_token)
            db.session.commit()
            
            # Automatically redirect to reset page with the token
            return redirect(url_for('reset_password', token=token))
        else:
            flash('Email not found in our system', 'error')
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    reset_record = PasswordReset.query.filter_by(token=token, used=False).first()
    
    if not reset_record or reset_record.expires_at < datetime.utcnow():
        flash('Invalid or expired reset token', 'error')
        return redirect(url_for('forgot_password'))
    
    # Get user info for display
    user = User.query.get(reset_record.user_id)
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('reset_password.html', token=token, user=user)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('reset_password.html', token=token, user=user)
        
        # Update user password
        user.password_hash = generate_password_hash(password)
        
        # Mark token as used
        reset_record.used = True
        
        db.session.commit()
        
        flash('Password reset successfully! Please login with your new password.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token, user=user)

# Profile and Settings Routes
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    
    # Check if email is already taken by another user
    existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
    if existing_user:
        flash('Email already taken by another user', 'error')
        return redirect(url_for('profile'))
    
    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.email = email
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    
    if not check_password_hash(current_user.password_hash, current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('settings'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('settings'))
    
    if len(new_password) < 6:
        flash('New password must be at least 6 characters long', 'error')
        return redirect(url_for('settings'))
    
    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('settings'))

# Static Pages
@app.route('/help')
def help_center():
    return render_template('help_center.html')

@app.route('/contact')
def contact_us():
    return render_template('contact_us.html')

@app.route('/privacy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/terms')
def terms_of_service():
    return render_template('terms_of_service.html')

# API Routes
@app.route('/api/feedback/<int:grade_id>')
@login_required
def get_feedback(grade_id):
    """Get feedback details for a specific grade"""
    grade = Grade.query.get_or_404(grade_id)
    
    # Check if the current user is the student who received this grade
    if grade.submission.student_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # Calculate percentage
    percentage = (grade.marks / grade.submission.assignment.max_marks) * 100
    
    return jsonify({
        'success': True,
        'grade': {
            'marks': grade.marks,
            'max_marks': grade.submission.assignment.max_marks,
            'percentage': round(percentage, 1),
            'feedback': grade.feedback,
            'graded_at': grade.graded_at.strftime('%B %d, %Y at %I:%M %p'),
            'grader_name': f"{grade.grader.first_name} {grade.grader.last_name}"
        }
    })

# Admin User Management Routes
@app.route('/admin/users')
@login_required
def admin_users():
    """Admin user management page"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
def admin_create_user():
    """Create new user (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        is_active = 'is_active' in request.form
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('admin_create_user.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('admin_create_user.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {username} created successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin_create_user.html')

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    """Edit user (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.is_active = 'is_active' in request.form
        
        # Check for username conflicts
        existing_user = User.query.filter(User.username == user.username, User.id != user_id).first()
        if existing_user:
            flash('Username already taken', 'error')
            return render_template('admin_edit_user.html', user=user)
        
        # Check for email conflicts
        existing_email = User.query.filter(User.email == user.email, User.id != user_id).first()
        if existing_email:
            flash('Email already taken', 'error')
            return render_template('admin_edit_user.html', user=user)
        
        # Update password if provided
        new_password = request.form.get('password')
        if new_password:
            user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin_edit_user.html', user=user)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """Delete user (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting own account
    if user.id == current_user.id:
        flash('Cannot delete your own account', 'error')
        return redirect(url_for('admin_users'))
    
    # Delete user and related data
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.username} deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def admin_toggle_user_status(user_id):
    """Toggle user active status (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent deactivating own account
    if user.id == current_user.id:
        flash('Cannot deactivate your own account', 'error')
        return redirect(url_for('admin_users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} {status} successfully!', 'success')
    return redirect(url_for('admin_users'))

# System Settings Routes
@app.route('/admin/settings')
@login_required
def admin_settings():
    """System settings page (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get system statistics for settings overview
    total_users = User.query.count()
    total_assignments = Assignment.query.count()
    total_submissions = Submission.query.count()
    active_assignments = Assignment.query.filter_by(is_active=True).count()
    
    return render_template('admin_settings.html',
                         total_users=total_users,
                         total_assignments=total_assignments,
                         total_submissions=total_submissions,
                         active_assignments=active_assignments)

@app.route('/admin/settings/backup', methods=['POST'])
@login_required
def admin_backup_data():
    """Create system backup (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Create backup directory
        backup_dir = os.path.join(app.root_path, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'assignment_system_backup_{timestamp}.db'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        import shutil
        db_path = os.path.join(app.root_path, 'instance', 'assignment_system.db')
        shutil.copy2(db_path, backup_path)
        
        flash(f'Backup created successfully: {backup_filename}', 'success')
        
    except Exception as e:
        flash(f'Backup failed: {str(e)}', 'error')
    
    return redirect(url_for('admin_settings'))

@app.route('/admin/settings/cleanup', methods=['POST'])
@login_required
def admin_cleanup_data():
    """Clean up old data (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Clean up old notifications (older than 30 days)
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        old_notifications = Notification.query.filter(Notification.created_at < cutoff_date).all()
        
        for notification in old_notifications:
            db.session.delete(notification)
        
        # Clean up old password reset tokens (older than 1 day)
        old_tokens = PasswordReset.query.filter(PasswordReset.created_at < cutoff_date).all()
        
        for token in old_tokens:
            db.session.delete(token)
        
        db.session.commit()
        
        flash(f'Cleanup completed: Removed {len(old_notifications)} old notifications and {len(old_tokens)} expired tokens', 'success')
        
    except Exception as e:
        flash(f'Cleanup failed: {str(e)}', 'error')
    
    return redirect(url_for('admin_settings'))

@app.route('/admin/settings/export-data')
@login_required
def admin_export_data():
    """Export system data (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Get all data
        users = User.query.all()
        assignments = Assignment.query.all()
        submissions = Submission.query.all()
        grades = Grade.query.all()
        notifications = Notification.query.all()
        
        # Create export data
        export_data = {
            'users': [{
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'role': u.role,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'is_active': u.is_active,
                'created_at': u.created_at.isoformat()
            } for u in users],
            'assignments': [{
                'id': a.id,
                'title': a.title,
                'description': a.description,
                'due_date': a.due_date.isoformat(),
                'max_marks': a.max_marks,
                'created_by': a.created_by,
                'is_active': a.is_active,
                'created_at': a.created_at.isoformat()
            } for a in assignments],
            'submissions': [{
                'id': s.id,
                'assignment_id': s.assignment_id,
                'student_id': s.student_id,
                'file_name': s.file_name,
                'submitted_at': s.submitted_at.isoformat(),
                'is_late': s.is_late,
                'plagiarism_score': s.plagiarism_score
            } for s in submissions],
            'grades': [{
                'id': g.id,
                'submission_id': g.submission_id,
                'grader_id': g.grader_id,
                'marks': g.marks,
                'feedback': g.feedback,
                'graded_at': g.graded_at.isoformat()
            } for g in grades],
            'export_date': datetime.utcnow().isoformat(),
            'total_records': {
                'users': len(users),
                'assignments': len(assignments),
                'submissions': len(submissions),
                'grades': len(grades)
            }
        }
        
        # Create JSON response
        response = jsonify(export_data)
        response.headers['Content-Disposition'] = f'attachment; filename=assignment_system_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        return response
        
    except Exception as e:
        flash(f'Export failed: {str(e)}', 'error')
        return redirect(url_for('admin_settings'))

# Analytics and Reporting Routes
@app.route('/admin/analytics')
@login_required
def admin_analytics():
    """Advanced analytics dashboard (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get comprehensive analytics data
    total_users = User.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_lecturers = User.query.filter_by(role='lecturer').count()
    total_assignments = Assignment.query.count()
    total_submissions = Submission.query.count()
    total_grades = Grade.query.count()
    
    # Calculate submission rates
    active_assignments = Assignment.query.filter_by(is_active=True).count()
    submission_rate = (total_submissions / (total_students * active_assignments) * 100) if total_students and active_assignments else 0
    
    # Calculate average grades
    avg_grade = db.session.query(db.func.avg(Grade.marks)).scalar() or 0
    
    # Get recent activity
    recent_submissions = Submission.query.order_by(Submission.submitted_at.desc()).limit(10).all()
    recent_grades = Grade.query.order_by(Grade.graded_at.desc()).limit(10).all()
    
    # Get plagiarism statistics
    high_plagiarism = Submission.query.filter(Submission.plagiarism_score > 50).count()
    plagiarism_rate = (high_plagiarism / total_submissions * 100) if total_submissions else 0
    
    # Get late submission statistics
    late_submissions = Submission.query.filter_by(is_late=True).count()
    late_rate = (late_submissions / total_submissions * 100) if total_submissions else 0
    
    return render_template('admin_analytics.html',
                         total_users=total_users,
                         total_students=total_students,
                         total_lecturers=total_lecturers,
                         total_assignments=total_assignments,
                         total_submissions=total_submissions,
                         total_grades=total_grades,
                         submission_rate=round(submission_rate, 1),
                         avg_grade=round(avg_grade, 1),
                         recent_submissions=recent_submissions,
                         recent_grades=recent_grades,
                         high_plagiarism=high_plagiarism,
                         plagiarism_rate=round(plagiarism_rate, 1),
                         late_submissions=late_submissions,
                         late_rate=round(late_rate, 1))

@app.route('/admin/analytics/performance-report')
@login_required
def admin_performance_report():
    """Generate performance report (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Get performance data
        students = User.query.filter_by(role='student').all()
        performance_data = []
        
        for student in students:
            student_submissions = Submission.query.filter_by(student_id=student.id).all()
            student_grades = Grade.query.join(Submission).filter(Submission.student_id == student.id).all()
            
            total_marks = sum(grade.marks for grade in student_grades)
            max_possible = sum(grade.submission.assignment.max_marks for grade in student_grades)
            avg_percentage = (total_marks / max_possible * 100) if max_possible > 0 else 0
            
            performance_data.append({
                'student_name': f"{student.first_name} {student.last_name}",
                'username': student.username,
                'submissions_count': len(student_submissions),
                'grades_count': len(student_grades),
                'total_marks': total_marks,
                'max_possible': max_possible,
                'average_percentage': round(avg_percentage, 1),
                'late_submissions': len([s for s in student_submissions if s.is_late]),
                'high_plagiarism': len([s for s in student_submissions if s.plagiarism_score > 50])
            })
        
        # Sort by average percentage
        performance_data.sort(key=lambda x: x['average_percentage'], reverse=True)
        
        return render_template('admin_performance_report.html', 
                                     performance_data=performance_data,
                                     current_time=datetime.utcnow())
        
    except Exception as e:
        flash(f'Report generation failed: {str(e)}', 'error')
        return redirect(url_for('admin_analytics'))

@app.route('/admin/analytics/assignment-report')
@login_required
def admin_assignment_report():
    """Generate assignment report (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Get assignment data
        assignments = Assignment.query.all()
        assignment_data = []
        
        for assignment in assignments:
            submissions = Submission.query.filter_by(assignment_id=assignment.id).all()
            grades = Grade.query.join(Submission).filter(Submission.assignment_id == assignment.id).all()
            
            submission_rate = (len(submissions) / User.query.filter_by(role='student').count() * 100) if User.query.filter_by(role='student').count() > 0 else 0
            avg_grade = sum(grade.marks for grade in grades) / len(grades) if grades else 0
            late_rate = (len([s for s in submissions if s.is_late]) / len(submissions) * 100) if submissions else 0
            plagiarism_rate = (len([s for s in submissions if s.plagiarism_score > 50]) / len(submissions) * 100) if submissions else 0
            
            assignment_data.append({
                'assignment': assignment,
                'submissions_count': len(submissions),
                'grades_count': len(grades),
                'submission_rate': round(submission_rate, 1),
                'average_grade': round(avg_grade, 1),
                'late_rate': round(late_rate, 1),
                'plagiarism_rate': round(plagiarism_rate, 1)
            })
        
        return render_template('admin_assignment_report.html', 
                                     assignment_data=assignment_data,
                                     current_time=datetime.utcnow())
        
    except Exception as e:
        flash(f'Report generation failed: {str(e)}', 'error')
        return redirect(url_for('admin_analytics'))

# Initialize database when app is created (after all models and routes are defined)
initialize_database()

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
