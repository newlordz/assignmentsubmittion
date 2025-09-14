#!/usr/bin/env python3
"""
Demo Account Creation Script for Assignment Submission System
This script creates demo accounts for testing purposes.
"""

from app import app, db, User, Assignment, Submission, Grade, Notification
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import os

def create_demo_accounts():
    """Create demo accounts for all user types"""
    
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        print("Creating demo accounts...")
        
        # Demo Students
        students_data = [
            {
                'username': 'student1',
                'email': 'john.doe@university.edu',
                'password': 'student123',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'student'
            },
            {
                'username': 'student2',
                'email': 'jane.smith@university.edu',
                'password': 'student123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'role': 'student'
            },
            {
                'username': 'student3',
                'email': 'mike.johnson@university.edu',
                'password': 'student123',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'role': 'student'
            },
            {
                'username': 'student4',
                'email': 'sarah.wilson@university.edu',
                'password': 'student123',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'role': 'student'
            },
            {
                'username': 'student5',
                'email': 'david.brown@university.edu',
                'password': 'student123',
                'first_name': 'David',
                'last_name': 'Brown',
                'role': 'student'
            }
        ]
        
        # Demo Lecturers
        lecturers_data = [
            {
                'username': 'lecturer1',
                'email': 'prof.jones@university.edu',
                'password': 'lecturer123',
                'first_name': 'Professor',
                'last_name': 'Jones',
                'role': 'lecturer'
            },
            {
                'username': 'lecturer2',
                'email': 'dr.garcia@university.edu',
                'password': 'lecturer123',
                'first_name': 'Dr. Maria',
                'last_name': 'Garcia',
                'role': 'lecturer'
            },
            {
                'username': 'lecturer3',
                'email': 'prof.lee@university.edu',
                'password': 'lecturer123',
                'first_name': 'Professor',
                'last_name': 'Lee',
                'role': 'lecturer'
            }
        ]
        
        # Demo Admin (if not exists)
        admin_data = {
            'username': 'admin',
            'email': 'admin@university.edu',
            'password': 'admin123',
            'first_name': 'System',
            'last_name': 'Administrator',
            'role': 'admin'
        }
        
        # Create students
        for student_data in students_data:
            existing_user = User.query.filter_by(username=student_data['username']).first()
            if not existing_user:
                user = User(
                    username=student_data['username'],
                    email=student_data['email'],
                    password_hash=generate_password_hash(student_data['password']),
                    first_name=student_data['first_name'],
                    last_name=student_data['last_name'],
                    role=student_data['role']
                )
                db.session.add(user)
                print(f"✓ Created student: {student_data['username']} ({student_data['first_name']} {student_data['last_name']})")
            else:
                print(f"- Student already exists: {student_data['username']}")
        
        # Create lecturers
        for lecturer_data in lecturers_data:
            existing_user = User.query.filter_by(username=lecturer_data['username']).first()
            if not existing_user:
                user = User(
                    username=lecturer_data['username'],
                    email=lecturer_data['email'],
                    password_hash=generate_password_hash(lecturer_data['password']),
                    first_name=lecturer_data['first_name'],
                    last_name=lecturer_data['last_name'],
                    role=lecturer_data['role']
                )
                db.session.add(user)
                print(f"✓ Created lecturer: {lecturer_data['username']} ({lecturer_data['first_name']} {lecturer_data['last_name']})")
            else:
                print(f"- Lecturer already exists: {lecturer_data['username']}")
        
        # Create admin
        existing_admin = User.query.filter_by(username=admin_data['username']).first()
        if not existing_admin:
            user = User(
                username=admin_data['username'],
                email=admin_data['email'],
                password_hash=generate_password_hash(admin_data['password']),
                first_name=admin_data['first_name'],
                last_name=admin_data['last_name'],
                role=admin_data['role']
            )
            db.session.add(user)
            print(f"✓ Created admin: {admin_data['username']} ({admin_data['first_name']} {admin_data['last_name']})")
        else:
            print(f"- Admin already exists: {admin_data['username']}")
        
        # Commit all changes
        db.session.commit()
        print("\n✅ Demo accounts created successfully!")
        
        # Print login credentials
        print("\n" + "="*60)
        print("DEMO ACCOUNT CREDENTIALS")
        print("="*60)
        print("\n📚 STUDENTS:")
        print("Username: student1 | Password: student123 | Name: John Doe")
        print("Username: student2 | Password: student123 | Name: Jane Smith")
        print("Username: student3 | Password: student123 | Name: Mike Johnson")
        print("Username: student4 | Password: student123 | Name: Sarah Wilson")
        print("Username: student5 | Password: student123 | Name: David Brown")
        
        print("\n👨‍🏫 LECTURERS:")
        print("Username: lecturer1 | Password: lecturer123 | Name: Professor Jones")
        print("Username: lecturer2 | Password: lecturer123 | Name: Dr. Maria Garcia")
        print("Username: lecturer3 | Password: lecturer123 | Name: Professor Lee")
        
        print("\n👨‍💼 ADMIN:")
        print("Username: admin | Password: admin123 | Name: System Administrator")
        
        print("\n" + "="*60)
        print("You can now use these accounts to test the system!")
        print("="*60)

