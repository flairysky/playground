"""Check which sections have no exercises."""
from app import create_app
from models import db, Chapter, Exercise

app = create_app()

with app.app_context():
    chapters = Chapter.query.all()
    
    sections_without_exercises = []
    
    for chapter in chapters:
        print(f'\nChapter {chapter.number}: {chapter.title}')
        for section in range(1, 8):
            exercises = Exercise.query.filter_by(chapter_id=chapter.id, section=section).all()
            print(f'  Section {section}: {len(exercises)} exercises')
            if len(exercises) == 0:
                sections_without_exercises.append((chapter.id, chapter.number, section))
    
    print('\n' + '='*50)
    print('SECTIONS WITHOUT EXERCISES:')
    print('='*50)
    for chapter_id, chapter_num, section in sections_without_exercises:
        print(f'Chapter {chapter_num}, Section {section}')
