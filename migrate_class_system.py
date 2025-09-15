#!/usr/bin/env python3
"""
Migration script for the new class-based system.
This script will recreate the database with the new schema.
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Course, Class, Assignment, Submission, Grade

def migrate_database():
    """Migrate database to include the new Class model and relationships"""
    print("🔄 Starting database migration for class-based system...")
    
    with app.app_context():
        try:
            # Drop all tables to recreate with new schema
            print("🗑️  Dropping existing tables...")
            db.drop_all()
            
            # Create all tables with new schema
            print("🏗️  Creating new tables...")
            db.create_all()
            
            print("✅ Database migration completed successfully!")
            print("📝 Note: All existing data has been cleared.")
            print("🔄 Run the application to recreate demo data.")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 Class System Database Migration")
    print("=" * 50)
    
    # Confirm migration
    response = input("⚠️  This will delete all existing data. Continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Migration cancelled.")
        sys.exit(0)
    
    success = migrate_database()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("💡 Next steps:")
        print("   1. Start the Flask application")
        print("   2. Demo data will be created automatically")
        print("   3. Test the new class-based system")
    else:
        print("\n💥 Migration failed. Check the error messages above.")
        sys.exit(1)
