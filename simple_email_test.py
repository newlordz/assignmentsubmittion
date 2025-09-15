#!/usr/bin/env python3
"""
Simple Email Test - Test email templates without web server
"""

import os
from datetime import datetime, timedelta
from flask import Flask, render_template_string

# Create a simple Flask app just for template rendering
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

def test_email_template(template_name, **context):
    """Test an email template and save it as HTML file"""
    try:
        with app.app_context():
            # Read the template file
            template_path = f'templates/emails/{template_name}'
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Render the template
            rendered = render_template_string(template_content, **context)
            
            # Save to output file
            output_file = f'email_preview_{template_name.replace(".html", "")}.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(rendered)
            
            print(f"✅ {template_name} rendered successfully → {output_file}")
            return True
            
    except Exception as e:
        print(f"❌ {template_name} failed: {e}")
        return False

def main():
    print("🧪 Simple Email Template Test")
    print("=" * 50)
    
    # Mock data
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
    
    lecturer = {
        'first_name': 'Dr. Smith',
        'last_name': 'Professor',
        'email': 'dr.smith@university.edu'
    }
    
    # Test all templates
    templates = [
        ('welcome.html', {'user': mock_user}),
        ('new_assignment.html', {'student': mock_user, 'assignment': mock_assignment}),
        ('new_submission.html', {
            'lecturer': lecturer,
            'submission': mock_submission,
            'student': mock_user,
            'assignment': mock_assignment
        }),
        ('grade_notification.html', {
            'student': mock_user,
            'grade': mock_grade,
            'assignment': mock_assignment
        }),
        ('deadline_reminder.html', {
            'student': mock_user,
            'assignment': mock_assignment
        })
    ]
    
    success_count = 0
    for template_name, context in templates:
        if test_email_template(template_name, **context):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {success_count}/{len(templates)} templates rendered successfully")
    
    if success_count == len(templates):
        print("🎉 All email templates are working correctly!")
        print("\n📁 Generated files:")
        for template_name, _ in templates:
            output_file = f'email_preview_{template_name.replace(".html", "")}.html'
            print(f"   • {output_file}")
        print("\n💡 Open these HTML files in your browser to preview the emails!")
    else:
        print("⚠️ Some templates failed. Check the error messages above.")

if __name__ == '__main__':
    main()
