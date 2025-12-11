from app import create_app
from models import db, User, BookRequest, Submission, ReadingSection, ActivityLog, WeeklyPlan

app = create_app()

with app.app_context():
    # Find user
    nadry_user = User.query.filter_by(username='nadry').first()
    
    if not nadry_user:
        print("User 'nadry' not found")
    else:
        user_id = nadry_user.id
        username = nadry_user.username
        
        # Delete related data first
        book_requests_deleted = BookRequest.query.filter_by(user_id=user_id).delete()
        submissions_deleted = Submission.query.filter_by(user_id=user_id).delete()
        reading_sections_deleted = ReadingSection.query.filter_by(user_id=user_id).delete()
        activity_logs_deleted = ActivityLog.query.filter_by(user_id=user_id).delete()
        weekly_plans_deleted = WeeklyPlan.query.filter_by(user_id=user_id).delete()
        
        # Delete user
        db.session.delete(nadry_user)
        
        db.session.commit()
        
        print(f"Successfully deleted user: {username}")
        print(f"  - Book requests deleted: {book_requests_deleted}")
        print(f"  - Submissions deleted: {submissions_deleted}")
        print(f"  - Reading sections deleted: {reading_sections_deleted}")
        print(f"  - Activity logs deleted: {activity_logs_deleted}")
        print(f"  - Weekly plans deleted: {weekly_plans_deleted}")
