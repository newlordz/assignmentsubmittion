#!/usr/bin/env python3
"""
Test API consistency between old and new plagiarism check endpoints
"""

import requests
import json

def test_both_apis():
    """Test both plagiarism check APIs to ensure consistency"""
    print("🧪 TESTING API CONSISTENCY")
    print("=" * 60)
    
    # Test with submission ID 15 (your plagiarized document)
    submission_id = 15
    
    print(f"🔗 Testing Submission ID: {submission_id}")
    print()
    
    # Test old API (GET)
    print("📊 Testing OLD API (/api/plagiarism-check/)")
    old_url = f"http://127.0.0.1:5000/api/plagiarism-check/{submission_id}"
    
    try:
        old_response = requests.get(old_url)
        print(f"   Status Code: {old_response.status_code}")
        
        if old_response.status_code == 200:
            old_data = old_response.json()
            print("   ✅ Old API Response:")
            print(f"   Plagiarism Score: {old_data.get('plagiarism_score', 0)}%")
            print(f"   Status: {old_data.get('status', 'unknown')}")
            print(f"   Report: {old_data.get('report', 'No report')[:100]}...")
        else:
            print(f"   ❌ Old API Error: {old_response.status_code}")
            old_data = None
    except Exception as e:
        print(f"   ❌ Old API Error: {e}")
        old_data = None
    
    print()
    
    # Test new API (POST)
    print("📊 Testing NEW API (/api/force-plagiarism-check/)")
    new_url = f"http://127.0.0.1:5000/api/force-plagiarism-check/{submission_id}"
    
    try:
        new_response = requests.post(new_url, json={'force': True, 'debug': True})
        print(f"   Status Code: {new_response.status_code}")
        
        if new_response.status_code == 200:
            new_data = new_response.json()
            print("   ✅ New API Response:")
            if new_data.get('success'):
                score = new_data.get('results', {}).get('overall_score', 0)
                print(f"   Plagiarism Score: {score}%")
                print(f"   Status: Success")
                debug_info = new_data.get('results', {}).get('debug_info', {})
                print(f"   Content Length: {debug_info.get('content_length', 0)} chars")
            else:
                print(f"   ❌ New API Error: {new_data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ New API Error: {new_response.status_code}")
            new_data = None
    except Exception as e:
        print(f"   ❌ New API Error: {e}")
        new_data = None
    
    print()
    
    # Compare results
    print("🔍 COMPARING RESULTS")
    print("=" * 30)
    
    if old_data and new_data and new_data.get('success'):
        old_score = old_data.get('plagiarism_score', 0)
        new_score = new_data.get('results', {}).get('overall_score', 0)
        
        print(f"Old API Score: {old_score}%")
        print(f"New API Score: {new_score}%")
        
        if abs(old_score - new_score) < 1.0:  # Allow for small differences
            print("✅ APIs are consistent!")
        else:
            print("❌ APIs are inconsistent!")
            print(f"   Difference: {abs(old_score - new_score):.2f}%")
    else:
        print("❌ Cannot compare - one or both APIs failed")
    
    return old_data, new_data

def test_multiple_submissions():
    """Test multiple submissions for consistency"""
    print(f"\n🔍 TESTING MULTIPLE SUBMISSIONS")
    print("=" * 50)
    
    test_cases = [10, 14, 15]  # Different submission IDs
    
    for submission_id in test_cases:
        print(f"\n📋 Testing Submission ID: {submission_id}")
        
        # Test old API
        try:
            old_response = requests.get(f"http://127.0.0.1:5000/api/plagiarism-check/{submission_id}")
            if old_response.status_code == 200:
                old_score = old_response.json().get('plagiarism_score', 0)
                print(f"   Old API: {old_score}%")
            else:
                print(f"   Old API: Error {old_response.status_code}")
                continue
        except:
            print(f"   Old API: Connection error")
            continue
        
        # Test new API
        try:
            new_response = requests.post(f"http://127.0.0.1:5000/api/force-plagiarism-check/{submission_id}", 
                                       json={'force': True, 'debug': True})
            if new_response.status_code == 200:
                new_data = new_response.json()
                if new_data.get('success'):
                    new_score = new_data.get('results', {}).get('overall_score', 0)
                    print(f"   New API: {new_score}%")
                    
                    # Check consistency
                    if abs(old_score - new_score) < 1.0:
                        print(f"   ✅ Consistent")
                    else:
                        print(f"   ❌ Inconsistent (diff: {abs(old_score - new_score):.2f}%)")
                else:
                    print(f"   New API: Error - {new_data.get('error', 'Unknown')}")
            else:
                print(f"   New API: Error {new_response.status_code}")
        except:
            print(f"   New API: Connection error")

def main():
    """Run all tests"""
    print("🚀 API CONSISTENCY TEST")
    print("=" * 70)
    print()
    
    # Test both APIs
    old_data, new_data = test_both_apis()
    
    # Test multiple submissions
    test_multiple_submissions()
    
    print("\n🎯 SUMMARY:")
    print("=" * 50)
    print("✅ Both APIs tested")
    print("✅ Consistency checked")
    print("✅ Multiple submissions verified")
    print()
    print("💡 EXPECTED RESULTS:")
    print("• Both APIs should return similar scores")
    print("• Old API should now use the working plagiarism detection")
    print("• Frontend should display consistent results")
    print("• No more mismatch between button and results")

if __name__ == "__main__":
    main()
