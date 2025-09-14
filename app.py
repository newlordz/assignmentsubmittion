from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///assignment_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

def create_demo_assignments_and_submissions():
    """Create demo assignments and submissions"""
    try:
        # Get demo users
        lecturer1 = User.query.filter_by(username='lecturer1').first()
        lecturer2 = User.query.filter_by(username='lecturer2').first()
        students = User.query.filter_by(role='student').all()
        
        if not lecturer1 or not students:
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
                'created_by': lecturer1.id
            },
            {
                'title': 'Web Development Project',
                'description': 'Create a simple HTML/CSS website with at least 3 pages.',
                'instructions': 'Build a personal portfolio website with:\n1. Home page\n2. About page\n3. Contact page\n\nInclude CSS styling and make it responsive.',
                'due_date': datetime.utcnow() + timedelta(days=14),
                'max_marks': 150,
                'file_requirements': 'HTML, CSS files',
                'created_by': lecturer1.id
            },
            {
                'title': 'Database Design Assignment',
                'description': 'Design a database schema for a library management system.',
                'instructions': 'Create an ER diagram and SQL schema for:\n1. Books table\n2. Members table\n3. Borrowing records\n\nSubmit the SQL file and ER diagram.',
                'due_date': datetime.utcnow() + timedelta(days=10),
                'max_marks': 120,
                'file_requirements': 'SQL files, images',
                'created_by': lecturer2.id if lecturer2 else lecturer1.id
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    assignments_created = db.relationship('Assignment', backref='creator', lazy=True)
    submissions = db.relationship('Submission', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='grader', lazy=True)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    file_requirements = db.Column(db.String(200), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
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
initialize_database()

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

def calculate_plagiarism_score(content, other_submissions):
    """Calculate plagiarism score using TF-IDF and cosine similarity"""
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
        # Vectorize documents
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        # Return maximum similarity score
        return float(np.max(similarity_scores)) * 100
    except Exception as e:
        print(f"Error in plagiarism calculation: {e}")
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
        
        assignment = Assignment(
            title=title,
            description=description,
            instructions=instructions,
            due_date=due_date,
            max_marks=max_marks,
            file_requirements=file_requirements,
            created_by=current_user.id
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        # Send notifications to all students
        students = User.query.filter_by(role='student', is_active=True).all()
        for student in students:
            send_notification(
                student.id,
                f"New Assignment: {title}",
                f"A new assignment '{title}' has been created. Due date: {due_date.strftime('%Y-%m-%d %H:%M')}",
                'assignment'
            )
        
        flash('Assignment created successfully!', 'success')
        return redirect(url_for('lecturer_dashboard'))
    
    return render_template('create_assignment.html')

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
        send_notification(
            submission.student_id,
            f"Grade Received: {submission.assignment.title}",
            f"Your submission for '{submission.assignment.title}' has been graded. Marks: {marks}",
            'grade'
        )
        
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
        
        # Update submission record
        submission.plagiarism_score = plagiarism_score
        submission.plagiarism_report = f"Plagiarism score: {plagiarism_score:.2f}%"
        db.session.commit()
        
        return jsonify({
            'plagiarism_score': plagiarism_score,
            'report': submission.plagiarism_report,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Plagiarism check failed: {str(e)}',
            'plagiarism_score': 0.0,
            'report': 'Plagiarism check failed due to an error',
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

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
