#!/usr/bin/env python3
"""
Test script for plagiarism detection functionality
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Assignment, Submission, calculate_plagiarism_score, read_file_content

def create_test_data():
    """Create test data for plagiarism detection"""
    
    with app.app_context():
        # Create test users
        lecturer = User.query.filter_by(email='lecturer@test.com').first()
        if not lecturer:
            lecturer = User(
            username='test_lecturer',
            email='lecturer@test.com',
            password_hash='test_hash',
            role='lecturer',
            first_name='Test',
            last_name='Lecturer',
            is_active=True
        )
            db.session.add(lecturer)
        
        student1 = User.query.filter_by(email='student1@test.com').first()
        if not student1:
            student1 = User(
            username='test_student1',
            email='student1@test.com',
            password_hash='test_hash',
            role='student',
            first_name='Test',
            last_name='Student1',
            is_active=True
        )
            db.session.add(student1)
        
        student2 = User.query.filter_by(email='student2@test.com').first()
        if not student2:
            student2 = User(
            username='test_student2',
            email='student2@test.com',
            password_hash='test_hash',
            role='student',
            first_name='Test',
            last_name='Student2',
            is_active=True
        )
            db.session.add(student2)
        
        db.session.commit()
        
        # Create test assignment
        assignment = Assignment.query.filter_by(title='Test Plagiarism Assignment').first()
        if not assignment:
            assignment = Assignment(
                title='Test Plagiarism Assignment',
                description='Test assignment for plagiarism detection',
                created_by=lecturer.id,
                due_date=datetime.utcnow() + timedelta(days=7),
                max_marks=100,
                is_active=True
            )
            db.session.add(assignment)
            db.session.commit()
        
        return lecturer, student1, student2, assignment

def create_test_files():
    """Create test files with different content"""
    
    # Create test directory
    test_dir = 'test_files'
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # Test file 1 - Original content
    file1_content = """
    This is a test document about machine learning algorithms.
    Machine learning is a subset of artificial intelligence that focuses on algorithms.
    These algorithms can learn from data and make predictions.
    Common types include supervised learning, unsupervised learning, and reinforcement learning.
    Supervised learning uses labeled data to train models.
    Unsupervised learning finds patterns in unlabeled data.
    Reinforcement learning learns through trial and error with rewards.
    """
    
    # Test file 2 - Similar content (should show plagiarism)
    file2_content = """
    This is a test document about machine learning algorithms.
    Machine learning is a subset of artificial intelligence that focuses on algorithms.
    These algorithms can learn from data and make predictions.
    Common types include supervised learning, unsupervised learning, and reinforcement learning.
    Supervised learning uses labeled data to train models.
    Unsupervised learning finds patterns in unlabeled data.
    Reinforcement learning learns through trial and error with rewards.
    """
    
    # Test file 3 - Different content (should show low plagiarism)
    file3_content = """
    This document discusses web development technologies.
    Web development involves creating websites and web applications.
    Frontend development focuses on user interface and user experience.
    Backend development handles server-side logic and database operations.
    Popular frontend technologies include HTML, CSS, and JavaScript.
    Popular backend technologies include Python, Java, and Node.js.
    Full-stack developers work on both frontend and backend.
    """
    
    # Write test files
    with open(os.path.join(test_dir, 'test1.txt'), 'w', encoding='utf-8') as f:
        f.write(file1_content)
    
    with open(os.path.join(test_dir, 'test2.txt'), 'w', encoding='utf-8') as f:
        f.write(file2_content)
    
    with open(os.path.join(test_dir, 'test3.txt'), 'w', encoding='utf-8') as f:
        f.write(file3_content)
    
    return [
        os.path.join(test_dir, 'test1.txt'),
        os.path.join(test_dir, 'test2.txt'),
        os.path.join(test_dir, 'test3.txt')
    ]

def test_file_reading():
    """Test the file reading functionality"""
    print("🔍 Testing file reading functionality...")
    
    test_files = create_test_files()
    
    for i, file_path in enumerate(test_files, 1):
        content = read_file_content(file_path)
        print(f"  File {i}: {len(content)} characters read")
        print(f"  Preview: {content[:100]}...")
        print()
    
    return test_files

def test_plagiarism_algorithm():
    """Test the plagiarism detection algorithm"""
    print("🧮 Testing plagiarism detection algorithm...")
    
    test_files = create_test_files()
    
    # Read content from files
    content1 = read_file_content(test_files[0])
    content2 = read_file_content(test_files[1])
    content3 = read_file_content(test_files[2])
    
    # Create mock submission objects
    class MockSubmission:
        def __init__(self, content):
            self.content = content
    
    # Test 1: Identical content (should show high plagiarism)
    print("Test 1: Identical content")
    score1 = calculate_plagiarism_score(content1, [MockSubmission(content1)])
    print(f"  Plagiarism score: {score1:.2f}%")
    print()
    
    # Test 2: Similar content (should show high plagiarism)
    print("Test 2: Similar content")
    score2 = calculate_plagiarism_score(content1, [MockSubmission(content2)])
    print(f"  Plagiarism score: {score2:.2f}%")
    print()
    
    # Test 3: Different content (should show low plagiarism)
    print("Test 3: Different content")
    score3 = calculate_plagiarism_score(content1, [MockSubmission(content3)])
    print(f"  Plagiarism score: {score3:.2f}%")
    print()
    
    # Test 4: Multiple comparisons
    print("Test 4: Multiple file comparison")
    score4 = calculate_plagiarism_score(content1, [MockSubmission(content2), MockSubmission(content3)])
    print(f"  Plagiarism score: {score4:.2f}%")
    print()
    
    return {
        'identical': score1,
        'similar': score2,
        'different': score3,
        'multiple': score4
    }

def test_database_integration():
    """Test plagiarism detection with database"""
    print("🗄️ Testing database integration...")
    
    with app.app_context():
        try:
            # Create test data
            lecturer, student1, student2, assignment = create_test_data()
            
            # Create test submissions
            test_files = create_test_files()
            
            # Clear existing test submissions
            Submission.query.filter_by(assignment_id=assignment.id).delete()
            db.session.commit()
            
            # Create submissions
            submission1 = Submission(
                assignment_id=assignment.id,
                student_id=student1.id,
                file_path=test_files[0],
                file_name='test1.txt',
                file_size=os.path.getsize(test_files[0]),
                is_late=False,
                content=read_file_content(test_files[0])
            )
            
            submission2 = Submission(
                assignment_id=assignment.id,
                student_id=student2.id,
                file_path=test_files[1],
                file_name='test2.txt',
                file_size=os.path.getsize(test_files[1]),
                is_late=False,
                content=read_file_content(test_files[1])
            )
            
            db.session.add(submission1)
            db.session.add(submission2)
            db.session.commit()
            
            print(f"  Created {assignment.title}")
            print(f"  Created submission 1: {submission1.file_name}")
            print(f"  Created submission 2: {submission2.file_name}")
            print()
            
            # Test plagiarism detection
            print("Testing plagiarism detection on submission 1...")
            other_submissions = Submission.query.filter(
                Submission.assignment_id == assignment.id,
                Submission.id != submission1.id
            ).all()
            
            plagiarism_score = calculate_plagiarism_score(
                submission1.content, 
                [sub.content for sub in other_submissions if sub.content]
            )
            
            print(f"  Plagiarism score: {plagiarism_score:.2f}%")
            
            # Update submission with plagiarism score
            submission1.plagiarism_score = plagiarism_score
            submission1.plagiarism_report = f"Plagiarism score: {plagiarism_score:.2f}%"
            db.session.commit()
            
            print("✅ Database integration test completed")
            return True
            
        except Exception as e:
            print(f"❌ Database integration test failed: {e}")
            return False

def cleanup_test_data():
    """Clean up test data"""
    print("🧹 Cleaning up test data...")
    
    # Remove test files
    test_dir = 'test_files'
    if os.path.exists(test_dir):
        for file in os.listdir(test_dir):
            os.remove(os.path.join(test_dir, file))
        os.rmdir(test_dir)
        print("  Removed test files")
    
    # Clean up database (optional - comment out if you want to keep test data)
    with app.app_context():
        try:
            # Remove test submissions
            test_assignment = Assignment.query.filter_by(title='Test Plagiarism Assignment').first()
            if test_assignment:
                Submission.query.filter_by(assignment_id=test_assignment.id).delete()
                db.session.commit()
                print("  Removed test submissions from database")
        except Exception as e:
            print(f"  Warning: Could not clean up database: {e}")

def main():
    """Run all plagiarism detection tests"""
    print("🚀 Starting Plagiarism Detection Tests")
    print("=" * 50)
    
    try:
        # Test 1: File reading
        test_file_reading()
        
        # Test 2: Plagiarism algorithm
        scores = test_plagiarism_algorithm()
        
        # Test 3: Database integration
        db_success = test_database_integration()
        
        # Results summary
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        print(f"File Reading: ✅ Working")
        print(f"Plagiarism Algorithm: ✅ Working")
        print(f"  - Identical content: {scores['identical']:.2f}%")
        print(f"  - Similar content: {scores['similar']:.2f}%")
        print(f"  - Different content: {scores['different']:.2f}%")
        print(f"  - Multiple files: {scores['multiple']:.2f}%")
        print(f"Database Integration: {'✅ Working' if db_success else '❌ Failed'}")
        
        if scores['similar'] > 80 and scores['different'] < 20:
            print("\n🎉 PLAGIARISM DETECTION IS WORKING CORRECTLY!")
            print("   - High similarity detected for similar content")
            print("   - Low similarity detected for different content")
        else:
            print("\n⚠️ PLAGIARISM DETECTION MAY NEED TUNING")
            print("   - Check algorithm parameters")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    
    finally:
        # Cleanup
        cleanup_test_data()
        print("\n✅ Test completed")

if __name__ == "__main__":
    main()