def create_demo_assignments():
    """Create demo assignments for testing"""
    
    with app.app_context():
        print("\nCreating demo assignments...")
        
        # Get lecturer users
        lecturers = User.query.filter_by(role='lecturer').all()
        if not lecturers:
            print("No lecturers found. Please create demo accounts first.")
            return
        
        # Demo assignments data
        assignments_data = [
            {
                'title': 'Introduction to Programming - Assignment 1',
                'description': 'Write a Python program that demonstrates basic programming concepts including variables, loops, and functions.',
                'instructions': 'Create a program that:\n1. Takes user input for a number\n2. Calculates its factorial\n3. Displays the result in a formatted output\n4. Include proper error handling',
                'due_date': datetime.now() + timedelta(days=7),
                'max_marks': 100,
                'file_requirements': 'Python files (.py) only',
                'created_by': lecturers[0].id
            },
            {
                'title': 'Database Design Project',
                'description': 'Design and implement a database schema for a library management system.',
                'instructions': 'Design a complete database schema including:\n1. Entity Relationship Diagram (ERD)\n2. Normalized table structures\n3. Primary and foreign key relationships\n4. Sample data insertion queries',
                'due_date': datetime.now() + timedelta(days=14),
                'max_marks': 150,
                'file_requirements': 'SQL files (.sql) and documentation (.pdf)',
                'created_by': lecturers[1].id
            },
            {
                'title': 'Web Development Final Project',
                'description': 'Build a complete web application using modern web technologies.',
                'instructions': 'Create a full-stack web application with:\n1. Responsive frontend design\n2. Backend API with authentication\n3. Database integration\n4. User management system\n5. Deploy to a cloud platform',
                'due_date': datetime.now() + timedelta(days=21),
                'max_marks': 200,
                'file_requirements': 'Source code files and deployment documentation',
                'created_by': lecturers[2].id
            },
            {
                'title': 'Data Structures and Algorithms - Lab 3',
                'description': 'Implement various sorting algorithms and analyze their performance.',
                'instructions': 'Implement and compare:\n1. Bubble Sort\n2. Quick Sort\n3. Merge Sort\n4. Heap Sort\n\nInclude time complexity analysis and performance testing.',
                'due_date': datetime.now() + timedelta(days=5),
                'max_marks': 80,
                'file_requirements': 'C++ or Java source files',
                'created_by': lecturers[0].id
            },
            {
                'title': 'Machine Learning Project',
                'description': 'Apply machine learning techniques to solve a real-world problem.',
                'instructions': 'Choose a dataset and:\n1. Perform exploratory data analysis\n2. Preprocess the data\n3. Apply at least 3 different ML algorithms\n4. Compare model performance\n5. Present findings in a report',
                'due_date': datetime.now() + timedelta(days=30),
                'max_marks': 250,
                'file_requirements': 'Jupyter notebooks (.ipynb) and Python code',
                'created_by': lecturers[1].id
            }
        ]
        
        # Create assignments
        for assignment_data in assignments_data:
            existing_assignment = Assignment.query.filter_by(title=assignment_data['title']).first()
            if not existing_assignment:
                assignment = Assignment(
                    title=assignment_data['title'],
                    description=assignment_data['description'],
                    instructions=assignment_data['instructions'],
                    due_date=assignment_data['due_date'],
                    max_marks=assignment_data['max_marks'],
                    file_requirements=assignment_data['file_requirements'],
                    created_by=assignment_data['created_by']
                )
                db.session.add(assignment)
                print(f"✓ Created assignment: {assignment_data['title']}")
            else:
                print(f"- Assignment already exists: {assignment_data['title']}")
        
        db.session.commit()
        print("✅ Demo assignments created successfully!")

