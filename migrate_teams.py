"""
Migration: Add team column to users table and assign teams to existing users.
"""
from app import create_app
from models import db, User
import random

app = create_app()

with app.app_context():
    # Add column if it doesn't exist
    inspector = db.inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    if 'team' not in columns:
        print("Adding team column...")
        with db.engine.connect() as conn:
            conn.execute(db.text("ALTER TABLE users ADD COLUMN team VARCHAR(20)"))
            conn.commit()
        print("✓ Added team column")
    else:
        print("team column already exists")
    
    # Assign teams to users who don't have one
    users_without_team = User.query.filter(
        (User.team == None) | (User.team == '')
    ).all()
    
    if users_without_team:
        print(f"\nAssigning teams to {len(users_without_team)} users...")
        
        for user in users_without_team:
            user.team = random.choice(['red', 'blue', 'green'])
            team_emoji = {'red': '🔴', 'blue': '🔵', 'green': '🟢'}[user.team]
            print(f"  {user.nickname or user.username} -> {team_emoji} {user.team.upper()} Team")
        
        db.session.commit()
        print(f"\n✓ Assigned teams to {len(users_without_team)} users!")
    else:
        print("All users already have teams assigned.")
    
    # Show team distribution
    red_count = User.query.filter_by(team='red').count()
    blue_count = User.query.filter_by(team='blue').count()
    green_count = User.query.filter_by(team='green').count()
    
    print(f"\nTeam Distribution:")
    print(f"  🔴 Red Team: {red_count} users")
    print(f"  🔵 Blue Team: {blue_count} users")
    print(f"  🟢 Green Team: {green_count} users")
    print(f"  Total: {red_count + blue_count + green_count} users")
