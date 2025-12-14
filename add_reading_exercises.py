"""Add reading completion exercises to sections without exercises.

For sections that have 0 exercises, this script adds a single exercise
that represents "reading completion" for that section. Users can upload
a file (e.g., notes, summary) to mark the section as read and earn points.
"""
from app import create_app
from models import db, Chapter, Exercise

app = create_app()

with app.app_context():
    chapters = Chapter.query.all()
    
    exercises_added = 0
    
    for chapter in chapters:
        chapter_multiplier = 1 + (0.05 * (chapter.number - 1))
        reading_points = int(round(25 * chapter_multiplier))
        
        for section in range(1, 8):
            # Check if section has any exercises
            existing_exercises = Exercise.query.filter_by(
                chapter_id=chapter.id,
                section=section
            ).all()
            
            if len(existing_exercises) == 0:
                # Add a reading completion exercise
                reading_exercise = Exercise(
                    chapter_id=chapter.id,
                    section=section,
                    number=1,  # First (and only) exercise in this section
                    difficulty='easy',  # Reading is considered easy
                    points=reading_points  # Points based on chapter multiplier
                )
                db.session.add(reading_exercise)
                exercises_added += 1
                print(f'Added reading exercise to Chapter {chapter.number}, Section {section} ({reading_points} pts)')
    
    if exercises_added > 0:
        db.session.commit()
        print(f'\n✅ Successfully added {exercises_added} reading completion exercises!')
    else:
        print('No sections without exercises found.')
