#!/usr/bin/env python3
"""
Test demo login by making actual HTTP requests
"""

import requests
import sys

def test_demo_login():
    """Test demo login with actual HTTP requests"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 Testing demo login with HTTP requests...")
    
    # Test 1: Access demo login page
    try:
        response = requests.get(f"{base_url}/demo-login")
        print(f"✅ Demo login page: {response.status_code}")
    except Exception as e:
        print(f"❌ Demo login page error: {e}")
        return
    
    # Test 2: Test student login
    try:
        login_data = {
            'username': 'student1',
            'password': 'student123'
        }
        response = requests.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"✅ Student login: {response.status_code}")
        if response.status_code == 302:
            print(f"  Redirect to: {response.headers.get('Location', 'Unknown')}")
    except Exception as e:
        print(f"❌ Student login error: {e}")
    
    # Test 3: Test lecturer login
    try:
        login_data = {
            'username': 'lecturer1',
            'password': 'lecturer123'
        }
        response = requests.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"✅ Lecturer login: {response.status_code}")
        if response.status_code == 302:
            print(f"  Redirect to: {response.headers.get('Location', 'Unknown')}")
    except Exception as e:
        print(f"❌ Lecturer login error: {e}")
    
    # Test 4: Test admin login
    try:
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = requests.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"✅ Admin login: {response.status_code}")
        if response.status_code == 302:
            print(f"  Redirect to: {response.headers.get('Location', 'Unknown')}")
    except Exception as e:
        print(f"❌ Admin login error: {e}")
    
    # Test 5: Test dashboard access (this might fail without session)
    try:
        response = requests.get(f"{base_url}/dashboard")
        print(f"✅ Dashboard access: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard access error: {e}")

def main():
    """Main function"""
    print("🚀 Testing Demo Login with HTTP Requests")
    print("=" * 50)
    
    try:
        test_demo_login()
        print("\n🎉 HTTP request test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
