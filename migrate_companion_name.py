"""
Migration script to add companion_name column to users table.
Run this script once to update the database schema.
"""
import os
import sys
from app import create_app
from models import db, User

def migrate_companion_name():
    """Add companion_name column to users table."""
    app = create_app()
    
    with app.app_context():
        # Check if companion_name column exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        if 'companion_name' not in columns:
            print("Adding companion_name column to users table...")
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE users ADD COLUMN companion_name VARCHAR(80)'))
                conn.commit()
            print("✓ Column added successfully")
        else:
            print("✓ companion_name column already exists")
        
        print("\n✅ Migration completed successfully!")

if __name__ == '__main__':
    migrate_companion_name()
