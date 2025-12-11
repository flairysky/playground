"""
Migrate database to add points system columns.
"""
from app import create_app
from models import db
from sqlalchemy import inspect

def migrate_points_system():
    """Add points, total_points, and points_earned columns."""
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check and add columns
        with db.engine.connect() as conn:
            # Add points to exercises table
            exercise_columns = [col['name'] for col in inspector.get_columns('exercises')]
            if 'points' not in exercise_columns:
                print("Adding 'points' column to exercises table...")
                conn.execute(db.text('ALTER TABLE exercises ADD COLUMN points INTEGER DEFAULT 0'))
                conn.commit()
                print("✓ Added")
            
            # Add total_points to users table
            user_columns = [col['name'] for col in inspector.get_columns('users')]
            if 'total_points' not in user_columns:
                print("Adding 'total_points' column to users table...")
                conn.execute(db.text('ALTER TABLE users ADD COLUMN total_points INTEGER DEFAULT 0'))
                conn.commit()
                print("✓ Added")
            
            # Add points_earned to submissions table
            submission_columns = [col['name'] for col in inspector.get_columns('submissions')]
            if 'points_earned' not in submission_columns:
                print("Adding 'points_earned' column to submissions table...")
                conn.execute(db.text('ALTER TABLE submissions ADD COLUMN points_earned INTEGER DEFAULT 0'))
                conn.commit()
                print("✓ Added")
        
        print("\n✓ Points system migration completed!")

if __name__ == '__main__':
    migrate_points_system()
