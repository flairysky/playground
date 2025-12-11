"""
Migration script to add reading_sections table for tracking completion of reading-only sections.
"""
from app import create_app
from models import db
from sqlalchemy import inspect, text

def migrate():
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check if table already exists
        if 'reading_sections' in inspector.get_table_names():
            print("✓ Table 'reading_sections' already exists")
            return
        
        print("Creating 'reading_sections' table...")
        
        # Create the reading_sections table
        db.session.execute(text("""
            CREATE TABLE reading_sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                chapter_id INTEGER NOT NULL,
                section INTEGER NOT NULL,
                points_earned INTEGER DEFAULT 25,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (chapter_id) REFERENCES chapters(id),
                UNIQUE (user_id, chapter_id, section)
            )
        """))
        
        # Create indexes
        db.session.execute(text("""
            CREATE INDEX idx_reading_sections_user_id ON reading_sections(user_id)
        """))
        
        db.session.execute(text("""
            CREATE INDEX idx_reading_sections_chapter_id ON reading_sections(chapter_id)
        """))
        
        db.session.commit()
        print("✓ Successfully created 'reading_sections' table with indexes")

if __name__ == '__main__':
    migrate()
