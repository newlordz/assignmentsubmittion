#!/usr/bin/env python3
"""
Test the force plagiarism API
"""

import requests
import json

def test_force_api():
    """Test the force plagiarism API"""
    print("🧪 TESTING FORCE PLAGIARISM API")
    print("=" * 50)
    
    # Test with a submission ID (you'll need to replace this with an actual ID)
    submission_id = 15  # Replace with actual submission ID from your system
    
    url = f"http://127.0.0.1:5000/api/force-plagiarism-check/{submission_id}"
    
    print(f"🔗 Testing API: {url}")
    
    try:
        # Make POST request
        response = requests.post(url, json={'force': True, 'debug': True})
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response:")
            print(json.dumps(data, indent=2))
            
            if data.get('success'):
                results = data.get('results', {})
                score = results.get('overall_score', 0)
                debug_info = results.get('debug_info', {})
                
                print(f"\n🎯 FORCE PLAGIARISM RESULTS:")
                print(f"   Overall Score: {score}%")
                print(f"   Content Length: {debug_info.get('content_length', 0)} chars")
                print(f"   Other Submissions: {debug_info.get('other_submissions_count', 0)}")
                print(f"   File Type: {debug_info.get('file_type', 'unknown')}")
                
                if score > 70:
                    print("   🚨 HIGH PLAGIARISM DETECTED!")
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

def test_with_different_submission_ids():
    """Test with different submission IDs"""
    print("\n🔍 TESTING WITH DIFFERENT SUBMISSION IDs")
    print("=" * 50)
    
    # Test with multiple submission IDs
    submission_ids = [1, 2, 3, 4, 5, 10, 15, 20]  # Common submission IDs
    
    for submission_id in submission_ids:
        print(f"\n📋 Testing Submission ID: {submission_id}")
        
        url = f"http://127.0.0.1:5000/api/force-plagiarism-check/{submission_id}"
        
        try:
            response = requests.post(url, json={'force': True}, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    score = data.get('results', {}).get('overall_score', 0)
                    print(f"   ✅ Score: {score}%")
                else:
                    print(f"   ❌ Error: {data.get('error', 'Unknown')}")
            elif response.status_code == 404:
                print(f"   ⚠️  Submission not found")
            else:
                print(f"   ❌ HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Run all tests"""
    print("🚀 FORCE PLAGIARISM API TEST")
    print("=" * 70)
    print()
    
    # Test the API
    test_force_api()
    
    # Test with different IDs
    test_with_different_submission_ids()
    
    print("\n🎯 SUMMARY:")
    print("=" * 50)
    print("✅ Force plagiarism API tested")
    print("✅ Multiple submission IDs tested")
    print()
    print("💡 If the API works:")
    print("1. Add the force button to your grade page")
    print("2. Test it with real submissions")
    print("3. Compare results with normal plagiarism check")

if __name__ == "__main__":
    main()
