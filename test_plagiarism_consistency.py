#!/usr/bin/env python3
"""
Test plagiarism consistency between old and new APIs
"""

import requests
import json
import time

def test_plagiarism_consistency():
    """Test that both APIs return consistent results"""
    print("🧪 TESTING PLAGIARISM CONSISTENCY")
    print("=" * 60)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Test with submission ID 15 (your plagiarized document)
    submission_id = 15
    
    print(f"🔗 Testing Submission ID: {submission_id}")
    print()
    
    # Test old API (GET)
    print("📊 Testing OLD API (/api/plagiarism-check/)")
    old_url = f"http://127.0.0.1:5000/api/plagiarism-check/{submission_id}"
    
    try:
        old_response = requests.get(old_url, timeout=10)
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
        new_response = requests.post(new_url, json={'force': True, 'debug': True}, timeout=10)
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
            print("✅ Plagiarism reports should now match!")
        else:
            print("❌ APIs are still inconsistent!")
            print(f"   Difference: {abs(old_score - new_score):.2f}%")
    else:
        print("❌ Cannot compare - one or both APIs failed")
        if not old_data:
            print("   Old API failed")
        if not new_data:
            print("   New API failed")
    
    return old_data, new_data

def main():
    """Run the consistency test"""
    print("🚀 PLAGIARISM CONSISTENCY TEST")
    print("=" * 70)
    print()
    
    # Test both APIs
    old_data, new_data = test_plagiarism_consistency()
    
    print("\n🎯 SUMMARY:")
    print("=" * 50)
    if old_data and new_data and new_data.get('success'):
        old_score = old_data.get('plagiarism_score', 0)
        new_score = new_data.get('results', {}).get('overall_score', 0)
        
        if abs(old_score - new_score) < 1.0:
            print("✅ SUCCESS: Both APIs return consistent results!")
            print("✅ The plagiarism report should now match the results!")
            print("✅ No more mismatch between button and actual scores!")
        else:
            print("❌ ISSUE: APIs still return different results")
            print(f"   Old API: {old_score}%")
            print(f"   New API: {new_score}%")
    else:
        print("❌ ERROR: Could not test consistency")
        print("   Check if server is running and both APIs are working")
    
    print()
    print("💡 NEXT STEPS:")
    print("1. Test the 'Check Plagiarism' button in your browser")
    print("2. Verify the modal shows the correct plagiarism score")
    print("3. Check that the score matches what you expect")

if __name__ == "__main__":
    main()
