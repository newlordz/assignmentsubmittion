#!/usr/bin/env python3
"""
Database migration script to add Course functionality
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Assignment, Course, course_enrollment

def migrate_database():
    """Migrate database to add Course functionality"""
    with app.app_context():
        try:
            print("🔄 Starting database migration...")
            
            # Create all tables (including new Course table)
            db.create_all()
            print("✅ All tables created/updated")
            
            # Check if courses already exist
            if Course.query.first():
                print("✅ Courses already exist, skipping creation")
                return
            
            # Create demo courses
            print("🚀 Creating demo courses...")
            
            # Get lecturers
            lecturer1 = User.query.filter_by(username='lecturer1').first()
            lecturer2 = User.query.filter_by(username='lecturer2').first()
            
            if not lecturer1 or not lecturer2:
                print("❌ Demo lecturers not found. Please run the main app first to create demo accounts.")
                return
            
            # Create demo courses
            courses_data = [
                {
                    'name': 'Introduction to Programming',
                    'code': 'CS101',
                    'description': 'Learn the fundamentals of programming with Python',
                    'lecturer_id': lecturer1.id
                },
                {
                    'name': 'Web Development',
                    'code': 'CS201',
                    'description': 'Build modern web applications with HTML, CSS, and JavaScript',
                    'lecturer_id': lecturer1.id
                },
                {
                    'name': 'Database Systems',
                    'code': 'CS301',
                    'description': 'Design and implement database systems',
                    'lecturer_id': lecturer2.id
                },
                {
                    'name': 'Software Engineering',
                    'code': 'CS401',
                    'description': 'Software development methodologies and best practices',
                    'lecturer_id': lecturer2.id
                }
            ]
            
            created_courses = []
            for course_data in courses_data:
                course = Course(**course_data)
                db.session.add(course)
                created_courses.append(course)
            
            db.session.commit()
            print("✅ Demo courses created")
            
            # Enroll all students in all courses
            students = User.query.filter_by(role='student').all()
            for course in created_courses:
                for student in students:
                    course.students.append(student)
            
            db.session.commit()
            print("✅ All students enrolled in courses")
            
            # Update existing assignments to have course_id
            print("🔄 Updating existing assignments...")
            assignments = Assignment.query.filter(Assignment.course_id.is_(None)).all()
            
            if assignments:
                # Assign courses to existing assignments
                cs101 = Course.query.filter_by(code='CS101').first()
                cs201 = Course.query.filter_by(code='CS201').first()
                cs301 = Course.query.filter_by(code='CS301').first()
                
                for i, assignment in enumerate(assignments):
                    if 'Programming' in assignment.title or 'factorial' in assignment.title.lower():
                        assignment.course_id = cs101.id
                    elif 'Web' in assignment.title or 'HTML' in assignment.title:
                        assignment.course_id = cs201.id
                    elif 'Database' in assignment.title:
                        assignment.course_id = cs301.id
                    else:
                        # Default to CS101
                        assignment.course_id = cs101.id
                
                db.session.commit()
                print(f"✅ Updated {len(assignments)} assignments with course IDs")
            
            print("🎉 Database migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    migrate_database()
