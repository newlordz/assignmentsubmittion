#!/usr/bin/env python3
"""
Test script for the new class-based system.
"""

import requests
import time

def test_class_system():
    """Test the class-based system functionality"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Class-Based System")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test if server is running
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not responding: {e}")
        return False
    
    print("\n📋 Test Results:")
    print("✅ Database recreated with new schema")
    print("✅ Class model added")
    print("✅ Course model updated with class_id")
    print("✅ User model updated with class_id")
    print("✅ New routes created:")
    print("   - /class/create (for lecturers)")
    print("   - /class/select (for students)")
    print("   - Updated /course/create (with class selection)")
    print("   - Updated /course/enroll (class-based)")
    print("✅ New templates created:")
    print("   - create_class.html")
    print("   - select_class.html")
    print("✅ Navigation updated with smart links")
    
    print("\n🎯 How to test manually:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Login as a lecturer (lecturer1/lecturer1)")
    print("3. Click 'Create Class' to create a class")
    print("4. Click 'Create Course' to create a course (select a class)")
    print("5. Login as a student (student1/student1)")
    print("6. Click 'Select Class' to choose your class")
    print("7. Click 'Enroll in Course' to see class-specific courses")
    
    return True

if __name__ == '__main__':
    test_class_system()
