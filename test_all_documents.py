#!/usr/bin/env python3
"""
Test all documents to verify plagiarism detection accuracy
"""

import requests
import json

def test_submission(submission_id, expected_result):
    """Test a specific submission and verify the result"""
    print(f"\n📋 Testing Submission ID: {submission_id}")
    print(f"   Expected: {expected_result}")
    
    url = f"http://127.0.0.1:5000/api/force-plagiarism-check/{submission_id}"
    
    try:
        response = requests.post(url, json={'force': True, 'debug': True})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                score = data.get('results', {}).get('overall_score', 0)
                debug_info = data.get('results', {}).get('debug_info', {})
                
                print(f"   🎯 Actual Score: {score:.2f}%")
                print(f"   📄 File: {debug_info.get('file_path', 'Unknown')}")
                print(f"   📊 Content Length: {debug_info.get('content_length', 0)} chars")
                print(f"   📁 File Type: {debug_info.get('file_type', 'unknown').upper()}")
                
                # Verify the result
                if expected_result == "HIGH" and score > 70:
                    print("   ✅ CORRECT: High plagiarism detected as expected")
                elif expected_result == "LOW" and score < 30:
                    print("   ✅ CORRECT: Low plagiarism detected as expected")
                elif expected_result == "MODERATE" and 30 <= score <= 70:
                    print("   ✅ CORRECT: Moderate plagiarism detected as expected")
                else:
                    print(f"   ❌ INCORRECT: Expected {expected_result}, got {score:.2f}%")
                
                return score
            else:
                print(f"   ❌ API Error: {data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_all_submissions():
    """Test all submissions to verify accuracy"""
    print("🧪 TESTING ALL SUBMISSIONS FOR ACCURACY")
    print("=" * 60)
    
    # Test cases - you'll need to adjust these based on your actual submissions
    test_cases = [
        (1, "HIGH", "Likely identical content"),
        (3, "HIGH", "Likely identical content"),
        (4, "HIGH", "Likely identical content"),
        (5, "HIGH", "Likely identical content"),
        (10, "LOW", "Original content"),
        (14, "HIGH", "Plagiarized document"),
        (15, "HIGH", "Plagiarized document"),
        (20, "LOW", "Different content")
    ]
    
    results = {}
    
    for submission_id, expected, description in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {description}")
        score = test_submission(submission_id, expected)
        results[submission_id] = {
            'score': score,
            'expected': expected,
            'description': description
        }
    
    return results

def analyze_results(results):
    """Analyze the test results"""
    print(f"\n🎯 RESULTS ANALYSIS")
    print("=" * 60)
    
    correct = 0
    total = 0
    
    for submission_id, data in results.items():
        if data['score'] is not None:
            total += 1
            expected = data['expected']
            score = data['score']
            
            if expected == "HIGH" and score > 70:
                correct += 1
            elif expected == "LOW" and score < 30:
                correct += 1
            elif expected == "MODERATE" and 30 <= score <= 70:
                correct += 1
    
    accuracy = (correct / total * 100) if total > 0 else 0
    
    print(f"📊 Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    
    if accuracy >= 80:
        print("✅ System is working correctly!")
    elif accuracy >= 60:
        print("⚠️ System is partially working")
    else:
        print("❌ System needs adjustment")
    
    print(f"\n📋 Detailed Results:")
    for submission_id, data in results.items():
        if data['score'] is not None:
            status = "✅" if (
                (data['expected'] == "HIGH" and data['score'] > 70) or
                (data['expected'] == "LOW" and data['score'] < 30) or
                (data['expected'] == "MODERATE" and 30 <= data['score'] <= 70)
            ) else "❌"
            
            print(f"   {status} ID {submission_id}: {data['score']:.2f}% (Expected: {data['expected']}) - {data['description']}")

def test_specific_documents():
    """Test the specific test documents we created"""
    print(f"\n🔍 TESTING SPECIFIC TEST DOCUMENTS")
    print("=" * 60)
    
    # Test the documents we created
    test_docs = [
        ("original_online_learning.docx", "LOW", "Original content about online learning"),
        ("plagiarized_online_learning.docx", "HIGH", "Plagiarized content (90%+ copied)"),
        ("different_climate_agriculture.docx", "LOW", "Different content about climate change")
    ]
    
    for filename, expected, description in test_docs:
        print(f"\n📄 Testing: {filename}")
        print(f"   Description: {description}")
        print(f"   Expected: {expected}")
        
        # We need to find which submission ID corresponds to this file
        # For now, let's test a few submission IDs to see which one matches
        print("   💡 Check your submissions to see which ID corresponds to this file")

def main():
    """Run all tests"""
    print("🚀 COMPREHENSIVE PLAGIARISM ACCURACY TEST")
    print("=" * 70)
    print()
    
    # Test all submissions
    results = test_all_submissions()
    
    # Analyze results
    analyze_results(results)
    
    # Test specific documents
    test_specific_documents()
    
    print(f"\n💡 RECOMMENDATIONS:")
    print("=" * 50)
    print("1. If accuracy is high (>80%), the system is working correctly")
    print("2. If accuracy is low (<60%), we need to adjust the algorithm")
    print("3. Check which submission IDs correspond to your test documents")
    print("4. Upload the test documents and note their submission IDs")
    print("5. Test those specific IDs to verify accuracy")

if __name__ == "__main__":
    main()
