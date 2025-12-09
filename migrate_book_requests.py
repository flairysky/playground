"""Migration script to create book_requests table."""
from app import create_app
from models import db

def migrate():
    app = create_app()
    
    with app.app_context():
        # Create book_requests table
        with db.engine.connect() as conn:
            # Check if table exists
            result = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='book_requests'"))
            table_exists = result.fetchone() is not None
            
            if not table_exists:
                print("Creating book_requests table...")
                conn.execute(db.text("""
                    CREATE TABLE book_requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        book_title VARCHAR(200) NOT NULL,
                        author VARCHAR(200),
                        reason TEXT,
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """))
                conn.commit()
                print("book_requests table created successfully!")
            else:
                print("book_requests table already exists.")
        
        print("Migration completed successfully!")

if __name__ == '__main__':
    migrate()
