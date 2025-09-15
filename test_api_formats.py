#!/usr/bin/env python3
"""
Test different API parameter formats for PlagiarismCheck.org
"""

import requests
import json

def test_api_formats():
    """Test different API parameter formats"""
    print("🔍 Testing Different API Parameter Formats")
    print("=" * 60)
    
    api_token = "nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4"
    test_content = "This is a test document for plagiarism detection."
    author_email = "enochessel5@gmail.com"
    
    # Test different parameter formats
    test_cases = [
        {
            "name": "Original Format (group_token)",
            "data": {
                'group_token': api_token,
                'author': author_email,
                'text': test_content
            }
        },
        {
            "name": "Alternative Format (token)",
            "data": {
                'token': api_token,
                'author': author_email,
                'text': test_content
            }
        },
        {
            "name": "API Key Format (api_key)",
            "data": {
                'api_key': api_token,
                'author': author_email,
                'text': test_content
            }
        },
        {
            "name": "Authorization Header",
            "headers": {
                'Authorization': f'Bearer {api_token}',
                'Content-Type': 'application/json'
            },
            "data": {
                'author': author_email,
                'text': test_content
            }
        },
        {
            "name": "JSON Format",
            "headers": {
                'Content-Type': 'application/json'
            },
            "data": json.dumps({
                'group_token': api_token,
                'author': author_email,
                'text': test_content
            })
        }
    ]
    
    base_url = "https://plagiarismcheck.org/api/org/text/check/"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Prepare request
            headers = test_case.get('headers', {})
            data = test_case.get('data', {})
            
            # Make request
            response = requests.post(
                base_url,
                data=data,
                headers=headers,
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ SUCCESS! This format works!")
                result = response.json()
                if 'check_id' in result:
                    print(f"Check ID: {result['check_id']}")
                break
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("📋 Summary:")
    print("If none of the formats worked, the token might need to be:")
    print("1. Activated by PlagiarismCheck.org support")
    print("2. Used with a different API endpoint")
    print("3. Associated with a specific account/email")

if __name__ == "__main__":
    test_api_formats()
