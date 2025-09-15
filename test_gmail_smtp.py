#!/usr/bin/env python3
"""
Test Gmail SMTP setup - Completely FREE!
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail_smtp():
    print("📧 Testing Gmail SMTP Setup...")
    print("=" * 50)
    print("✅ This is completely FREE - no payment required!")
    print()
    
    # Get credentials from user
    gmail_address = input("Enter your Gmail address: ").strip()
    app_password = input("Enter your Gmail App Password (16 characters): ").strip()
    recipient_email = input("Enter recipient email (your Gmail or any email): ").strip()
    
    if not gmail_address or not app_password or not recipient_email:
        print("❌ All fields are required!")
        return
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🎉 Gmail SMTP Test - Assignment System"
        msg['From'] = gmail_address
        msg['To'] = recipient_email
        
        # HTML content
        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #4285f4 0%, #34a853 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">🎉 Gmail SMTP Test Successful!</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hello!</h2>
                <p>This is a test email from your Assignment Submission System using <strong>Gmail SMTP</strong>.</p>
                <p>If you're reading this, your email setup is working perfectly! 🚀</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>✅ What this means:</h3>
                    <ul>
                        <li>Gmail SMTP is configured correctly</li>
                        <li>Your App Password is working</li>
                        <li>Emails will be delivered reliably</li>
                        <li>Your assignment system is ready!</li>
                        <li><strong>This is completely FREE!</strong></li>
                    </ul>
                </div>
                
                <p>You can now use your assignment system and receive real email notifications!</p>
                
                <div style="background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>💰 Cost: $0.00</h3>
                    <p>Gmail SMTP is completely free for personal use!</p>
                </div>
            </div>
            <div style="background: #e9ecef; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
                Assignment Submission System - Powered by Gmail SMTP (FREE)
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to Gmail SMTP
        print("📧 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("🔐 Authenticating...")
        server.login(gmail_address, app_password)
        
        print("📤 Sending email...")
        server.send_message(msg)
        server.quit()
        
        print("✅ SUCCESS! Email sent successfully!")
        print(f"📬 Check your inbox: {recipient_email}")
        print(f"📱 Check spam folder if not in inbox")
        print("\n🎉 Your Gmail SMTP setup is working perfectly!")
        print("💰 Cost: $0.00 - Completely FREE!")
        print("You can now use your assignment system with real email notifications!")
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed!")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're using an App Password, not your regular Gmail password")
        print("2. Ensure 2-Factor Authentication is enabled on your Gmail")
        print("3. Generate a new App Password if needed")
        print("4. Check that your Gmail address is correct")
        
    except smtplib.SMTPRecipientsRefused:
        print("❌ Recipient email address is invalid!")
        print("Please check the email address and try again.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify Gmail SMTP settings")
        print("3. Make sure your App Password is correct")

if __name__ == "__main__":
    test_gmail_smtp()
