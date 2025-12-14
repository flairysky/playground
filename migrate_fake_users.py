"""
Migration: Add is_fake and competitiveness fields to users table.
Also mark existing fake users and assign competitiveness levels.
"""
from app import create_app
from models import db, User
import random

app = create_app()

with app.app_context():
    # Add columns if they don't exist
    inspector = db.inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    if 'is_fake' not in columns:
        print("Adding is_fake column...")
        with db.engine.connect() as conn:
            conn.execute(db.text('ALTER TABLE users ADD COLUMN is_fake BOOLEAN DEFAULT 0'))
            conn.commit()
        print("✓ Added is_fake column")
    else:
        print("is_fake column already exists")
    
    if 'competitiveness' not in columns:
        print("Adding competitiveness column...")
        with db.engine.connect() as conn:
            conn.execute(db.text('ALTER TABLE users ADD COLUMN competitiveness FLOAT DEFAULT 0.5'))
            conn.commit()
        print("✓ Added competitiveness column")
    else:
        print("competitiveness column already exists")
    
    # Mark existing fake users
    fake_usernames = [
        'alex_math', 'bella_student', 'carlos_genius', 'diana_solver', 
        'ethan_pro', 'fiona_ace', 'george_keen', 'hannah_smart',
        'isaac_brain', 'julia_whiz', 'kevin_master', 'lily_legend',
        'marcus_ninja', 'nina_star', 'oliver_champ'
    ]
    
    # Competitiveness tiers:
    # High (0.7-0.9): 30% of users - these are your tough competitors
    # Medium (0.4-0.6): 50% of users - average competitors
    # Low (0.1-0.3): 20% of users - slower progressors
    
    high_comp = random.sample(fake_usernames, k=5)  # 5 high competitors
    low_comp = random.sample([u for u in fake_usernames if u not in high_comp], k=3)  # 3 low competitors
    medium_comp = [u for u in fake_usernames if u not in high_comp and u not in low_comp]  # Rest are medium
    
    updated_count = 0
    for username in fake_usernames:
        user = User.query.filter_by(username=username).first()
        if user:
            user.is_fake = True
            
            # Assign competitiveness based on tier
            if username in high_comp:
                user.competitiveness = random.uniform(0.7, 0.9)
                tier = "HIGH"
            elif username in low_comp:
                user.competitiveness = random.uniform(0.1, 0.3)
                tier = "LOW"
            else:
                user.competitiveness = random.uniform(0.4, 0.6)
                tier = "MEDIUM"
            
            updated_count += 1
            print(f"Marked {user.nickname} ({username}) as fake user - Competitiveness: {user.competitiveness:.2f} ({tier})")
    
    db.session.commit()
    
    print(f"\n✓ Migration complete! Updated {updated_count} fake users.")
    print(f"  - High competitors (70-90%): {len(high_comp)} users")
    print(f"  - Medium competitors (40-60%): {len(medium_comp)} users")
    print(f"  - Low competitors (10-30%): {len(low_comp)} users")
