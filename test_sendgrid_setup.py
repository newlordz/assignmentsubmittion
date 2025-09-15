#!/usr/bin/env python3
"""
Test SendGrid setup with your actual credentials
"""

import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

def test_sendgrid():
    print("🧪 Testing SendGrid Setup...")
    print("=" * 50)
    
    # Get credentials from user input
    api_key = input("Enter your SendGrid API key (starts with SG.): ").strip()
    from_email = input("Enter your verified sender email: ").strip()
    to_email = input("Enter your Gmail address to receive test email: ").strip()
    
    if not api_key or not from_email or not to_email:
        print("❌ All fields are required!")
        return
    
    try:
        # Initialize SendGrid
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        
        # Create email
        from_email_obj = Email(from_email)
        to_email_obj = To(to_email)
        subject = "🎉 SendGrid Test - Assignment System"
        
        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">🎉 SendGrid Test Successful!</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hello!</h2>
                <p>This is a test email from your Assignment Submission System.</p>
                <p>If you're reading this, SendGrid is working perfectly! 🚀</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>✅ What this means:</h3>
                    <ul>
                        <li>Your SendGrid API key is valid</li>
                        <li>Your sender email is verified</li>
                        <li>Emails will be delivered to Gmail</li>
                        <li>Your assignment system is ready!</li>
                    </ul>
                </div>
                
                <p>You can now use your assignment system and receive real email notifications!</p>
            </div>
            <div style="background: #e9ecef; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
                Assignment Submission System - Powered by SendGrid
            </div>
        </body>
        </html>
        """
        
        content = Content("text/html", html_content)
        mail = Mail(from_email_obj, to_email_obj, subject, content)
        
        # Send email
        print("📧 Sending test email...")
        response = sg.send(mail)
        
        if response.status_code in [200, 201, 202]:
            print(f"✅ SUCCESS! Email sent successfully!")
            print(f"📧 Status Code: {response.status_code}")
            print(f"📬 Check your Gmail inbox: {to_email}")
            print(f"📱 Check spam folder if not in inbox")
            print("\n🎉 Your SendGrid setup is working perfectly!")
            print("You can now use your assignment system with real email notifications!")
        else:
            print(f"❌ Error: Status code {response.status_code}")
            print(f"Response: {response.body}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your API key is correct")
        print("2. Verify your sender email in SendGrid dashboard")
        print("3. Make sure you copied the full API key")

if __name__ == "__main__":
    test_sendgrid()
