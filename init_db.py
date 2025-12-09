"""
Database initialization and seeding script for MathTracker.

This script will:
1. Create all database tables
2. Seed the database with sample books, chapters, and exercises
3. Optionally create a demo user

Run this script before starting the application for the first time.
"""

import os
from datetime import datetime
from app import create_app
from models import db, User, Book, Chapter, Exercise


def init_db():
    """Initialize the database and create all tables."""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if data already exists
        if Book.query.first():
            print("⚠ Database already contains data. Skipping seed.")
            return
        
        print("\nSeeding database with sample data...")
        seed_data()
        print("✓ Database seeded successfully!")


def seed_data():
    """Seed the database with sample books, chapters, and exercises."""
    
    # Create Serge Lang's Undergraduate Algebra book
    algebra_book = Book(
        slug='lang-undergraduate-algebra',
        title='Undergraduate Algebra',
        author='Serge Lang',
        description='A comprehensive introduction to abstract algebra covering groups, rings, fields, and modules. '
                   'This classic textbook provides clear explanations and numerous exercises.'
    )
    db.session.add(algebra_book)
    db.session.flush()  # Get the book ID
    
    # Chapter 1: Groups
    chapter1 = Chapter(
        book_id=algebra_book.id,
        number=1,
        title='Groups'
    )
    db.session.add(chapter1)
    db.session.flush()
    
    # Add exercises for Chapter 1
    for i in range(1, 11):
        difficulty = 'easy' if i <= 3 else 'medium' if i <= 7 else 'hard'
        exercise = Exercise(
            chapter_id=chapter1.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Chapter 2: Rings
    chapter2 = Chapter(
        book_id=algebra_book.id,
        number=2,
        title='Rings'
    )
    db.session.add(chapter2)
    db.session.flush()
    
    # Add exercises for Chapter 2
    for i in range(1, 9):
        difficulty = 'easy' if i <= 2 else 'medium' if i <= 6 else 'hard'
        exercise = Exercise(
            chapter_id=chapter2.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Chapter 3: Fields
    chapter3 = Chapter(
        book_id=algebra_book.id,
        number=3,
        title='Fields'
    )
    db.session.add(chapter3)
    db.session.flush()
    
    # Add exercises for Chapter 3
    for i in range(1, 8):
        difficulty = 'medium' if i <= 4 else 'hard'
        exercise = Exercise(
            chapter_id=chapter3.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Chapter 4: Modules
    chapter4 = Chapter(
        book_id=algebra_book.id,
        number=4,
        title='Modules'
    )
    db.session.add(chapter4)
    db.session.flush()
    
    # Add exercises for Chapter 4
    for i in range(1, 10):
        difficulty = 'easy' if i <= 2 else 'medium' if i <= 6 else 'hard'
        exercise = Exercise(
            chapter_id=chapter4.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Create a second book: Real Analysis
    analysis_book = Book(
        slug='rudin-real-analysis',
        title='Principles of Mathematical Analysis',
        author='Walter Rudin',
        description='Known as "Baby Rudin", this is a classic introduction to real analysis. '
                   'Covers metric spaces, sequences, continuity, differentiation, and integration.'
    )
    db.session.add(analysis_book)
    db.session.flush()
    
    # Chapter 1: The Real and Complex Number Systems
    rudin_ch1 = Chapter(
        book_id=analysis_book.id,
        number=1,
        title='The Real and Complex Number Systems'
    )
    db.session.add(rudin_ch1)
    db.session.flush()
    
    for i in range(1, 13):
        difficulty = 'easy' if i <= 4 else 'medium' if i <= 9 else 'hard'
        exercise = Exercise(
            chapter_id=rudin_ch1.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Chapter 2: Basic Topology
    rudin_ch2 = Chapter(
        book_id=analysis_book.id,
        number=2,
        title='Basic Topology'
    )
    db.session.add(rudin_ch2)
    db.session.flush()
    
    for i in range(1, 11):
        difficulty = 'medium' if i <= 6 else 'hard'
        exercise = Exercise(
            chapter_id=rudin_ch2.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Chapter 3: Numerical Sequences and Series
    rudin_ch3 = Chapter(
        book_id=analysis_book.id,
        number=3,
        title='Numerical Sequences and Series'
    )
    db.session.add(rudin_ch3)
    db.session.flush()
    
    for i in range(1, 15):
        difficulty = 'easy' if i <= 5 else 'medium' if i <= 11 else 'hard'
        exercise = Exercise(
            chapter_id=rudin_ch3.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Create a third book: Linear Algebra
    linear_book = Book(
        slug='axler-linear-algebra',
        title='Linear Algebra Done Right',
        author='Sheldon Axler',
        description='A modern approach to linear algebra that emphasizes vector spaces and linear maps. '
                   'Focuses on understanding rather than computational techniques.'
    )
    db.session.add(linear_book)
    db.session.flush()
    
    # Chapter 1: Vector Spaces
    linear_ch1 = Chapter(
        book_id=linear_book.id,
        number=1,
        title='Vector Spaces'
    )
    db.session.add(linear_ch1)
    db.session.flush()
    
    for i in range(1, 9):
        difficulty = 'easy' if i <= 3 else 'medium'
        exercise = Exercise(
            chapter_id=linear_ch1.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Chapter 2: Finite-Dimensional Vector Spaces
    linear_ch2 = Chapter(
        book_id=linear_book.id,
        number=2,
        title='Finite-Dimensional Vector Spaces'
    )
    db.session.add(linear_ch2)
    db.session.flush()
    
    for i in range(1, 12):
        difficulty = 'easy' if i <= 4 else 'medium' if i <= 9 else 'hard'
        exercise = Exercise(
            chapter_id=linear_ch2.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Chapter 3: Linear Maps
    linear_ch3 = Chapter(
        book_id=linear_book.id,
        number=3,
        title='Linear Maps'
    )
    db.session.add(linear_ch3)
    db.session.flush()
    
    for i in range(1, 10):
        difficulty = 'medium' if i <= 6 else 'hard'
        exercise = Exercise(
            chapter_id=linear_ch3.id,
            number=i,
            difficulty=difficulty
        )
        db.session.add(exercise)
    
    # Commit all changes
    db.session.commit()
    
    print(f"✓ Created {Book.query.count()} books")
    print(f"✓ Created {Chapter.query.count()} chapters")
    print(f"✓ Created {Exercise.query.count()} exercises")


def create_demo_user():
    """Create a demo user for testing."""
    app = create_app()
    
    with app.app_context():
        # Check if demo user exists
        demo_user = User.query.filter_by(username='demo').first()
        if demo_user:
            print("⚠ Demo user already exists.")
            return
        
        print("\nCreating demo user...")
        user = User(
            username='demo',
            email='demo@example.com'
        )
        user.set_password('demo123')
        db.session.add(user)
        db.session.commit()
        
        print("✓ Demo user created!")
        print("  Username: demo")
        print("  Password: demo123")


if __name__ == '__main__':
    print("=" * 60)
    print("MathTracker Database Initialization")
    print("=" * 60)
    
    init_db()
    
    # Ask if user wants to create a demo account
    response = input("\nWould you like to create a demo user? (y/n): ").strip().lower()
    if response == 'y':
        create_demo_user()
    
    print("\n" + "=" * 60)
    print("Setup complete! You can now run the application with:")
    print("  flask run")
    print("or:")
    print("  python app.py")
    print("=" * 60)
