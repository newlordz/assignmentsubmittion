#!/usr/bin/env python3
"""
Email Template Test - Generate static HTML files for preview
"""

import os
import re
from datetime import datetime, timedelta

def replace_url_for(content):
    """Replace url_for calls with static URLs for preview"""
    # Replace url_for calls with static URLs
    content = re.sub(
        r'\{\{\s*url_for\([\'"]([^\'"]+)[\'"][^}]*\)\s*\}\}',
        r'#\1',
        content
    )
    
    # Replace _external=True with full URLs
    content = re.sub(
        r'#dashboard',
        'https://your-university.edu/dashboard',
        content
    )
    content = re.sub(
        r'#submit_assignment',
        'https://your-university.edu/assignment/submit/1',
        content
    )
    content = re.sub(
        r'#grade_submission',
        'https://your-university.edu/submission/grade/1',
        content
    )
    content = re.sub(
        r'#student_dashboard',
        'https://your-university.edu/student/dashboard',
        content
    )
    
    return content

def test_email_template(template_name, **context):
    """Test an email template and save it as HTML file"""
    try:
        # Read the template file
        template_path = f'templates/emails/{template_name}'
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Replace url_for calls
        template_content = replace_url_for(template_content)
        
        # Simple template rendering (replace variables)
        rendered = template_content
        
        # Replace template variables
        for key, value in context.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    placeholder = f'{{{{ {key}.{sub_key} }}}}'
                    rendered = rendered.replace(placeholder, str(sub_value))
            else:
                placeholder = f'{{{{ {key} }}}}'
                rendered = rendered.replace(placeholder, str(value))
        
        # Handle datetime formatting
        rendered = re.sub(
            r'\{\{\s*([^}]+)\.strftime\([\'"]([^\'"]+)[\'"]\)\s*\}\}',
            lambda m: datetime.now().strftime(m.group(2)),
            rendered
        )
        
        # Handle length filters
        rendered = re.sub(
            r'\{\{\s*([^}]+)\|length\s*\}\}',
            '5',  # Mock length
            rendered
        )
        
        # Handle selectattr filters (simplified)
        rendered = re.sub(
            r'\{\{\s*[^}]+\|selectattr\([^}]+\|first\s*\}\}',
            'None',  # Mock no existing submission
            rendered
        )
        
        # Handle if statements (simplified)
        rendered = re.sub(
            r'\{%\s*if\s+([^%]+)\s*%\}',
            '<!-- if \\1 -->',
            rendered
        )
        rendered = re.sub(
            r'\{%\s*endif\s*%\}',
            '<!-- endif -->',
            rendered
        )
        rendered = re.sub(
            r'\{%\s*else\s*%\}',
            '<!-- else -->',
            rendered
        )
        
        # Handle for loops (simplified)
        rendered = re.sub(
            r'\{%\s*for\s+([^%]+)\s*%\}',
            '<!-- for \\1 -->',
            rendered
        )
        rendered = re.sub(
            r'\{%\s*endfor\s*%\}',
            '<!-- endfor -->',
            rendered
        )
        
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
    print("🧪 Email Template Test (Static Generation)")
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
    
    if success_count > 0:
        print("🎉 Email templates generated successfully!")
        print("\n📁 Generated files:")
        for template_name, _ in templates:
            output_file = f'email_preview_{template_name.replace(".html", "")}.html'
            if os.path.exists(output_file):
                print(f"   • {output_file}")
        print("\n💡 Open these HTML files in your browser to preview the emails!")
        print("🔗 The links in the emails are placeholder URLs for preview purposes.")
    else:
        print("⚠️ All templates failed. Check the error messages above.")

if __name__ == '__main__':
    main()
