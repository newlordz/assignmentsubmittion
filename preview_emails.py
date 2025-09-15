#!/usr/bin/env python3
"""
Email Template Preview Script
View email templates in your browser
"""

from flask import Flask, render_template
from datetime import datetime, timedelta
import webbrowser
import os

# Create a simple Flask app for preview
app = Flask(__name__)
app.config['SECRET_KEY'] = 'preview'

# Mock data for preview
mock_user = {
    'first_name': 'John',
    'last_name': 'Doe',
    'username': 'johndoe',
    'email': 'john.doe@university.edu',
    'role': 'student'
}

mock_assignment = {
    'id': 1,
    'title': 'Introduction to Programming',
    'description': 'Write a simple Python program that calculates the factorial of a number.',
    'instructions': 'Create a Python script that:\n1. Takes a number as input\n2. Calculates its factorial\n3. Displays the result\n\nSubmit your .py file.',
    'due_date': datetime.now() + timedelta(days=7),
    'max_marks': 100,
    'file_requirements': 'Python files (.py)'
}

mock_submission = {
    'id': 1,
    'file_name': 'factorial.py',
    'file_size': 1024,
    'submitted_at': datetime.now(),
    'is_late': False,
    'assignment': mock_assignment,
    'student': mock_user
}

mock_grade = {
    'marks': 85,
    'feedback': 'Great work! Your code is well-structured and handles edge cases properly.',
    'graded_at': datetime.now(),
    'assignment': mock_assignment
}

@app.route('/')
def index():
    return '''
    <h1>Email Template Preview</h1>
    <ul>
        <li><a href="/welcome">Welcome Email</a></li>
        <li><a href="/new-assignment">New Assignment Email</a></li>
        <li><a href="/new-submission">New Submission Email</a></li>
        <li><a href="/grade-notification">Grade Notification Email</a></li>
        <li><a href="/deadline-reminder">Deadline Reminder Email</a></li>
    </ul>
    '''

# Add dummy routes for url_for to work
@app.route('/dashboard')
def dashboard():
    return "Dashboard"

@app.route('/assignment/submit/<int:assignment_id>')
def submit_assignment(assignment_id):
    return f"Submit Assignment {assignment_id}"

@app.route('/submission/grade/<int:submission_id>')
def grade_submission(submission_id):
    return f"Grade Submission {submission_id}"

@app.route('/student/dashboard')
def student_dashboard():
    return "Student Dashboard"

@app.route('/welcome')
def welcome():
    return render_template('emails/welcome.html', user=mock_user)

@app.route('/new-assignment')
def new_assignment():
    return render_template('emails/new_assignment.html', 
                         student=mock_user, 
                         assignment=mock_assignment)

@app.route('/new-submission')
def new_submission():
    lecturer = {
        'first_name': 'Dr. Smith',
        'last_name': 'Professor',
        'email': 'dr.smith@university.edu'
    }
    return render_template('emails/new_submission.html',
                         lecturer=lecturer,
                         submission=mock_submission,
                         student=mock_user,
                         assignment=mock_assignment)

@app.route('/grade-notification')
def grade_notification():
    return render_template('emails/grade_notification.html',
                         student=mock_user,
                         grade=mock_grade,
                         assignment=mock_assignment)

@app.route('/deadline-reminder')
def deadline_reminder():
    return render_template('emails/deadline_reminder.html',
                         student=mock_user,
                         assignment=mock_assignment)

if __name__ == '__main__':
    print("🌐 Starting Email Preview Server...")
    print("📧 Open your browser and go to: http://localhost:5001")
    print("🔍 Preview all email templates before sending")
    
    # Open browser automatically
    webbrowser.open('http://localhost:5001')
    
    app.run(host='localhost', port=5001, debug=True)
