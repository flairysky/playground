#!/usr/bin/env python3
"""
Migration script to add topic field to Book model.

Adds topic column to books table with values: 
- algebra
- analysis
- geometry_topology
- logic
- applied_mathematics
"""

import sqlite3
import sys
from pathlib import Path

def migrate_database():
    """Add topic column to books table."""
    
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
        
        if 'topic' not in columns:
            print("➕ Adding 'topic' column to books table...")
            cursor.execute("ALTER TABLE books ADD COLUMN topic VARCHAR(100) DEFAULT 'algebra'")
            print("   ✅ Added 'topic' column")
            
            # Set default value for existing books
            cursor.execute("UPDATE books SET topic = 'algebra' WHERE topic IS NULL")
            print("   ✅ Set default value (algebra) for existing books")
            
            # Commit changes
            conn.commit()
            print("\n✅ Migration completed successfully!")
            print("\nNew feature:")
            print("  • Books now have topics for better organization")
            print("  • Available topics:")
            print("    - algebra")
            print("    - analysis")
            print("    - geometry_topology")
            print("    - logic")
            print("    - applied_mathematics")
            print("\nYou can update book topics in the database or when seeding books.")
        else:
            print("   ⏭️  'topic' column already exists")
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
    print("  BOOK TOPIC MIGRATION")
    print("=" * 70)
    print()
    migrate_database()
