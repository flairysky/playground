from app import create_app
from models import db, User, BookRequest, Submission, ReadingSection, ActivityLog, WeeklyPlan

app = create_app()

with app.app_context():
    # Find users
    test_user = User.query.filter_by(username='test').first()
    nadry_user = User.query.filter_by(username='nadry').first()
    
    users_to_delete = [u for u in [test_user, nadry_user] if u]
    
    if not users_to_delete:
        print("No users found to delete")
    else:
        user_ids = [u.id for u in users_to_delete]
        usernames = [u.username for u in users_to_delete]
        
        # Delete related data first
        book_requests_deleted = BookRequest.query.filter(BookRequest.user_id.in_(user_ids)).delete(synchronize_session=False)
        submissions_deleted = Submission.query.filter(Submission.user_id.in_(user_ids)).delete(synchronize_session=False)
        reading_sections_deleted = ReadingSection.query.filter(ReadingSection.user_id.in_(user_ids)).delete(synchronize_session=False)
        activity_logs_deleted = ActivityLog.query.filter(ActivityLog.user_id.in_(user_ids)).delete(synchronize_session=False)
        weekly_plans_deleted = WeeklyPlan.query.filter(WeeklyPlan.user_id.in_(user_ids)).delete(synchronize_session=False)
        
        # Delete users
        for user in users_to_delete:
            db.session.delete(user)
        
        db.session.commit()
        
        print(f"Successfully deleted users: {usernames}")
        print(f"  - Book requests deleted: {book_requests_deleted}")
        print(f"  - Submissions deleted: {submissions_deleted}")
        print(f"  - Reading sections deleted: {reading_sections_deleted}")
        print(f"  - Activity logs deleted: {activity_logs_deleted}")
        print(f"  - Weekly plans deleted: {weekly_plans_deleted}")
