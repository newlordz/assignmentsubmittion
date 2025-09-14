#!/usr/bin/env python3
"""
Create demo data (assignments and submissions) for testing
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Assignment, Submission

def create_demo_data():
    """Create demo assignments and submissions"""
    
    with app.app_context():
        print("🚀 Creating demo data...")
        
        # Get demo users
        lecturer1 = User.query.filter_by(username='lecturer1').first()
        lecturer2 = User.query.filter_by(username='lecturer2').first()
        
        students = User.query.filter_by(role='student').all()
        
        if not lecturer1 or not students:
            print("❌ Demo users not found. Please run create_demo_accounts.py first.")
            return False
        
        # Create sample assignments
        assignments_data = [
            {
                'title': 'Introduction to Programming',
                'description': 'Write a simple Python program that calculates the factorial of a number.',
                'instructions': 'Create a Python script that:\n1. Takes a number as input\n2. Calculates its factorial\n3. Displays the result\n\nSubmit your .py file.',
                'due_date': datetime.utcnow() + timedelta(days=7),
                'max_marks': 100,
                'file_requirements': 'Python files (.py)',
                'created_by': lecturer1.id
            },
            {
                'title': 'Web Development Project',
                'description': 'Create a simple HTML/CSS website with at least 3 pages.',
                'instructions': 'Build a personal portfolio website with:\n1. Home page\n2. About page\n3. Contact page\n\nInclude CSS styling and make it responsive.',
                'due_date': datetime.utcnow() + timedelta(days=14),
                'max_marks': 150,
                'file_requirements': 'HTML, CSS files',
                'created_by': lecturer1.id
            },
            {
                'title': 'Database Design Assignment',
                'description': 'Design a database schema for a library management system.',
                'instructions': 'Create an ER diagram and SQL schema for:\n1. Books table\n2. Members table\n3. Borrowing records\n\nSubmit the SQL file and ER diagram.',
                'due_date': datetime.utcnow() + timedelta(days=10),
                'max_marks': 120,
                'file_requirements': 'SQL files, images',
                'created_by': lecturer2.id
            },
            {
                'title': 'Data Structures Lab',
                'description': 'Implement a binary search tree in Python.',
                'instructions': 'Create a Python class for BST with:\n1. Insert method\n2. Search method\n3. Delete method\n4. In-order traversal\n\nInclude test cases.',
                'due_date': datetime.utcnow() + timedelta(days=5),
                'max_marks': 100,
                'file_requirements': 'Python files (.py)',
                'created_by': lecturer1.id
            }
        ]
        
        created_assignments = []
        
        for assignment_data in assignments_data:
            # Check if assignment already exists
            existing = Assignment.query.filter_by(title=assignment_data['title']).first()
            if existing:
                print(f"✅ Assignment already exists: {assignment_data['title']}")
                created_assignments.append(existing)
                continue
            
            assignment = Assignment(**assignment_data)
            db.session.add(assignment)
            db.session.commit()
            created_assignments.append(assignment)
            print(f"🆕 Created assignment: {assignment_data['title']}")
        
        # Create sample submissions
        print("\n📝 Creating sample submissions...")
        
        # Sample file content for submissions
        sample_files = {
            'factorial.py': '''def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Test the function
number = int(input("Enter a number: "))
result = factorial(number)
print(f"The factorial of {number} is {result}")''',
            
            'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Welcome to My Portfolio</h1>
        <nav>
            <a href="index.html">Home</a>
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
        </nav>
    </header>
    <main>
        <h2>Hello, I'm a Web Developer</h2>
        <p>This is my portfolio website showcasing my projects and skills.</p>
    </main>
</body>
</html>''',
            
            'library_schema.sql': '''-- Library Management System Database Schema

CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publication_year INT,
    available_copies INT DEFAULT 1
);

CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    join_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE borrowing_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    book_id INT,
    borrow_date DATE DEFAULT CURRENT_DATE,
    return_date DATE,
    due_date DATE,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);''',
            
            'bst.py': '''class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value):
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node is not None
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)
    
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

# Test the BST
bst = BinarySearchTree()
bst.insert(50)
bst.insert(30)
bst.insert(70)
bst.insert(20)
bst.insert(40)
bst.insert(60)
bst.insert(80)

print("In-order traversal:", bst.inorder_traversal())
print("Search for 40:", bst.search(40))
print("Search for 90:", bst.search(90))'''
        }
        
        # Create submissions for each assignment
        submission_count = 0
        
        for i, assignment in enumerate(created_assignments):
            # Get file info for this assignment
            if i == 0:  # Programming assignment
                filename = 'factorial.py'
                content = sample_files['factorial.py']
            elif i == 1:  # Web development
                filename = 'index.html'
                content = sample_files['index.html']
            elif i == 2:  # Database assignment
                filename = 'library_schema.sql'
                content = sample_files['library_schema.sql']
            else:  # Data structures
                filename = 'bst.py'
                content = sample_files['bst.py']
            
            # Create submissions for some students (not all to make it realistic)
            for j, student in enumerate(students[:3]):  # Only first 3 students submit
                # Check if submission already exists
                existing = Submission.query.filter_by(
                    assignment_id=assignment.id,
                    student_id=student.id
                ).first()
                
                if existing:
                    continue
                
                # Create submission
                submission = Submission(
                    assignment_id=assignment.id,
                    student_id=student.id,
                    file_path=f'static/uploads/demo_{filename}',
                    file_name=filename,
                    file_size=len(content),
                    is_late=datetime.utcnow() > assignment.due_date,
                    content=content
                )
                
                db.session.add(submission)
                submission_count += 1
        
        db.session.commit()
        
        print(f"\n📊 Demo Data Summary:")
        print(f"  Assignments created: {len(created_assignments)}")
        print(f"  Submissions created: {submission_count}")
        print(f"  Students with submissions: 3")
        
        # Show assignment details
        print(f"\n📋 Created Assignments:")
        for assignment in created_assignments:
            submissions = Submission.query.filter_by(assignment_id=assignment.id).count()
            print(f"  • {assignment.title} ({submissions} submissions)")
        
        return True

def main():
    """Main function"""
    print("🚀 Creating Demo Data")
    print("=" * 50)
    
    try:
        success = create_demo_data()
        if success:
            print("\n🎉 Demo data created successfully!")
            print("You can now test the system with realistic data.")
        else:
            print("\n💥 Failed to create demo data!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
