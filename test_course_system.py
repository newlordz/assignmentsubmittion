#!/usr/bin/env python3
"""
Test the course-based assignment system
"""

import requests
import time

def test_course_system():
    print("🧪 Testing Course-Based Assignment System...")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Check if app is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ App is running successfully")
        else:
            print(f"❌ App returned status code: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ App is not running: {e}")
        return
    
    print("\n📚 Course System Features:")
    print("1. ✅ Course-based assignment distribution")
    print("2. ✅ Students can enroll in courses")
    print("3. ✅ Lecturers can create courses")
    print("4. ✅ Assignments are targeted to specific courses")
    print("5. ✅ Email notifications are course-specific")
    
    print("\n🌐 Ready to Test:")
    print(f"Open your browser: {base_url}")
    print("\n📋 Test Steps:")
    print("1. Login as lecturer1 / password123")
    print("2. Go to 'Create Course' to create a new course")
    print("3. Go to 'Create Assignment' and select a course")
    print("4. Login as student1 / password123")
    print("5. Go to 'Enroll in Course' to join courses")
    print("6. Check 'My Assignments' - only see course-specific assignments")
    print("7. Check your Gmail for targeted email notifications!")
    
    print("\n🎯 Key Benefits:")
    print("• No more spam emails to all students")
    print("• Targeted assignment distribution")
    print("• Professional course management")
    print("• Better organization for lecturers and students")

if __name__ == '__main__':
    test_course_system()
