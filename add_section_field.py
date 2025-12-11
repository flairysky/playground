"""
Add section field to exercises and fix Complex Analysis structure with proper section numbering.
"""
from app import create_app
from models import db, Book, Chapter, Exercise
import math

def add_section_to_exercises():
    """Add section column to exercises table and restructure Complex Analysis."""
    app = create_app()
    
    with app.app_context():
        # Add section column if it doesn't exist
        from sqlalchemy import inspect, Integer
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('exercises')]
        
        if 'section' not in columns:
            print("Adding 'section' column to exercises table...")
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE exercises ADD COLUMN section INTEGER'))
                conn.commit()
            print("✓ Column added")
        
        # Delete existing Complex Analysis book
        book = Book.query.filter_by(slug='complex-analysis-lang').first()
        if book:
            print(f"Deleting existing book: {book.title}")
            # Delete associated weekly plans first
            from models import WeeklyPlan
            WeeklyPlan.query.filter_by(book_id=book.id).delete()
            db.session.delete(book)
            db.session.commit()
        
        # Create the book
        book = Book(
            slug='complex-analysis-lang',
            title='Complex Analysis',
            author='Serge Lang',
            description='Complex Analysis, 4th Edition by Serge Lang',
            category='graduate',
            topic='analysis'
        )
        db.session.add(book)
        db.session.flush()
        
        print(f"\nCreated book: {book.title} by {book.author}")
        
        # Chapter 1: Complex Numbers and Functions
        chapter1 = Chapter(
            book_id=book.id,
            number=1,
            title='Complex Numbers and Functions'
        )
        db.session.add(chapter1)
        db.session.flush()
        
        print(f"Created Chapter {chapter1.number}: {chapter1.title}\n")
        
        # 7 sections with exercise counts
        sections = [
            {'section': 1, 'title': '§1. Definition', 'exercises': 10},
            {'section': 2, 'title': '§2. Polar Form', 'exercises': 8},
            {'section': 3, 'title': '§3. Complex Valued Functions', 'exercises': 4},
            {'section': 4, 'title': '§4. Limits and Compact Sets', 'exercises': 7},
            {'section': 5, 'title': '§5. Complex Differentiability', 'exercises': 0},
            {'section': 6, 'title': '§6. The Cauchy-Riemann Equations', 'exercises': 1},
            {'section': 7, 'title': '§7. Angles Under Holomorphic Maps', 'exercises': 0}
        ]
        
        total_exercises = 0
        
        # Add exercises with section tracking
        for section_data in sections:
            section_num = section_data['section']
            num_exercises = section_data['exercises']
            
            print(f"  {section_data['title']}: {num_exercises} exercises")
            
            # Add exercises for this section with difficulty distribution
            # First 30% easy, next 50% medium, last 20% hard
            for ex_num in range(1, num_exercises + 1):
                # Calculate difficulty based on position in section
                position_ratio = ex_num / num_exercises if num_exercises > 0 else 0
                
                if position_ratio <= 0.30:
                    difficulty = 'easy'
                elif position_ratio <= 0.80:
                    difficulty = 'medium'
                else:
                    difficulty = 'hard'
                
                # Set base points based on difficulty
                base_points = {'easy': 10, 'medium': 20, 'hard': 30}
                # Apply chapter multiplier: Chapter 1 = 1.0, Chapter 2 = 1.05, etc.
                chapter_multiplier = 1 + (0.05 * (1 - 1))  # Chapter 1
                points = math.ceil(base_points[difficulty] * chapter_multiplier)
                
                exercise = Exercise(
                    chapter_id=chapter1.id,
                    section=section_num,
                    number=ex_num,
                    difficulty=difficulty,
                    points=points
                )
                db.session.add(exercise)
                total_exercises += 1
                print(f"    - Exercise 1.{section_num}.{ex_num} ({difficulty}) - {points} pts")
        
        # Commit all changes
        db.session.commit()
        print(f"\nSuccessfully created '{book.title}'!")
        print(f"  Chapter 1 with 7 sections")
        print(f"  Total exercises: {total_exercises}")
        print(f"  Numbering format: 1.section.exercise (e.g., 1.2.3 = Chapter 1, Section 2, Exercise 3)")

if __name__ == '__main__':
    add_section_to_exercises()
