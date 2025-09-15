#!/usr/bin/env python3
"""
SendGrid Email Test Script
Test SendGrid email functionality
"""

import os
from app import app, send_email

def test_sendgrid():
    """Test SendGrid email sending"""
    print("🧪 Testing SendGrid Email Service")
    print("=" * 50)
    
    # Check configuration
    print("📧 SendGrid Configuration:")
    print(f"  Use SendGrid: {app.config.get('USE_SENDGRID', False)}")
    print(f"  API Key: {'✅ Set' if app.config.get('SENDGRID_API_KEY') else '❌ Not set'}")
    print(f"  From Email: {app.config.get('SENDGRID_FROM_EMAIL', 'Not set')}")
    print(f"  Suppress Send: {app.config.get('MAIL_SUPPRESS_SEND', False)}")
    print()
    
    # Test email data
    test_user = {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'email': 'test@example.com',
        'role': 'student'
    }
    
    # Test 1: Welcome Email
    print("🔍 Test 1: Welcome Email")
    try:
        result = send_email(
            to_email='your-email@gmail.com',  # Replace with your Gmail
            subject='Test Welcome Email from Assignment System',
            template='welcome.html',
            user=test_user
        )
        print(f"  Result: {'✅ Success' if result else '❌ Failed'}")
    except Exception as e:
        print(f"  Result: ❌ Error - {e}")
    print()
    
    # Test 2: Simple Test Email
    print("🔍 Test 2: Simple Test Email")
    try:
        result = send_email(
            to_email='your-email@gmail.com',  # Replace with your Gmail
            subject='Simple Test Email',
            template='welcome.html',
            user=test_user
        )
        print(f"  Result: {'✅ Success' if result else '❌ Failed'}")
    except Exception as e:
        print(f"  Result: ❌ Error - {e}")
    print()
    
    print("📊 Test Summary")
    print("=" * 50)
    
    if not app.config.get('USE_SENDGRID'):
        print("⚠️ SendGrid not enabled")
        print("   Set USE_SENDGRID=true to enable SendGrid")
    elif not app.config.get('SENDGRID_API_KEY'):
        print("⚠️ SendGrid API key not configured")
        print("   Set SENDGRID_API_KEY=SG.your-api-key-here")
    elif not app.config.get('SENDGRID_FROM_EMAIL'):
        print("⚠️ SendGrid from email not configured")
        print("   Set SENDGRID_FROM_EMAIL=your-verified-email@domain.com")
    else:
        print("✅ SendGrid is properly configured!")
        print("   Check your Gmail inbox for test emails")
    
    print()
    print("💡 Setup Instructions:")
    print("1. Sign up at https://sendgrid.com/")
    print("2. Get your API key from Settings → API Keys")
    print("3. Verify a sender email address")
    print("4. Set environment variables:")
    print("   USE_SENDGRID=true")
    print("   SENDGRID_API_KEY=SG.your-api-key-here")
    print("   SENDGRID_FROM_EMAIL=your-verified-email@domain.com")
    print("5. Replace 'your-email@gmail.com' in this script with your real Gmail")
    print("6. Run this test again")

if __name__ == '__main__':
    test_sendgrid()
