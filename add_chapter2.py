"""
Add Chapter 2: Power Series to Complex Analysis book
"""
from app import create_app
from models import db, Book, Chapter, Exercise
import math

def add_chapter2():
    app = create_app()
    
    with app.app_context():
        # Get the Complex Analysis book
        book = Book.query.filter_by(title='Complex Analysis').first()
        
        if not book:
            print("Error: Complex Analysis book not found!")
            return
        
        # Check if Chapter 2 already exists
        existing_chapter = Chapter.query.filter_by(book_id=book.id, number=2).first()
        if existing_chapter:
            print(f"Deleting existing Chapter 2: {existing_chapter.title}")
            # Delete associated exercises first
            Exercise.query.filter_by(chapter_id=existing_chapter.id).delete()
            db.session.delete(existing_chapter)
            db.session.commit()
        
        # Create Chapter 2
        chapter2 = Chapter(
            book_id=book.id,
            number=2,
            title='Power Series'
        )
        db.session.add(chapter2)
        db.session.flush()
        
        print(f"Created Chapter {chapter2.number}: {chapter2.title}\n")
        
        # 7 sections with exercise counts
        sections = [
            {'section': 1, 'title': '§1. Formal Power Series', 'exercises': 7},
            {'section': 2, 'title': '§2. Convergent Power Series', 'exercises': 13},
            {'section': 3, 'title': '§3. Relations Between Formal and Convergent Series', 'exercises': 6},
            {'section': 4, 'title': '§4. Analytic Functions', 'exercises': 2},
            {'section': 5, 'title': '§5. Differentiation of Power Series', 'exercises': 6},
            {'section': 6, 'title': '§6. The Inverse and Open Mapping Theorems', 'exercises': 7},
            {'section': 7, 'title': '§7. The Local Maximum Modulus Principle', 'exercises': 0}
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
                chapter_multiplier = 1 + (0.05 * (2 - 1))  # Chapter 2 = 1.05
                points = math.ceil(base_points[difficulty] * chapter_multiplier)
                
                exercise = Exercise(
                    chapter_id=chapter2.id,
                    section=section_num,
                    number=ex_num,
                    difficulty=difficulty,
                    points=points
                )
                db.session.add(exercise)
                total_exercises += 1
                print(f"    - Exercise 2.{section_num}.{ex_num} ({difficulty}) - {points} pts")
        
        # Commit all changes
        db.session.commit()
        print(f"\nSuccessfully added Chapter 2 to '{book.title}'!")
        print(f"  Chapter 2 with 7 sections")
        print(f"  Total exercises: {total_exercises}")
        print(f"  Numbering format: 2.section.exercise (e.g., 2.3.5 = Chapter 2, Section 3, Exercise 5)")

if __name__ == '__main__':
    add_chapter2()
