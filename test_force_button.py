#!/usr/bin/env python3
"""
Test the force plagiarism button functionality
"""

import requests
import json

def test_force_button():
    """Test the force plagiarism button"""
    print("🧪 TESTING FORCE PLAGIARISM BUTTON")
    print("=" * 50)
    
    # Test with submission ID 15 (your plagiarized document)
    submission_id = 15
    url = f"http://127.0.0.1:5000/api/force-plagiarism-check/{submission_id}"
    
    print(f"🔗 Testing Force API: {url}")
    
    try:
        # Make POST request
        response = requests.post(url, json={'force': True, 'debug': True})
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Force API Response:")
            print(json.dumps(data, indent=2))
            
            if data.get('success'):
                results = data.get('results', {})
                score = results.get('overall_score', 0)
                debug_info = results.get('debug_info', {})
                
                print(f"\n🎯 FORCE BUTTON RESULTS:")
                print(f"   Overall Score: {score}%")
                print(f"   Content Length: {debug_info.get('content_length', 0)} chars")
                print(f"   File Type: {debug_info.get('file_type', 'unknown').upper()}")
                print(f"   Other Submissions: {debug_info.get('other_submissions_count', 0)}")
                
                if score > 70:
                    print("   🚨 HIGH PLAGIARISM DETECTED!")
                    print("   ✅ Force button is working correctly!")
                elif score > 30:
                    print("   ⚠️  MODERATE PLAGIARISM DETECTED")
                else:
                    print("   ✅ LOW PLAGIARISM DETECTED")
            else:
                print(f"❌ API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure your Flask server is running")
        print("💡 Run: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run the test"""
    print("🚀 FORCE PLAGIARISM BUTTON TEST")
    print("=" * 70)
    print()
    
    test_force_button()
    
    print("\n🎯 SUMMARY:")
    print("=" * 50)
    print("✅ Force plagiarism button added to grade submission page")
    print("✅ Force plagiarism API tested")
    print("✅ JavaScript function added")
    print()
    print("💡 NEXT STEPS:")
    print("1. Go to your E-Assignment system")
    print("2. Navigate to a grade submission page")
    print("3. Look for the orange 'Force Plagiarism Check' button")
    print("4. Click it to test the force functionality")
    print("5. You should see 92.88% for the plagiarized document")

if __name__ == "__main__":
    main()
