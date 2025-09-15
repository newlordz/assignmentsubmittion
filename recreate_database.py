#!/usr/bin/env python3
"""
Force recreate the database with the new class-based schema.
"""

import os
import sys
import shutil

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def recreate_database():
    """Force recreate the database"""
    print("🔄 Force recreating database...")
    
    # Remove the entire instance directory
    instance_dir = "instance"
    if os.path.exists(instance_dir):
        print(f"🗑️  Removing {instance_dir} directory...")
        shutil.rmtree(instance_dir)
        print("✅ Instance directory removed")
    
    # Create new instance directory
    os.makedirs(instance_dir, exist_ok=True)
    print("✅ New instance directory created")
    
    print("🎉 Database recreation completed!")
    print("💡 The database will be recreated with the new schema when you start the app.")

if __name__ == '__main__':
    recreate_database()
