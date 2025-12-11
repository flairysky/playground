"""
Add Complex Analysis by Serge Lang (4th Edition) to the database.
"""
from app import create_app
from models import db, Book, Chapter, Exercise

def add_complex_analysis():
    """Add Complex Analysis book with Chapter 1 and its sections."""
    app = create_app()
    
    with app.app_context():
        # Check if book already exists
        existing_book = Book.query.filter_by(slug='complex-analysis-lang').first()
        if existing_book:
            print(f"Book already exists: {existing_book.title}")
            return
        
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
        db.session.flush()  # Get book.id
        
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
        
        # Subchapters with exercise counts: [10, 13, 4, 7, 0, 1, 0]
        subchapters = [
            {'number': 1.1, 'title': 'Definition', 'exercises': 10},
            {'number': 1.2, 'title': 'Polar Form', 'exercises': 13},
            {'number': 1.3, 'title': 'Complex Valued Functions', 'exercises': 4},
            {'number': 1.4, 'title': 'Limits and Compact Sets', 'exercises': 7},
            {'number': 1.41, 'title': 'Compact Sets', 'exercises': 0},
            {'number': 1.5, 'title': 'Complex Differentiability', 'exercises': 1},
            {'number': 1.6, 'title': 'The Cauchy-Riemann Equations', 'exercises': 0},
            {'number': 1.7, 'title': 'Angles Under Holomorphic Maps', 'exercises': 0}
        ]
        
        # Track exercise number across all subchapters
        exercise_counter = 1
        
        for subchapter in subchapters:
            # Create a "subchapter" as a chapter entry
            sub_ch = Chapter(
                book_id=book.id,
                number=int(subchapter['number'] * 10),  # Convert 1.1 -> 11, 1.2 -> 12, etc.
                title=f"§{int(subchapter['number'])}. {subchapter['title']}" if subchapter['number'] < 1.4 
                      else f"§{subchapter['number']}. {subchapter['title']}"
            )
            db.session.add(sub_ch)
            db.session.flush()
            
            print(f"  Created subchapter {subchapter['number']}: {subchapter['title']} ({subchapter['exercises']} exercises)")
            
            # Add exercises for this subchapter
            for i in range(subchapter['exercises']):
                exercise = Exercise(
                    chapter_id=sub_ch.id,
                    number=exercise_counter,
                    difficulty='medium'  # Default difficulty
                )
                db.session.add(exercise)
                exercise_counter += 1
        
        # Commit all changes
        db.session.commit()
        print(f"\n✓ Successfully added '{book.title}' with Chapter 1 and all subchapters!")
        print(f"  Total exercises in Chapter 1: {exercise_counter - 1}")

if __name__ == '__main__':
    add_complex_analysis()
