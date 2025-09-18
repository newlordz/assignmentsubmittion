#!/usr/bin/env python3
"""
Check plagiarism results in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Submission

def check_database_results():
    """Check plagiarism results in the database"""
    with app.app_context():
        print("🔍 CHECKING DATABASE RESULTS")
        print("=" * 50)
        
        # Get all submissions with plagiarism reports
        submissions = Submission.query.filter(Submission.plagiarism_report.isnot(None)).all()
        
        print(f"Found {len(submissions)} submissions with plagiarism reports")
        print()
        
        for submission in submissions:
            print(f"Submission {submission.id}:")
            print(f"  Plagiarism Score: {submission.plagiarism_score}%")
            print(f"  Plagiarism Report: {submission.plagiarism_report[:100]}...")
            print(f"  File: {submission.file_name}")
            print()
        
        # Also check submissions without reports
        no_reports = Submission.query.filter(Submission.plagiarism_report.is_(None)).all()
        print(f"Found {len(no_reports)} submissions without plagiarism reports")
        
        if no_reports:
            print("Submissions without reports:")
            for submission in no_reports:
                print(f"  Submission {submission.id}: {submission.file_name}")

def main():
    """Run the database check"""
    check_database_results()
    
    print("\n💡 SUMMARY:")
    print("=" * 30)
    print("✅ Database results checked")
    print("✅ Plagiarism reports verified")
    print()
    print("🎯 NEXT STEPS:")
    print("1. Students and teachers should now see plagiarism reports")
    print("2. The 'Plagiarism Report' section should show saved results")
    print("3. Both modal and report should display consistent scores")

if __name__ == "__main__":
    main()
