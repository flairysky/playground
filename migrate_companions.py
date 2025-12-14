"""
Migration script to add companion_id column and assign random companions to existing users.
Run this script once to update the database schema and assign companions.
"""
import os
import sys
from app import create_app
from models import db, User
import random

def migrate_companions():
    """Add companion_id column and assign random companions to existing users."""
    app = create_app()
    
    with app.app_context():
        # Check if companion_id column exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        if 'companion_id' not in columns:
            print("Adding companion_id column to users table...")
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE users ADD COLUMN companion_id INTEGER'))
                conn.commit()
            print("✓ Column added successfully")
        else:
            print("✓ companion_id column already exists")
        
        # Assign random companions to users who don't have one
        users_without_companion = User.query.filter(
            (User.companion_id == None) | (User.companion_id < 1) | (User.companion_id > 5)
        ).all()
        
        if users_without_companion:
            print(f"\nAssigning companions to {len(users_without_companion)} user(s)...")
            for user in users_without_companion:
                user.companion_id = random.randint(1, 5)
                companion_names = {
                    1: "🦉 Wise Owl",
                    2: "🦊 Speedy Fox", 
                    3: "🐻 Strong Bear",
                    4: "🐱 Clever Cat",
                    5: "🦁 Brave Lion"
                }
                print(f"  - {user.username}: {companion_names[user.companion_id]}")
            
            db.session.commit()
            print(f"✓ Assigned companions to {len(users_without_companion)} user(s)")
        else:
            print("\n✓ All users already have companions assigned")
        
        print("\n✅ Migration completed successfully!")

if __name__ == '__main__':
    migrate_companions()
