#!/usr/bin/env python3
"""
Migration script to add category field to Book model.

Adds category column to books table with values: high_school, undergraduate, graduate
"""

import sqlite3
import sys
from pathlib import Path

def migrate_database():
    """Add category column to books table."""
    
    # Database path
    db_path = Path(__file__).parent / 'instance' / 'app.db'
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        print("Please run init_db.py first to create the database.")
        sys.exit(1)
    
    # Connect to database
    print(f"📂 Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if books table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
        if not cursor.fetchone():
            print("❌ Books table not found. Please run init_db.py first to create database tables.")
            sys.exit(1)
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(books)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'category' not in columns:
            print("➕ Adding 'category' column to books table...")
            cursor.execute("ALTER TABLE books ADD COLUMN category VARCHAR(50) DEFAULT 'undergraduate'")
            print("   ✅ Added 'category' column")
            
            # Set default value for existing books
            cursor.execute("UPDATE books SET category = 'undergraduate' WHERE category IS NULL")
            print("   ✅ Set default value (undergraduate) for existing books")
            
            # Commit changes
            conn.commit()
            print("\n✅ Migration completed successfully!")
            print("\nNew feature:")
            print("  • Books now have categories: high_school, undergraduate, graduate")
            print("  • Leaderboard can be filtered by book category")
            print("\nYou can update book categories in the database:")
            print("  - high_school: For high school level math books")
            print("  - undergraduate: For undergraduate level books (default)")
            print("  - graduate: For graduate level books")
        else:
            print("   ⏭️  'category' column already exists")
            print("\n✅ Database already up to date - no changes needed")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)
    
    finally:
        conn.close()
        print("\n🔌 Database connection closed")

if __name__ == "__main__":
    print("=" * 70)
    print("  BOOK CATEGORY MIGRATION")
    print("=" * 70)
    print()
    migrate_database()
