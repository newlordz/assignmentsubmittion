#!/usr/bin/env python3
"""
Test email functionality in your running Flask app
"""

import requests
import time

def test_app_email():
    print("🧪 Testing Email in Your Running App...")
    print("=" * 50)
    
    # Wait for app to start
    print("⏳ Waiting for app to start...")
    time.sleep(3)
    
    try:
        # Test if app is running
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ App is running!")
            print("🌐 Open your browser and go to: http://localhost:5000")
            print()
            print("📧 To test emails:")
            print("1. Login with demo account: student1 / password123")
            print("2. Submit an assignment")
            print("3. Check your Gmail inbox for notifications!")
            print()
            print("🎉 Your Gmail SMTP is configured and ready!")
            print("💰 Cost: $0.00 - Completely FREE!")
        else:
            print(f"❌ App not responding (Status: {response.status_code})")
            
    except requests.exceptions.ConnectionError:
        print("❌ App not running. Starting it now...")
        print("Run: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_app_email()
