#!/usr/bin/env python3
"""
Email Service Test Script
Test the email functionality of the E-Assignment Submission System
"""

import os
from datetime import datetime, timedelta
from app import app, db, User, Assignment, Submission, send_email, send_welcome_email

def test_email_service():
    """Test the email service functionality"""
    print("🧪 Testing Email Service")
    print("=" * 50)
    
    with app.app_context():
        # Check email configuration
        print("📧 Email Configuration:")
        print(f"  Server: {app.config.get('MAIL_SERVER', 'Not set')}")
        print(f"  Port: {app.config.get('MAIL_PORT', 'Not set')}")
        print(f"  TLS: {app.config.get('MAIL_USE_TLS', 'Not set')}")
        print(f"  Username: {app.config.get('MAIL_USERNAME', 'Not set')}")
        print(f"  Suppress Send: {app.config.get('MAIL_SUPPRESS_SEND', 'Not set')}")
        print()
        
        # Test 1: Basic email sending
        print("🔍 Test 1: Basic Email Sending")
        try:
            result = send_email(
                to_email='test@example.com',
                subject='Test Email from E-Assignment System',
                template='welcome.html',
                user={'first_name': 'Test', 'last_name': 'User', 'username': 'testuser', 'email': 'test@example.com', 'role': 'student'}
            )
            print(f"  Result: {'✅ Success' if result else '❌ Failed'}")
        except Exception as e:
            print(f"  Result: ❌ Error - {e}")
        print()
        
        # Test 2: Welcome email
        print("🔍 Test 2: Welcome Email")
        try:
            # Create a test user
            test_user = User(
                username='email_test_user',
                email='test@example.com',
                password_hash='test_hash',
                role='student',
                first_name='Email',
                last_name='Test',
                is_active=True
            )
            
            result = send_welcome_email(test_user)
            print(f"  Result: {'✅ Success' if result else '❌ Failed'}")
            
            # Clean up
            db.session.rollback()
        except Exception as e:
            print(f"  Result: ❌ Error - {e}")
        print()
        
        # Test 3: Assignment notification
        print("🔍 Test 3: Assignment Notification")
        try:
            # Create test data
            lecturer = User.query.filter_by(role='lecturer').first()
            students = User.query.filter_by(role='student').limit(2).all()
            
            if lecturer and students:
                test_assignment = Assignment(
                    title='Email Test Assignment',
                    description='This is a test assignment for email notifications',
                    instructions='Submit your test file',
                    due_date=datetime.utcnow() + timedelta(days=7),
                    max_marks=100,
                    file_requirements='Any file type',
                    created_by=lecturer.id
                )
                
                from app import send_assignment_notification
                result = send_assignment_notification(test_assignment, students)
                print(f"  Result: {'✅ Success' if result else '❌ Failed'}")
            else:
                print("  Result: ⚠️ Skipped - No test users found")
        except Exception as e:
            print(f"  Result: ❌ Error - {e}")
        print()
        
        # Test 4: Grade notification
        print("🔍 Test 4: Grade Notification")
        try:
            student = User.query.filter_by(role='student').first()
            assignment = Assignment.query.first()
            
            if student and assignment:
                from app import send_grade_notification
                from app import Grade
                
                # Create a test grade
                test_grade = Grade(
                    submission_id=1,  # Dummy ID
                    grader_id=1,      # Dummy ID
                    marks=85,
                    feedback='Great work!',
                    graded_at=datetime.utcnow()
                )
                
                # Mock the assignment relationship
                test_grade.assignment = assignment
                
                result = send_grade_notification(test_grade)
                print(f"  Result: {'✅ Success' if result else '❌ Failed'}")
            else:
                print("  Result: ⚠️ Skipped - No test data found")
        except Exception as e:
            print(f"  Result: ❌ Error - {e}")
        print()
        
        # Test 5: Deadline reminder
        print("🔍 Test 5: Deadline Reminder")
        try:
            assignment = Assignment.query.first()
            students = User.query.filter_by(role='student').limit(2).all()
            
            if assignment and students:
                from app import send_deadline_reminder
                result = send_deadline_reminder(assignment, students)
                print(f"  Result: {'✅ Success' if result else '❌ Failed'}")
            else:
                print("  Result: ⚠️ Skipped - No test data found")
        except Exception as e:
            print(f"  Result: ❌ Error - {e}")
        print()
        
        # Summary
        print("📊 Email Service Test Summary")
        print("=" * 50)
        
        if app.config.get('MAIL_SUPPRESS_SEND'):
            print("ℹ️ Email sending is suppressed (MAIL_SUPPRESS_SEND=true)")
            print("   Emails are being logged instead of sent")
        elif not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
            print("⚠️ Email credentials not configured")
            print("   Set MAIL_USERNAME and MAIL_PASSWORD environment variables")
        else:
            print("✅ Email service is configured and ready")
            print("   Check your email inbox for test messages")
        
        print()
        print("💡 Tips:")
        print("   - Set MAIL_SUPPRESS_SEND=true for testing without sending emails")
        print("   - Check application logs for detailed email status")
        print("   - Verify SMTP settings with your email provider")
        print("   - Use app passwords for Gmail accounts with 2FA enabled")

if __name__ == '__main__':
    test_email_service()
