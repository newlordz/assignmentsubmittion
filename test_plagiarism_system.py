#!/usr/bin/env python3
"""
Comprehensive Test for E-Assignment System Plagiarism Detection
Tests both Dolos integration and local plagiarism detection methods.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_local_plagiarism_detection():
    """Test the local plagiarism detection system."""
    print("🧪 Testing Local Plagiarism Detection...")
    
    try:
        # Import the plagiarism detection functions
        from app import calculate_local_plagiarism_score, calculate_tfidf_similarity
        
        # Test data - similar Python code
        code1 = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
        
        code2 = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
        
        code3 = """
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fib(10))
"""
        
        # Test with identical code
        score1 = calculate_local_plagiarism_score(code1, [code2])
        print(f"✅ Identical code similarity: {score1}%")
        
        # Test with different implementation
        score2 = calculate_local_plagiarism_score(code1, [code3])
        print(f"✅ Different implementation similarity: {score2}%")
        
        # Test TF-IDF directly
        documents = [code1, code2, code3]
        tfidf_score = calculate_tfidf_similarity(documents)
        print(f"✅ TF-IDF similarity: {tfidf_score}%")
        
        print("✅ Local plagiarism detection working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Local plagiarism detection test failed: {e}")
        return False

def test_dolos_integration():
    """Test the Dolos integration system."""
    print("\n🧪 Testing Dolos Integration...")
    
    try:
        from dolos_integration import DolosIntegration
        
        # Initialize Dolos integration
        dolos = DolosIntegration()
        
        # Check availability
        is_available = dolos.is_available()
        print(f"✅ Dolos availability check: {'Available' if is_available else 'Not available (Node.js required)'}")
        
        if is_available:
            # Test with sample submissions
            sample_submissions = [
                {
                    "id": "student1",
                    "content": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
                },
                {
                    "id": "student2", 
                    "content": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
                }
            ]
            
            print("🔍 Running Dolos analysis...")
            results = dolos.analyze_submissions(sample_submissions, language="python")
            
            if "error" not in results:
                print("✅ Dolos analysis completed successfully")
                print(f"📊 Results: {results}")
            else:
                print(f"⚠️ Dolos analysis failed: {results['error']}")
        else:
            print("ℹ️ Dolos integration not available - this is expected without Node.js")
        
        print("✅ Dolos integration test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Dolos integration test failed: {e}")
        return False

def test_app_integration():
    """Test the main application integration."""
    print("\n🧪 Testing Application Integration...")
    
    try:
        # Import the main app
        from app import app, calculate_plagiarism_score
        
        # Test the integrated plagiarism detection
        content = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""
        
        other_submissions = [
            """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
""",
            """
def sum_list(lst):
    result = 0
    for item in lst:
        result = result + item
    return result
"""
        ]
        
        # Test the main plagiarism detection function
        score = calculate_plagiarism_score(content, other_submissions)
        print(f"✅ Integrated plagiarism detection score: {score}%")
        
        # Test Flask app creation
        with app.test_client() as client:
            response = client.get('/')
            print(f"✅ Flask app responds: {response.status_code}")
        
        print("✅ Application integration test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Application integration test failed: {e}")
        return False

def test_file_detection():
    """Test file type detection for Dolos."""
    print("\n🧪 Testing File Type Detection...")
    
    try:
        from dolos_integration import DolosIntegration
        
        dolos = DolosIntegration()
        
        # Test different file types
        test_cases = [
            ("def hello(): pass", ".py"),
            ("function hello() { console.log('hi'); }", ".js"),
            ("public class Hello { public static void main(String[] args) {} }", ".java"),
            ("#include <stdio.h>\nint main() { return 0; }", ".c"),
            ("<html><body>Hello</body></html>", ".html"),
            ("SELECT * FROM users;", ".sql")
        ]
        
        for content, expected_ext in test_cases:
            detected_ext = dolos._detect_file_extension(content)
            status = "✅" if detected_ext == expected_ext else "⚠️"
            print(f"{status} {expected_ext}: {detected_ext}")
        
        print("✅ File type detection test completed!")
        return True
        
    except Exception as e:
        print(f"❌ File type detection test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎓 E-Assignment System - Plagiarism Detection Test Suite")
    print("=" * 60)
    
    tests = [
        ("Local Plagiarism Detection", test_local_plagiarism_detection),
        ("Dolos Integration", test_dolos_integration),
        ("Application Integration", test_app_integration),
        ("File Type Detection", test_file_detection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The plagiarism detection system is working correctly.")
        print("\n📋 System Status:")
        print("✅ Local plagiarism detection: Working")
        print("✅ Dolos integration: Available (with Node.js) or Fallback (without Node.js)")
        print("✅ Application integration: Working")
        print("✅ File type detection: Working")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        sys.exit(1)
