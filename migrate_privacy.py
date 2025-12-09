"""Migration script to add privacy settings to User model."""
from app import create_app
from models import db

def migrate():
    app = create_app()
    
    with app.app_context():
        # Add new columns if they don't exist
        with db.engine.connect() as conn:
            # Check if columns exist
            result = conn.execute(db.text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result]
            
            if 'public_profile' not in columns:
                print("Adding public_profile column...")
                conn.execute(db.text("ALTER TABLE users ADD COLUMN public_profile BOOLEAN DEFAULT 1"))
                conn.commit()
            
            if 'public_stats' not in columns:
                print("Adding public_stats column...")
                conn.execute(db.text("ALTER TABLE users ADD COLUMN public_stats BOOLEAN DEFAULT 1"))
                conn.commit()
            
            if 'public_uploads' not in columns:
                print("Adding public_uploads column...")
                conn.execute(db.text("ALTER TABLE users ADD COLUMN public_uploads BOOLEAN DEFAULT 0"))
                conn.commit()
            
            if 'public_activity' not in columns:
                print("Adding public_activity column...")
                conn.execute(db.text("ALTER TABLE users ADD COLUMN public_activity BOOLEAN DEFAULT 1"))
                conn.commit()
        
        print("Migration completed successfully!")

if __name__ == '__main__':
    migrate()
