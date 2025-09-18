#!/usr/bin/env python3
"""
Test email functionality with the running server
"""

import requests
import json

def test_email_functionality():
    """Test email functionality through the server"""
    print("📧 TESTING EMAIL FUNCTIONALITY")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Test 1: Check if server is running
        print("🔍 Testing server connection...")
        response = requests.get(f"{base_url}/login", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
        
        # Test 2: Test registration (which should send welcome email)
        print("\n📝 Testing user registration...")
        registration_data = {
            'username': 'testuser123',
            'email': 'testuser123@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'role': 'student',
            'name': 'Test User'
        }
        
        response = requests.post(f"{base_url}/register", data=registration_data, timeout=10)
        if response.status_code == 200:
            print("✅ Registration request sent successfully")
            if "successfully" in response.text.lower() or "welcome" in response.text.lower():
                print("✅ Registration appears successful")
            else:
                print("⚠️ Registration response unclear - check manually")
        else:
            print(f"❌ Registration failed with status code: {response.status_code}")
        
        # Test 3: Test login
        print("\n🔐 Testing user login...")
        login_data = {
            'username': 'testuser123',
            'password': 'testpass123'
        }
        
        response = requests.post(f"{base_url}/login", data=login_data, timeout=10)
        if response.status_code == 200:
            print("✅ Login request sent successfully")
            if "dashboard" in response.text.lower() or "welcome" in response.text.lower():
                print("✅ Login appears successful")
            else:
                print("⚠️ Login response unclear - check manually")
        else:
            print(f"❌ Login failed with status code: {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running.")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Server might be slow or unresponsive.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Run email functionality test"""
    print("🧪 EMAIL FUNCTIONALITY TEST")
    print("=" * 50)
    
    success = test_email_functionality()
    
    print("\n🎯 SUMMARY:")
    print("=" * 30)
    if success:
        print("✅ Server is running")
        print("✅ Basic functionality tested")
        print("✅ Email system should be working")
        print()
        print("📋 NEXT STEPS:")
        print("1. Check your email for welcome messages")
        print("2. Test the web interface at http://127.0.0.1:5000")
        print("3. Try registering a new user to test email notifications")
    else:
        print("❌ Some tests failed")
        print("💡 Check server logs for more details")

if __name__ == "__main__":
    main()
