#!/usr/bin/env python3
"""
Migration script to add nickname system and leaderboard visibility preference to User model.

Adds three new columns:
- nickname: VARCHAR(80) - User's display name (optional)
- nickname_changed_at: DATETIME - Timestamp of last nickname change
- show_leaderboard: BOOLEAN - Whether user wants to see leaderboard on dashboard (default True)
"""

import sqlite3
import sys
from pathlib import Path

def migrate_database():
    """Add nickname and show_leaderboard columns to users table."""
    
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
        # Check if user table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ Users table not found. Please run init_db.py first to create database tables.")
            sys.exit(1)
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        changes_made = False
        
        # Add nickname column if it doesn't exist
        if 'nickname' not in columns:
            print("➕ Adding 'nickname' column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN nickname VARCHAR(80)")
            changes_made = True
            print("   ✅ Added 'nickname' column")
        else:
            print("   ⏭️  'nickname' column already exists")
        
        # Add nickname_changed_at column if it doesn't exist
        if 'nickname_changed_at' not in columns:
            print("➕ Adding 'nickname_changed_at' column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN nickname_changed_at DATETIME")
            changes_made = True
            print("   ✅ Added 'nickname_changed_at' column")
        else:
            print("   ⏭️  'nickname_changed_at' column already exists")
        
        # Add show_leaderboard column if it doesn't exist
        if 'show_leaderboard' not in columns:
            print("➕ Adding 'show_leaderboard' column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN show_leaderboard BOOLEAN DEFAULT 1")
            changes_made = True
            print("   ✅ Added 'show_leaderboard' column")
            
            # Set default value for existing users
            cursor.execute("UPDATE users SET show_leaderboard = 1 WHERE show_leaderboard IS NULL")
            print("   ✅ Set default value (True) for existing users")
        else:
            print("   ⏭️  'show_leaderboard' column already exists")
        
        if changes_made:
            # Commit changes
            conn.commit()
            print("\n✅ Migration completed successfully!")
            print("\nNew features:")
            print("  • Users can now set a display nickname (changeable once per month)")
            print("  • Users can hide the leaderboard widget from their dashboard")
            print("  • All users still appear on the global leaderboard regardless of preference")
        else:
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
    print("  NICKNAME & LEADERBOARD PREFERENCE MIGRATION")
    print("=" * 70)
    print()
    migrate_database()