def create_demo_submissions():
    """Create demo submissions for testing"""
    
    with app.app_context():
        print("\nCreating demo submissions...")
        
        # Get students and assignments
        students = User.query.filter_by(role='student').all()
        assignments = Assignment.query.all()
        
        if not students or not assignments:
            print("No students or assignments found. Please create demo accounts and assignments first.")
            return
        
        # Create sample submissions
        submission_count = 0
        for assignment in assignments[:3]:  # Only for first 3 assignments
            for i, student in enumerate(students[:3]):  # Only first 3 students
                # Check if submission already exists
                existing_submission = Submission.query.filter_by(
                    assignment_id=assignment.id,
                    student_id=student.id
                ).first()
                
                if not existing_submission:
                    # Create a dummy file for submission
                    dummy_filename = f"submission_{student.username}_{assignment.id}.txt"
                    dummy_filepath = os.path.join('static/uploads', dummy_filename)
                    
                    # Create dummy content
                    dummy_content = f"""
Assignment: {assignment.title}
Student: {student.first_name} {student.last_name}
Submission Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is a demo submission for testing purposes.
The assignment requires: {assignment.instructions[:100]}...

[Demo content - This would be the actual student work in a real scenario]
"""
                    
                    # Write dummy file
                    os.makedirs('static/uploads', exist_ok=True)
                    with open(dummy_filepath, 'w', encoding='utf-8') as f:
                        f.write(dummy_content)
                    
                    # Create submission record
                    submission = Submission(
                        assignment_id=assignment.id,
                        student_id=student.id,
                        file_path=dummy_filepath,
                        file_name=dummy_filename,
                        file_size=len(dummy_content.encode('utf-8')),
                        is_late=i == 2,  # Make third submission late
                        plagiarism_score=0.0
                    )
                    db.session.add(submission)
                    submission_count += 1
                    print(f"✓ Created submission: {student.username} -> {assignment.title}")
        
        db.session.commit()
        print(f"✅ Created {submission_count} demo submissions!")

def create_demo_grades():
    """Create demo grades for some submissions"""
    
    with app.app_context():
        print("\nCreating demo grades...")
        
        # Get submissions and lecturers
        submissions = Submission.query.all()
        lecturers = User.query.filter_by(role='lecturer').all()
        
        if not submissions or not lecturers:
            print("No submissions or lecturers found.")
            return
        
        grade_count = 0
        for i, submission in enumerate(submissions[:6]):  # Grade first 6 submissions
            # Check if already graded
            existing_grade = Grade.query.filter_by(submission_id=submission.id).first()
            if not existing_grade:
                # Create grade
                marks = 75 + (i * 5)  # Varying marks
                if marks > submission.assignment.max_marks:
                    marks = submission.assignment.max_marks
                
                feedback = f"Good work! You demonstrated understanding of the concepts. "
                if marks >= 90:
                    feedback += "Excellent submission with clear explanations and proper implementation."
                elif marks >= 80:
                    feedback += "Well done with minor areas for improvement."
                elif marks >= 70:
                    feedback += "Satisfactory work with some areas that need attention."
                else:
                    feedback += "Please review the requirements and resubmit if needed."
                
                grade = Grade(
                    submission_id=submission.id,
                    grader_id=lecturers[0].id,
                    marks=marks,
                    feedback=feedback
                )
                db.session.add(grade)
                grade_count += 1
                print(f"✓ Created grade: {submission.student.first_name} {submission.student.last_name} - {marks} marks")
        
        db.session.commit()
        print(f"✅ Created {grade_count} demo grades!")

def main():
    """Main function to create all demo data"""
    print("🚀 Assignment Submission System - Demo Data Creator")
    print("=" * 60)
    
    try:
        # Create demo accounts
        create_demo_accounts()
        
        # Create demo assignments
        create_demo_assignments()
        
        # Create demo submissions
        create_demo_submissions()
        
        # Create demo grades
        create_demo_grades()
        
        print("\n🎉 All demo data created successfully!")
        print("\nYou can now start the application and test with the demo accounts.")
        
    except Exception as e:
        print(f"\n❌ Error creating demo data: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    main()
