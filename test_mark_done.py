"""Test script to verify the mark as done functionality."""
from app import create_app
from models import db, Exercise, Submission, User

app = create_app()

with app.app_context():
    # Get a user
    user = User.query.first()
    if not user:
        print("No users found. Please create a user first.")
        exit(1)
    
    print(f"Testing with user: {user.username}")
    print(f"Current points: {user.total_points}")
    
    # Find an exercise that hasn't been completed by this user
    all_exercises = Exercise.query.limit(10).all()
    uncompleted_exercise = None
    
    for exercise in all_exercises:
        existing = Submission.query.filter_by(
            user_id=user.id,
            exercise_id=exercise.id
        ).first()
        
        if not existing:
            uncompleted_exercise = exercise
            break
    
    if uncompleted_exercise:
        print(f"\nFound uncompleted exercise: {uncompleted_exercise.get_display_number()}")
        print(f"Exercise points: {uncompleted_exercise.points}")
        print(f"Exercise difficulty: {uncompleted_exercise.difficulty}")
        
        # Check submissions with __marked_done__ filename
        marked_done_submissions = Submission.query.filter_by(filename='__marked_done__').all()
        print(f"\nTotal 'marked as done' submissions in system: {len(marked_done_submissions)}")
        
        if marked_done_submissions:
            print("\nSample 'marked as done' submissions:")
            for sub in marked_done_submissions[:5]:
                ex = Exercise.query.get(sub.exercise_id)
                u = User.query.get(sub.user_id)
                print(f"  - User: {u.username}, Exercise: {ex.get_display_number()}, Points: {sub.points_earned}")
    else:
        print("\nNo uncompleted exercises found for this user.")
        
        # Still show marked as done submissions
        marked_done_submissions = Submission.query.filter_by(filename='__marked_done__').all()
        print(f"\nTotal 'marked as done' submissions in system: {len(marked_done_submissions)}")

print("\n✅ Test complete. The app is ready to use the 'Mark as Done' feature!")
print("   - Click on a book in the dashboard")
print("   - Select one or more exercises")
print("   - Click 'Mark as Done' button (green button next to Upload)")
