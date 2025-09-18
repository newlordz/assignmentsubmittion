#!/usr/bin/env python3
"""
Clear old plagiarism reports from the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Submission

def clear_old_reports():
    """Clear old plagiarism reports from the database"""
    with app.app_context():
        print("🧹 CLEARING OLD PLAGIARISM REPORTS")
        print("=" * 50)
        
        # Get all submissions
        submissions = Submission.query.all()
        
        print(f"Found {len(submissions)} submissions")
        print()
        
        for submission in submissions:
            if submission.plagiarism_report:
                print(f"Submission {submission.id}:")
                print(f"  Old Report: {submission.plagiarism_report[:100]}...")
                print(f"  Old Score: {submission.plagiarism_score}%")
                
                # Clear the old report
                submission.plagiarism_report = None
                submission.plagiarism_score = 0.0
                
                print(f"  ✅ Cleared old report")
                print()
        
        # Commit changes
        db.session.commit()
        print("✅ All old plagiarism reports cleared!")
        print("✅ Now the frontend will use the Force API results")

def main():
    """Run the cleanup"""
    clear_old_reports()
    
    print("\n💡 NEXT STEPS:")
    print("1. Refresh your browser page")
    print("2. Click 'Check Plagiarism' button")
    print("3. You should now see the correct Force API results")
    print("4. The modal should show the proper plagiarism score (e.g., 92.88%)")

if __name__ == "__main__":
    main()
