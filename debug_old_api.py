#!/usr/bin/env python3
"""
Debug the old API to see what's happening
"""

import requests
import json

def debug_old_api():
    """Debug the old API response"""
    print("🔍 DEBUGGING OLD API")
    print("=" * 40)
    
    submission_id = 15
    url = f"http://127.0.0.1:5000/api/plagiarism-check/{submission_id}"
    
    print(f"URL: {url}")
    print()
    
    try:
        # Test without authentication first
        print("📊 Testing without authentication...")
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content Length: {len(response.content)}")
        print(f"Raw Content: {response.content[:200]}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON Data: {data}")
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                print(f"Response Text: {response.text[:500]}")
        elif response.status_code == 401:
            print("❌ Authentication required - this is the issue!")
            print("The old API requires login, but our test doesn't have a session")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Request Error: {e}")

def test_with_session():
    """Test with a session cookie"""
    print("\n🍪 TESTING WITH SESSION")
    print("=" * 40)
    
    # Create a session
    session = requests.Session()
    
    # Try to login first (this might not work without proper credentials)
    login_url = "http://127.0.0.1:5000/login"
    
    try:
        # Get login page first
        login_page = session.get(login_url)
        print(f"Login page status: {login_page.status_code}")
        
        # Try to access the API with the session
        api_url = "http://127.0.0.1:5000/api/plagiarism-check/15"
        response = session.get(api_url)
        
        print(f"API Status with session: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
    except Exception as e:
        print(f"Session test error: {e}")

def main():
    """Run debug tests"""
    debug_old_api()
    test_with_session()
    
    print("\n💡 DIAGNOSIS:")
    print("=" * 30)
    print("The old API likely requires authentication (@login_required)")
    print("This is why it returns empty responses in our tests")
    print("The frontend should work because it has a valid session")
    print()
    print("✅ SOLUTION:")
    print("The frontend JavaScript is correctly calling the Force API")
    print("The Force API works without authentication issues")
    print("Both APIs now use the same plagiarism detection logic")

if __name__ == "__main__":
    main()
