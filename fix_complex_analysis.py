"""
Fix the Complex Analysis book structure.
"""
from app import create_app
from models import db, Book, Chapter, Exercise

def fix_complex_analysis():
    """Remove and re-add Complex Analysis with correct structure."""
    app = create_app()
    
    with app.app_context():
        # Find and delete existing book
        book = Book.query.filter_by(slug='complex-analysis-lang').first()
        if book:
            print(f"Deleting existing book: {book.title}")
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
        
        print(f"Created book: {book.title} by {book.author}")
        
        # Chapter 1: Complex Numbers and Functions
        chapter1 = Chapter(
            book_id=book.id,
            number=1,
            title='Complex Numbers and Functions'
        )
        db.session.add(chapter1)
        db.session.flush()
        
        print(f"Created Chapter {chapter1.number}: {chapter1.title}")
        
        # 7 sections with exercise counts: [10, 13, 4, 7, 0, 1, 0]
        # All exercises belong to Chapter 1
        sections = [
            {'title': '§1. Definition', 'exercises': 10},
            {'title': '§2. Polar Form', 'exercises': 13},
            {'title': '§3. Complex Valued Functions', 'exercises': 4},
            {'title': '§4. Limits and Compact Sets', 'exercises': 7},
            {'title': '§5. Complex Differentiability', 'exercises': 1},
            {'title': '§6. The Cauchy-Riemann Equations', 'exercises': 0},
            {'title': '§7. Angles Under Holomorphic Maps', 'exercises': 0}
        ]
        
        total_exercises = 0
        
        # Add all exercises to Chapter 1, tracking which section they belong to
        for section in sections:
            print(f"  Section: {section['title']} ({section['exercises']} exercises)")
            
            # Add exercises for this section - all under chapter1
            for i in range(1, section['exercises'] + 1):
                exercise = Exercise(
                    chapter_id=chapter1.id,
                    number=total_exercises + 1,  # Continuous numbering across all sections
                    difficulty='medium'
                )
                db.session.add(exercise)
                total_exercises += 1
        
        # Commit all changes
        db.session.commit()
        print(f"\n✓ Successfully fixed '{book.title}'!")
        print(f"  Chapter 1: Complex Numbers and Functions")
        print(f"  - 7 sections (§1 through §7)")
        print(f"  - Total exercises: {total_exercises}")

if __name__ == '__main__':
    fix_complex_analysis()
