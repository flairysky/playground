"""
Database migration script to add new weekly plan features.

Run this to update existing database with new columns.
"""

import sqlite3
import os

def migrate_database():
    """Add new columns to weekly_plans table."""
    db_path = os.path.join('instance', 'app.db')
    
    if not os.path.exists(db_path):
        print("Database not found. Please run init_db.py first.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Migrating database...")
    
    # Add new columns if they don't exist
    try:
        cursor.execute("ALTER TABLE weekly_plans ADD COLUMN plan_mode VARCHAR(20) DEFAULT 'chapterwise'")
        print("✓ Added plan_mode column")
    except sqlite3.OperationalError:
        print("- plan_mode column already exists")
    
    try:
        cursor.execute("ALTER TABLE weekly_plans ADD COLUMN current_chapter_number INTEGER")
        print("✓ Added current_chapter_number column")
    except sqlite3.OperationalError:
        print("- current_chapter_number column already exists")
    
    try:
        cursor.execute("ALTER TABLE weekly_plans ADD COLUMN deadline_time VARCHAR(5)")
        print("✓ Added deadline_time column")
    except sqlite3.OperationalError:
        print("- deadline_time column already exists")
    
    try:
        cursor.execute("ALTER TABLE weekly_plans ADD COLUMN custom_text TEXT")
        print("✓ Added custom_text column")
    except sqlite3.OperationalError:
        print("- custom_text column already exists")
    
    try:
        cursor.execute("ALTER TABLE weekly_plans ADD COLUMN auto_renew BOOLEAN DEFAULT 1")
        print("✓ Added auto_renew column")
    except sqlite3.OperationalError:
        print("- auto_renew column already exists")
    
    conn.commit()
    conn.close()
    
    print("\n✓ Database migration completed!")
    print("You can now use the new weekly plan features.")

if __name__ == '__main__':
    migrate_database()
