"""
Add fake users with activity for testing the leaderboard.
"""
import random
from datetime import datetime, timedelta, date
from app import create_app
from models import db, User, Book, Exercise, Submission, ActivityLog

# Fake user data
FAKE_USERS = [
    {'username': 'alex_math', 'nickname': 'Alex', 'email': 'alex@example.com'},
    {'username': 'bella_student', 'nickname': 'Bella', 'email': 'bella@example.com'},
    {'username': 'carlos_genius', 'nickname': 'Carlos', 'email': 'carlos@example.com'},
    {'username': 'diana_solver', 'nickname': 'Diana', 'email': 'diana@example.com'},
    {'username': 'ethan_pro', 'nickname': 'Ethan', 'email': 'ethan@example.com'},
    {'username': 'fiona_ace', 'nickname': 'Fiona', 'email': 'fiona@example.com'},
    {'username': 'george_keen', 'nickname': 'George', 'email': 'george@example.com'},
    {'username': 'hannah_smart', 'nickname': 'Hannah', 'email': 'hannah@example.com'},
    {'username': 'isaac_brain', 'nickname': 'Isaac', 'email': 'isaac@example.com'},
    {'username': 'julia_whiz', 'nickname': 'Julia', 'email': 'julia@example.com'},
    {'username': 'kevin_master', 'nickname': 'Kevin', 'email': 'kevin@example.com'},
    {'username': 'lily_legend', 'nickname': 'Lily', 'email': 'lily@example.com'},
    {'username': 'marcus_ninja', 'nickname': 'Marcus', 'email': 'marcus@example.com'},
    {'username': 'nina_star', 'nickname': 'Nina', 'email': 'nina@example.com'},
    {'username': 'oliver_champ', 'nickname': 'Oliver', 'email': 'oliver@example.com'},
]

def create_fake_users():
    """Create fake users with realistic activity."""
    app = create_app()
    
    with app.app_context():
        # Get all exercises
        exercises = Exercise.query.all()
        if not exercises:
            print("No exercises found in database. Please add books first.")
            return
        
        print(f"Found {len(exercises)} exercises in database")
        
        # Competitiveness tiers
        high_comp_users = random.sample(FAKE_USERS, k=5)  # 5 high competitors
        low_comp_users = random.sample([u for u in FAKE_USERS if u not in high_comp_users], k=3)  # 3 low
        
        for user_data in FAKE_USERS:
            # Check if user exists
            existing = User.query.filter_by(username=user_data['username']).first()
            if existing:
                print(f"User {user_data['username']} already exists, skipping...")
                continue
            
            # Determine competitiveness tier
            if user_data in high_comp_users:
                competitiveness = random.uniform(0.7, 0.9)
                tier = "HIGH"
            elif user_data in low_comp_users:
                competitiveness = random.uniform(0.1, 0.3)
                tier = "LOW"
            else:
                competitiveness = random.uniform(0.4, 0.6)
                tier = "MEDIUM"
            
            # Randomly assign team
            team = random.choice(['red', 'blue', 'green'])
            
            # Create user
            user = User(
                username=user_data['username'],
                nickname=user_data['nickname'],
                email=user_data['email'],
                public_profile=True,
                public_stats=True,
                public_activity=True,
                show_leaderboard=True,
                is_fake=True,
                competitiveness=competitiveness,
                team=team
            )
            user.set_password('password123')  # Simple password for testing
            
            # Random join date (within last 3 months)
            days_ago = random.randint(10, 90)
            user.date_joined = datetime.utcnow() - timedelta(days=days_ago)
            
            db.session.add(user)
            db.session.flush()  # Get user.id
            
            # Generate random activity
            # Each user solves between 5-50 exercises
            num_exercises = random.randint(5, 50)
            selected_exercises = random.sample(exercises, min(num_exercises, len(exercises)))
            
            # Track unique dates for activity logs
            activity_dates = set()
            
            for i, exercise in enumerate(selected_exercises):
                # Create submission with random date (within user's lifetime)
                days_since_join = (datetime.utcnow() - user.date_joined).days
                if days_since_join > 0:
                    submission_days_ago = random.randint(0, days_since_join)
                else:
                    submission_days_ago = 0
                
                submission_date = datetime.utcnow() - timedelta(days=submission_days_ago)
                
                submission = Submission(
                    user_id=user.id,
                    exercise_id=exercise.id,
                    filename=f'fake_solution_{user.id}_{exercise.id}.pdf',
                    created_at=submission_date,
                    status='submitted'
                )
                db.session.add(submission)
                
                # Track the date for activity log
                activity_dates.add(submission_date.date())
            
            # Create activity logs for each unique date
            for activity_date in activity_dates:
                activity_log = ActivityLog(
                    user_id=user.id,
                    date=activity_date,
                    exercises_done=1  # At least 1 exercise per day
                )
                db.session.add(activity_log)
            
            # Update streak
            user.streak_days = random.randint(0, 15)
            user.longest_streak = random.randint(user.streak_days, 30)
            
            print(f"Created user: {user.nickname} ({user.username}) - {tier} competitiveness ({competitiveness:.2f}) - {len(selected_exercises)} exercises")
        
        # Commit all changes
        db.session.commit()
        print(f"\n✓ Successfully created {len(FAKE_USERS)} fake users!")

if __name__ == '__main__':
    create_fake_users()
