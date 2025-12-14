import os
import json
from datetime import datetime, date, timedelta
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import func

from config import Config
from models import db, User, Book, Chapter, Exercise, Submission, WeeklyPlan, ActivityLog
from forms import RegistrationForm, LoginForm, WeeklyPlanForm
from companions import get_login_message, get_upload_message


def create_app(config_class=Config):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure instance and upload folders exist
    os.makedirs(os.path.join(app.instance_path), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    
    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Helper functions
    def allowed_file(filename):
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
    def get_user_badges(user):
        """Calculate and return badges for a user."""
        badges = []
        total_exercises = user.get_total_exercises_completed()
        
        # First Steps badge
        if total_exercises >= 1:
            badges.append({
                'name': 'First Steps',
                'description': 'Completed your first exercise',
                'icon': '🎯',
                'color': 'success'
            })
        
        # Getting Serious badge
        if total_exercises >= 20:
            badges.append({
                'name': 'Getting Serious',
                'description': 'Completed 20+ exercises',
                'icon': '📚',
                'color': 'primary'
            })
        
        # Book Grinder badge
        if total_exercises >= 100:
            badges.append({
                'name': 'Book Grinder',
                'description': 'Completed 100+ exercises',
                'icon': '🔥',
                'color': 'danger'
            })
        
        # One-Week Streak badge
        if user.streak_days >= 7:
            badges.append({
                'name': 'One-Week Streak',
                'description': '7+ day streak',
                'icon': '⚡',
                'color': 'warning'
            })
        
        # Chapter Finisher badge - check if user completed any full chapter
        # Get all chapters
        chapters = Chapter.query.all()
        completed_chapters = None
        for chapter in chapters:
            total_in_chapter = chapter.exercises.count()
            completed_in_chapter = db.session.query(func.count(Submission.id))\
                .join(Exercise).filter(Exercise.chapter_id == chapter.id, Submission.user_id == user.id).scalar()
            if total_in_chapter > 0 and completed_in_chapter == total_in_chapter:
                completed_chapters = chapter
                break
        
        if completed_chapters:
            badges.append({
                'name': 'Chapter Finisher',
                'description': 'Completed a full chapter',
                'icon': '🏆',
                'color': 'info'
            })
        
        return badges
    
    def update_weekly_plans_on_completion(user_id, book_id):
        """Check if any chapter is completed and update weekly plans to next chapter."""
        import json
        
        # Get active weekly plans for this user and book
        active_plans = WeeklyPlan.query.filter_by(
            user_id=user_id,
            book_id=book_id,
            completed=False
        ).filter(WeeklyPlan.end_date >= date.today()).all()
        
        for plan in active_plans:
            # Only auto-progress for chapterwise and subchapterwise plans
            if plan.plan_mode not in ['chapterwise', 'subchapterwise']:
                continue
            
            # Check if current chapter is 100% complete
            if plan.chapter_id and plan.get_progress() >= 100:
                # Find next chapter
                current_chapter = Chapter.query.get(plan.chapter_id)
                if current_chapter:
                    next_chapter = Chapter.query.filter_by(
                        book_id=book_id,
                        number=current_chapter.number + 1
                    ).first()
                    
                    if next_chapter:
                        # Update plan to next chapter
                        plan.chapter_id = next_chapter.id
                        plan.current_chapter_number = next_chapter.number
                        
                        # Update target exercises to next chapter's exercises
                        if plan.plan_mode == 'chapterwise':
                            # All exercises in next chapter
                            next_exercises = Exercise.query.filter_by(chapter_id=next_chapter.id).all()
                            exercise_ids = [ex.id for ex in next_exercises]
                            plan.target_exercises = json.dumps(exercise_ids)
                        elif plan.plan_mode == 'subchapterwise':
                            # First section of next chapter
                            next_exercises = Exercise.query.filter_by(
                                chapter_id=next_chapter.id,
                                section=1
                            ).all()
                            if next_exercises:
                                exercise_ids = [ex.id for ex in next_exercises]
                                plan.target_exercises = json.dumps(exercise_ids)
    
    def simulate_fake_user_progress(real_user_id, exercises_submitted, points_earned):
        """Simulate progress for fake users when a real user submits exercises."""
        import random
        from datetime import datetime, timedelta
        
        # Don't simulate if the real user is fake
        real_user = User.query.get(real_user_id)
        if not real_user or real_user.is_fake:
            return
        
        # Get all fake users
        fake_users = User.query.filter_by(is_fake=True).all()
        if not fake_users:
            return
        
        # Get all available exercises (that haven't been completed by each fake user)
        all_exercises = Exercise.query.all()
        today = date.today()
        
        for fake_user in fake_users:
            # Determine how many exercises this fake user will complete
            # Based on their competitiveness (10-90% of real user's progress)
            base_percentage = fake_user.competitiveness
            # Add some randomness (±15% variation)
            actual_percentage = random.uniform(max(0.1, base_percentage - 0.15), min(0.9, base_percentage + 0.15))
            
            # Calculate number of exercises for this fake user
            num_exercises = max(1, int(exercises_submitted * actual_percentage))
            
            # Get exercises this fake user hasn't completed yet
            completed_exercise_ids = db.session.query(Submission.exercise_id)\
                .filter(Submission.user_id == fake_user.id).all()
            completed_exercise_ids = [ex_id[0] for ex_id in completed_exercise_ids]
            
            available_exercises = [ex for ex in all_exercises if ex.id not in completed_exercise_ids]
            
            if not available_exercises:
                continue  # This fake user has completed everything
            
            # Randomly select exercises to "complete"
            exercises_to_complete = random.sample(
                available_exercises, 
                min(num_exercises, len(available_exercises))
            )
            
            fake_points_earned = 0
            for exercise in exercises_to_complete:
                # Calculate points for this exercise (simplified - no bonuses for fake users)
                points = exercise.points
                
                # Create submission with slight time variation (within last 6 hours)
                hours_ago = random.randint(0, 6)
                minutes_ago = random.randint(0, 59)
                submission_time = datetime.utcnow() - timedelta(hours=hours_ago, minutes=minutes_ago)
                
                submission = Submission(
                    user_id=fake_user.id,
                    exercise_id=exercise.id,
                    filename=f'ai_solution_{fake_user.id}_{exercise.id}.pdf',
                    created_at=submission_time,
                    status='submitted',
                    points_earned=points
                )
                db.session.add(submission)
                fake_points_earned += points
            
            # Update fake user's total points
            if not fake_user.total_points:
                fake_user.total_points = 0
            fake_user.total_points += fake_points_earned
            
            # Update activity log for fake user
            activity = ActivityLog.query.filter_by(
                user_id=fake_user.id,
                date=today
            ).first()
            
            if activity:
                activity.exercises_done += len(exercises_to_complete)
            else:
                activity = ActivityLog(
                    user_id=fake_user.id,
                    date=today,
                    exercises_done=len(exercises_to_complete)
                )
                db.session.add(activity)
            
            # Small chance to update streak
            if random.random() < 0.3:  # 30% chance
                fake_user.streak_days = min(fake_user.streak_days + 1, 30)
                fake_user.longest_streak = max(fake_user.longest_streak, fake_user.streak_days)
    
    def create_random_fake_users():
        """Create 1-5 random new fake users with activity."""
        import random
        from datetime import datetime, timedelta
        
        # List of possible names for generating fake users
        first_names = [
            'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
            'Isabella', 'William', 'Mia', 'James', 'Charlotte', 'Benjamin', 'Amelia',
            'Lucas', 'Harper', 'Henry', 'Evelyn', 'Alexander', 'Abigail', 'Michael',
            'Emily', 'Daniel', 'Elizabeth', 'Matthew', 'Sofia', 'Jackson', 'Avery',
            'Sebastian', 'Ella', 'David', 'Scarlett', 'Joseph', 'Grace', 'Samuel',
            'Chloe', 'John', 'Victoria', 'Owen', 'Riley', 'Dylan', 'Aria', 'Luke',
            'Lily', 'Gabriel', 'Aubrey', 'Anthony', 'Zoey', 'Isaac', 'Penelope'
        ]
        
        suffixes = [
            'math', 'brain', 'genius', 'pro', 'ace', 'star', 'master', 'champ',
            'whiz', 'solver', 'ninja', 'legend', 'wizard', 'expert', 'scholar',
            'student', 'learner', 'thinker', 'keen', 'smart', 'bright', 'swift'
        ]
        
        # Randomly decide how many users to create (1-5)
        num_users = random.randint(1, 5)
        
        # Get all exercises for assigning initial activity
        all_exercises = Exercise.query.all()
        if not all_exercises:
            return 0
        
        created_count = 0
        today = date.today()
        
        for _ in range(num_users):
            # Generate unique username
            attempts = 0
            while attempts < 50:  # Try up to 50 times to find unique username
                first_name = random.choice(first_names)
                suffix = random.choice(suffixes)
                username = f"{first_name.lower()}_{suffix}"
                email = f"{username}@example.com"
                
                # Check if username exists
                existing = User.query.filter_by(username=username).first()
                if not existing:
                    break
                attempts += 1
            else:
                # Couldn't find unique username after 50 attempts, skip
                continue
            
            # Determine competitiveness tier (same distribution as before)
            tier_roll = random.random()
            if tier_roll < 0.33:  # 33% high
                competitiveness = random.uniform(0.7, 0.9)
            elif tier_roll < 0.53:  # 20% low
                competitiveness = random.uniform(0.1, 0.3)
            else:  # 47% medium
                competitiveness = random.uniform(0.4, 0.6)
            
            # Randomly assign team
            team = random.choice(['red', 'blue', 'green'])
            
            # Randomly assign companion (1-5)
            companion_id = random.randint(1, 5)
            
            # Create user
            user = User(
                username=username,
                nickname=first_name,
                email=email,
                public_profile=True,
                public_stats=True,
                public_activity=True,
                show_leaderboard=True,
                is_fake=True,
                competitiveness=competitiveness,
                team=team,
                companion_id=companion_id
            )
            user.set_password('password123')
            
            # Random join date (joined recently - within last 7 days)
            days_ago = random.randint(0, 7)
            user.date_joined = datetime.utcnow() - timedelta(days=days_ago)
            
            db.session.add(user)
            db.session.flush()  # Get user.id
            
            # Give them some initial activity (1-15 exercises completed)
            num_initial_exercises = random.randint(1, 15)
            selected_exercises = random.sample(all_exercises, min(num_initial_exercises, len(all_exercises)))
            
            total_points = 0
            for exercise in selected_exercises:
                # Random submission date (within their lifetime)
                days_since_join = (datetime.utcnow() - user.date_joined).days
                if days_since_join > 0:
                    submission_days_ago = random.randint(0, days_since_join)
                else:
                    submission_days_ago = 0
                
                submission_date = datetime.utcnow() - timedelta(days=submission_days_ago)
                
                submission = Submission(
                    user_id=user.id,
                    exercise_id=exercise.id,
                    filename=f'ai_solution_{user.id}_{exercise.id}.pdf',
                    created_at=submission_date,
                    status='submitted',
                    points_earned=exercise.points
                )
                db.session.add(submission)
                total_points += exercise.points
            
            # Set total points
            user.total_points = total_points
            
            # Create activity log for today if they did any exercises today
            if random.random() < 0.5:  # 50% chance they were active today
                activity = ActivityLog(
                    user_id=user.id,
                    date=today,
                    exercises_done=random.randint(1, 3)
                )
                db.session.add(activity)
            
            # Random streak
            user.streak_days = random.randint(0, 10)
            user.longest_streak = random.randint(user.streak_days, 20)
            
            created_count += 1
        
        return created_count
    
    def get_activity_calendar(user, days=60):
        """Generate activity calendar data for the last N days."""
        today = date.today()
        calendar_data = []
        
        # Get all activity logs for this user in date range
        start_date = today - timedelta(days=days-1)
        logs = ActivityLog.query.filter(
            ActivityLog.user_id == user.id,
            ActivityLog.date >= start_date,
            ActivityLog.date <= today
        ).all()
        
        # Create a dictionary for quick lookup
        log_dict = {log.date: log.exercises_done for log in logs}
        
        # Generate calendar data
        for i in range(days):
            day = today - timedelta(days=days-1-i)
            exercises = log_dict.get(day, 0)
            
            # Determine color intensity
            if exercises == 0:
                color = 'grey'
            elif exercises <= 2:
                color = 'light-green'
            elif exercises <= 5:
                color = 'medium-green'
            else:
                color = 'dark-green'
            
            calendar_data.append({
                'date': day.strftime('%Y-%m-%d'),
                'exercises': exercises,
                'color': color
            })
        
        return calendar_data
    
    # Context processor to make companion_message available in all templates
    @app.context_processor
    def inject_companion_message():
        """Inject companion message from session into all templates."""
        companion_message = session.get('companion_message')
        return dict(companion_message=companion_message)
    
    # Routes
    @app.route('/')
    def index():
        """Landing page."""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration."""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                nickname=form.nickname.data if form.nickname.data else None,
                show_leaderboard=form.show_leaderboard.data,
                team=form.team.data,
                companion_id=int(form.companion.data),
                companion_name=form.companion_name.data if form.companion_name.data else None
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            flash(f'Account created for {form.username.data}! You can now log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login."""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=form.remember_me.data)
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard')
            
            return redirect(next_page)
        
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout."""
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard."""
        from datetime import datetime, timedelta
        
        # Set companion message in session on dashboard visit
        if current_user.companion_id and 'companion_message' not in session:
            session['companion_message'] = get_login_message(current_user.companion_id)
        
        # Get only books that the user has in their weekly plans
        user_book_ids = db.session.query(WeeklyPlan.book_id.distinct())\
            .filter(WeeklyPlan.user_id == current_user.id).all()
        user_book_ids = [book_id[0] for book_id in user_book_ids]
        
        # Update weekly plans if any chapters are completed
        for book_id in user_book_ids:
            update_weekly_plans_on_completion(current_user.id, book_id)
        db.session.commit()
        
        books = Book.query.filter(Book.id.in_(user_book_ids)).all() if user_book_ids else []
        book_data = []
        for book in books:
            progress = current_user.get_book_progress(book.id)
            book_data.append({
                'book': book,
                'progress': progress,
                'total_exercises': book.get_total_exercises()
            })
        
        # Get ALL active weekly plans (not just one)
        active_plans = WeeklyPlan.query.filter_by(
            user_id=current_user.id,
            completed=False
        ).filter(WeeklyPlan.end_date >= date.today()).order_by(WeeklyPlan.start_date).all()
        
        # Get badges
        badges = get_user_badges(current_user)
        
        # Get activity calendar
        activity_calendar = get_activity_calendar(current_user)
        
        # Get recent submissions
        recent_submissions = Submission.query.filter_by(user_id=current_user.id)\
            .order_by(Submission.created_at.desc()).limit(5).all()
        
        # Calculate statistics
        total_exercises = current_user.get_total_exercises_completed()
        
        # This week stats
        week_start = date.today() - timedelta(days=date.today().weekday())
        week_submissions = Submission.query.filter(
            Submission.user_id == current_user.id,
            Submission.created_at >= datetime.combine(week_start, datetime.min.time())
        ).count()
        
        # This month stats
        month_start = date.today().replace(day=1)
        month_submissions = Submission.query.filter(
            Submission.user_id == current_user.id,
            Submission.created_at >= datetime.combine(month_start, datetime.min.time())
        ).count()
        
        # This year stats
        year_start = date.today().replace(month=1, day=1)
        year_submissions = Submission.query.filter(
            Submission.user_id == current_user.id,
            Submission.created_at >= datetime.combine(year_start, datetime.min.time())
        ).count()
        
        # Calculate weekly average (from account creation)
        if current_user.date_joined:
            days_since_joined = (datetime.utcnow() - current_user.date_joined).days
            weeks_since_joined = max(1, days_since_joined / 7)
            weekly_average = round(total_exercises / weeks_since_joined, 1)
        else:
            weekly_average = 0
        
        stats = {
            'week': week_submissions,
            'month': month_submissions,
            'year': year_submissions,
            'weekly_average': weekly_average
        }
        
        # Get leaderboard data only if user wants to see it
        leaderboard_data = None
        if current_user.show_leaderboard:
            # Get top 10 users for dashboard mini-leaderboard
            users = User.query.all()
            leaderboard_list = []
            for user in users:
                leaderboard_list.append({
                    'user': user,
                    'display_name': user.get_display_name(),
                    'total_exercises': user.get_total_exercises_completed()
                })
            leaderboard_list.sort(key=lambda x: x['total_exercises'], reverse=True)
            leaderboard_data = leaderboard_list[:10]  # Top 10 only for dashboard
        
        return render_template('dashboard.html',
                             books=book_data,
                             active_plans=active_plans,
                             badges=badges,
                             activity_calendar=activity_calendar,
                             recent_submissions=recent_submissions,
                             stats=stats,
                             leaderboard=leaderboard_data)
    
    @app.route('/books/<slug>')
    @login_required
    def book_detail(slug):
        """Book detail page with chapters and exercises."""
        book = Book.query.filter_by(slug=slug).first_or_404()
        chapters = book.chapters.all()
        
        # Get user's submissions for this book
        submission_dict = {}
        submissions = Submission.query.join(Exercise).join(Chapter)\
            .filter(Submission.user_id == current_user.id, Chapter.book_id == book.id).all()
        
        for sub in submissions:
            submission_dict[sub.exercise_id] = sub
        
        # Get user's completed reading sections for this book
        from models import ReadingSection
        reading_sections_completed = {}
        reading_completions = ReadingSection.query.join(Chapter)\
            .filter(ReadingSection.user_id == current_user.id, Chapter.book_id == book.id).all()
        
        for reading in reading_completions:
            key = f"{reading.chapter_id}_{reading.section}"
            reading_sections_completed[key] = reading
        
        return render_template('book_detail.html',
                             book=book,
                             chapters=chapters,
                             submission_dict=submission_dict,
                             reading_sections_completed=reading_sections_completed)
    
    @app.route('/books/<slug>/submit', methods=['POST'])
    @login_required
    def submit_solution(slug):
        """Handle solution file upload."""
        book = Book.query.filter_by(slug=slug).first_or_404()
        
        # Get selected exercises
        exercise_ids = request.form.getlist('exercises')
        if not exercise_ids:
            flash('Please select at least one exercise.', 'warning')
            return redirect(url_for('book_detail', slug=slug))
        
        # Check if file was uploaded
        if 'solution_file' not in request.files:
            flash('No file uploaded.', 'danger')
            return redirect(url_for('book_detail', slug=slug))
        
        file = request.files['solution_file']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('book_detail', slug=slug))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Allowed: PDF, PNG, JPG, JPEG', 'danger')
            return redirect(url_for('book_detail', slug=slug))
        
        # Save file with unique name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        exercise_str = '_'.join(exercise_ids[:3])  # Limit length
        new_filename = f"user{current_user.id}_ex{exercise_str}_{timestamp}.{extension}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filepath)
        
        # Create submissions for each selected exercise
        submission_count = 0
        total_points_earned = 0
        today = date.today()
        
        # First, collect valid exercises and check which are new
        exercises_to_submit = []
        for ex_id in exercise_ids:
            exercise = Exercise.query.get(int(ex_id))
            if exercise:
                # Check if already submitted
                existing = Submission.query.filter_by(
                    user_id=current_user.id,
                    exercise_id=exercise.id
                ).first()
                
                if not existing:
                    exercises_to_submit.append(exercise)
        
        # Group exercises by section and chapter to detect completions
        sections_completing = set()  # Set of (chapter_id, section) tuples
        chapters_completing = set()  # Set of chapter_ids
        
        for exercise in exercises_to_submit:
            # Check section completion
            if exercise.section:
                section_key = (exercise.chapter_id, exercise.section)
                section_exercises = Exercise.query.filter_by(
                    chapter_id=exercise.chapter_id,
                    section=exercise.section
                ).all()
                
                # Count already completed in this section
                completed_in_section = Submission.query.join(Exercise).filter(
                    Submission.user_id == current_user.id,
                    Exercise.chapter_id == exercise.chapter_id,
                    Exercise.section == exercise.section
                ).count()
                
                # Count how many from this batch are in this section
                batch_in_section = sum(1 for e in exercises_to_submit 
                                      if e.chapter_id == exercise.chapter_id and e.section == exercise.section)
                
                # Will complete after this batch?
                if completed_in_section + batch_in_section == len(section_exercises):
                    sections_completing.add(section_key)
            
            # Check chapter completion
            chapter_exercises = Exercise.query.filter_by(
                chapter_id=exercise.chapter_id
            ).all()
            
            completed_in_chapter = Submission.query.join(Exercise).filter(
                Submission.user_id == current_user.id,
                Exercise.chapter_id == exercise.chapter_id
            ).count()
            
            # Count how many from this batch are in this chapter
            batch_in_chapter = sum(1 for e in exercises_to_submit if e.chapter_id == exercise.chapter_id)
            
            # Will complete after this batch?
            if completed_in_chapter + batch_in_chapter == len(chapter_exercises):
                chapters_completing.add(exercise.chapter_id)
        
        # Now process each exercise with correct completion flags
        for exercise in exercises_to_submit:
            # Check if this is last exercise in section (by number)
            is_last_in_section = False
            if exercise.section:
                section_exercises = Exercise.query.filter_by(
                    chapter_id=exercise.chapter_id,
                    section=exercise.section
                ).order_by(Exercise.number.desc()).first()
                is_last_in_section = (section_exercises and section_exercises.id == exercise.id)
            
            # Check if section will be complete with this batch
            is_section_complete = False
            if exercise.section:
                section_key = (exercise.chapter_id, exercise.section)
                is_section_complete = section_key in sections_completing
            
            # Check if chapter will be complete with this batch
            is_chapter_complete = exercise.chapter_id in chapters_completing
            
            # Calculate points
            points = exercise.calculate_points(
                is_last_in_section=is_last_in_section,
                is_section_complete=is_section_complete,
                is_chapter_complete=is_chapter_complete
            )
            
            submission = Submission(
                user_id=current_user.id,
                exercise_id=exercise.id,
                filename=new_filename,
                points_earned=points
            )
            db.session.add(submission)
            submission_count += 1
            total_points_earned += points
        
        # Update user's total points
        if not current_user.total_points:
            current_user.total_points = 0
        current_user.total_points += total_points_earned
        
        # Update activity log for today
        activity = ActivityLog.query.filter_by(
            user_id=current_user.id,
            date=today
        ).first()
        
        if activity:
            activity.exercises_done += submission_count
        else:
            activity = ActivityLog(
                user_id=current_user.id,
                date=today,
                exercises_done=submission_count
            )
            db.session.add(activity)
        
        # Update streak
        current_user.update_streak(today)
        
        # Check and update weekly plans if chapter is completed
        update_weekly_plans_on_completion(current_user.id, book.id)
        
        # Simulate fake user progress (gamification)
        simulate_fake_user_progress(current_user.id, submission_count, total_points_earned)
        
        # Create new random fake users (1-5)
        new_users_count = create_random_fake_users()
        
        db.session.commit()
        
        # Store companion message in session if user has a companion (for bottom-right display)
        if current_user.companion_id:
            # Check how many different chapters were in this upload
            chapters_in_upload = set(e.chapter_id for e in exercises_to_submit)
            is_large_upload = len(chapters_in_upload) > 1
            companion_msg = get_upload_message(current_user.companion_id, is_large_upload)
            if companion_msg:
                session['companion_message'] = companion_msg
                # Also flash the message
                flash(f"{companion_msg['emoji']} {companion_msg['name']}: {companion_msg['message']}", 'info')
        
        if total_points_earned > 0:
            flash(f'Successfully submitted solution for {submission_count} exercise(s)! You earned {total_points_earned} points!', 'success')
        else:
            flash(f'Successfully submitted solution for {submission_count} exercise(s)!', 'success')
        
        if new_users_count > 0:
            flash(f'🆕 {new_users_count} new competitor(s) joined the platform!', 'info')
        
        return redirect(url_for('book_detail', slug=slug))
    
    @app.route('/books/<slug>/mark-reading/<int:chapter_id>/<int:section>', methods=['POST'])
    @login_required
    def mark_reading_complete(slug, chapter_id, section):
        """Mark a reading-only section as complete and award points."""
        from models import ReadingSection
        
        book = Book.query.filter_by(slug=slug).first_or_404()
        chapter = Chapter.query.get_or_404(chapter_id)
        
        # Verify chapter belongs to book
        if chapter.book_id != book.id:
            flash('Invalid chapter', 'error')
            return redirect(url_for('book_detail', slug=slug))
        
        # Check if already marked as complete
        existing = ReadingSection.query.filter_by(
            user_id=current_user.id,
            chapter_id=chapter_id,
            section=section
        ).first()
        
        if existing:
            # Already completed - unmark it
            current_user.total_points -= existing.points_earned
            db.session.delete(existing)
            db.session.commit()
            flash(f'Reading section unmarked. You lost {existing.points_earned} points.', 'info')
        else:
            # Mark as complete and award points with chapter multiplier
            # Base points for reading sections: 25
            # Chapter multiplier: 5% increase per chapter
            import math
            base_reading_points = 25
            chapter_number = chapter.number
            chapter_multiplier = 1 + (0.05 * (chapter_number - 1))
            reading_points = math.ceil(base_reading_points * chapter_multiplier)
            
            reading_completion = ReadingSection(
                user_id=current_user.id,
                chapter_id=chapter_id,
                section=section,
                points_earned=reading_points
            )
            
            current_user.total_points = (current_user.total_points or 0) + reading_points
            
            db.session.add(reading_completion)
            db.session.commit()
            
            flash(f'Reading section completed! You earned {reading_points} points!', 'success')
        
        return redirect(url_for('book_detail', slug=slug))
    
    @app.route('/leaderboard')
    @login_required
    def leaderboard():

        """Global leaderboard."""
        from datetime import datetime, timedelta
        
        # Get sort parameter (default: total_exercises)
        sort_by = request.args.get('sort', 'total_exercises')
        # Get category filter parameter
        category_filter = request.args.get('category', 'all')
        # Get team filter parameter
        team_filter = request.args.get('team', 'all')
        
        # Get all users (with team filter if specified)
        if team_filter != 'all':
            users = User.query.filter_by(team=team_filter).all()
        else:
            users = User.query.all()
        
        # Calculate week/month/year start dates
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())  # Monday of current week
        month_start = today.replace(day=1)
        year_start = today.replace(month=1, day=1)
        
        leaderboard_data = []
        for user in users:
            # Build base query for submissions
            if category_filter != 'all':
                # Filter submissions by book category
                week_query = db.session.query(Submission).join(Exercise).join(Chapter).join(Book)\
                    .filter(Submission.user_id == user.id, Submission.created_at >= week_start, Book.category == category_filter)
                month_query = db.session.query(Submission).join(Exercise).join(Chapter).join(Book)\
                    .filter(Submission.user_id == user.id, Submission.created_at >= month_start, Book.category == category_filter)
                year_query = db.session.query(Submission).join(Exercise).join(Chapter).join(Book)\
                    .filter(Submission.user_id == user.id, Submission.created_at >= year_start, Book.category == category_filter)
                total_query = db.session.query(Submission).join(Exercise).join(Chapter).join(Book)\
                    .filter(Submission.user_id == user.id, Book.category == category_filter)
                
                week_submissions = week_query.count()
                month_submissions = month_query.count()
                year_submissions = year_query.count()
                total_exercises = total_query.count()
            else:
                # Get all submissions (no category filter)
                week_submissions = Submission.query.filter(
                    Submission.user_id == user.id,
                    Submission.created_at >= week_start
                ).count()
                
                month_submissions = Submission.query.filter(
                    Submission.user_id == user.id,
                    Submission.created_at >= month_start
                ).count()
                
                year_submissions = Submission.query.filter(
                    Submission.user_id == user.id,
                    Submission.created_at >= year_start
                ).count()
                
                total_exercises = user.get_total_exercises_completed()
            
            leaderboard_data.append({
                'user': user,
                'display_name': user.get_display_name(),
                'total_exercises': total_exercises,
                'total_points': user.total_points or 0,
                'streak': user.streak_days,
                'longest_streak': user.longest_streak,
                'week_exercises': week_submissions,
                'month_exercises': month_submissions,
                'year_exercises': year_submissions
            })
        
        # Sort based on selected criteria
        if sort_by == 'total_exercises':
            leaderboard_data.sort(key=lambda x: x['total_exercises'], reverse=True)
        elif sort_by == 'total_points':
            leaderboard_data.sort(key=lambda x: x['total_points'], reverse=True)
        elif sort_by == 'streak':
            leaderboard_data.sort(key=lambda x: x['streak'], reverse=True)
        elif sort_by == 'longest_streak':
            leaderboard_data.sort(key=lambda x: x['longest_streak'], reverse=True)
        elif sort_by == 'week_exercises':
            leaderboard_data.sort(key=lambda x: x['week_exercises'], reverse=True)
        elif sort_by == 'month_exercises':
            leaderboard_data.sort(key=lambda x: x['month_exercises'], reverse=True)
        elif sort_by == 'year_exercises':
            leaderboard_data.sort(key=lambda x: x['year_exercises'], reverse=True)
        else:
            # Default: sort by total exercises
            leaderboard_data.sort(key=lambda x: x['total_exercises'], reverse=True)
        
        # Add rank
        for idx, entry in enumerate(leaderboard_data, 1):
            entry['rank'] = idx
        
        return render_template('leaderboard.html', 
                             leaderboard=leaderboard_data, 
                             sort_by=sort_by,
                             category_filter=category_filter,
                             team_filter=team_filter)
    
    @app.route('/weekly-plan', methods=['GET', 'POST'])
    @login_required
    def weekly_plan():
        """Create and view weekly plans."""
        form = WeeklyPlanForm()
        
        # Populate book choices - keep it simple for the form
        books = Book.query.order_by(Book.title).all()
        form.book_id.choices = [(0, 'Select a book')] + [(book.id, book.title) for book in books]
        
        # Populate chapter choices (will be all chapters for now)
        all_chapters = Chapter.query.all()
        form.start_chapter.choices = [(0, 'Select starting chapter')] + \
            [(ch.id, f"{ch.book.title} - Ch {ch.number}: {ch.title}") for ch in all_chapters]
        
        if form.validate_on_submit():
            book_id = form.book_id.data
            plan_mode = form.plan_mode.data
            deadline_day = form.deadline_day.data
            deadline_hour = form.deadline_hour.data
            deadline_minute = form.deadline_minute.data
            deadline_time = f"{deadline_day}_{deadline_hour}:{deadline_minute}"
            
            # Calculate dates - start today, end in 7 days
            start_date = date.today()
            end_date = start_date + timedelta(days=7)
            
            target_exercise_ids = []
            custom_text = None
            chapter_id = None
            current_chapter_number = None
            
            if plan_mode == 'chapterwise':
                # Get the starting chapter
                start_chapter_id = form.start_chapter.data
                if start_chapter_id and start_chapter_id != 0:
                    chapter = Chapter.query.get(start_chapter_id)
                    if chapter:
                        chapter_id = chapter.id
                        current_chapter_number = chapter.number
                        exercises = Exercise.query.filter_by(chapter_id=chapter.id).all()
                        target_exercise_ids = [ex.id for ex in exercises]
                else:
                    flash('Please select a starting chapter for chapterwise mode.', 'warning')
                    return redirect(url_for('weekly_plan'))
            
            elif plan_mode == 'subchapterwise':
                # Get the starting chapter (same as chapterwise for first week)
                start_chapter_id = form.start_chapter.data
                if start_chapter_id and start_chapter_id != 0:
                    chapter = Chapter.query.get(start_chapter_id)
                    if chapter:
                        chapter_id = chapter.id
                        current_chapter_number = chapter.number
                        exercises = Exercise.query.filter_by(chapter_id=chapter.id).all()
                        target_exercise_ids = [ex.id for ex in exercises]
                else:
                    flash('Please select a starting chapter for subchapterwise mode.', 'warning')
                    return redirect(url_for('weekly_plan'))
            
            elif plan_mode == 'own_pace':
                # User provides custom text
                custom_text = form.custom_exercises.data
                if not custom_text or not custom_text.strip():
                    flash('Please specify the exercises you want to complete this week.', 'warning')
                    return redirect(url_for('weekly_plan'))
                
                # For own_pace, we don't auto-populate exercises
                # User will manually mark them as done
                target_exercise_ids = []
            
            # Create weekly plan
            plan = WeeklyPlan(
                user_id=current_user.id,
                book_id=book_id,
                chapter_id=chapter_id,
                plan_mode=plan_mode,
                current_chapter_number=current_chapter_number,
                deadline_time=deadline_time,
                start_date=start_date,
                end_date=end_date,
                target_exercises=json.dumps(target_exercise_ids) if target_exercise_ids else None,
                custom_text=custom_text
            )
            db.session.add(plan)
            db.session.commit()
            
            flash(f'Weekly plan created successfully! Mode: {plan.get_mode_display()}', 'success')
            return redirect(url_for('dashboard'))
        
        # Get user's plans
        plans = WeeklyPlan.query.filter_by(user_id=current_user.id)\
            .order_by(WeeklyPlan.start_date.desc()).all()
        
        # Get all chapters for filtering in template
        all_chapters = Chapter.query.order_by(Chapter.book_id, Chapter.number).all()
        
        return render_template('weekly_plan.html', form=form, plans=plans, books=books, all_chapters=all_chapters)
    
    @app.route('/weekly-plan/delete/<int:plan_id>', methods=['POST'])
    @login_required
    def delete_weekly_plan(plan_id):
        """Delete a weekly plan and all associated progress for that book."""
        plan = WeeklyPlan.query.get_or_404(plan_id)
        
        # Check if plan belongs to current user
        if plan.user_id != current_user.id:
            flash('You do not have permission to delete this plan.', 'danger')
            return redirect(url_for('weekly_plan'))
        
        book_id = plan.book_id
        
        # Delete all submissions for exercises in this book
        submissions_to_delete = Submission.query.join(Exercise).join(Chapter)\
            .filter(Submission.user_id == current_user.id, Chapter.book_id == book_id).all()
        
        # Calculate points to deduct
        points_to_deduct = sum(sub.points_earned for sub in submissions_to_delete)
        
        # Delete all submissions
        for submission in submissions_to_delete:
            db.session.delete(submission)
        
        # Delete all reading section completions for this book
        from models import ReadingSection
        reading_completions = ReadingSection.query.join(Chapter)\
            .filter(ReadingSection.user_id == current_user.id, Chapter.book_id == book_id).all()
        
        # Add reading points to deduction
        points_to_deduct += sum(reading.points_earned for reading in reading_completions)
        
        # Delete reading completions
        for reading in reading_completions:
            db.session.delete(reading)
        
        # Deduct points from user's total
        if current_user.total_points:
            current_user.total_points = max(0, current_user.total_points - points_to_deduct)
        
        # Delete the weekly plan
        db.session.delete(plan)
        db.session.commit()
        
        flash(f'Weekly plan deleted successfully! Reset all progress for this book and deducted {points_to_deduct} points.', 'success')
        return redirect(url_for('weekly_plan'))
    
    @app.route('/uploads/<filename>')
    @login_required
    def uploaded_file(filename):
        """Serve uploaded files."""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    @app.route('/my-uploads')
    @login_required
    def my_uploads():
        """View all user uploads."""
        # Get all submissions with related data
        submissions = Submission.query.filter_by(user_id=current_user.id)\
            .join(Exercise).join(Chapter).join(Book)\
            .order_by(Submission.created_at.desc()).all()
        
        # Group by file (since one file can be for multiple exercises)
        uploads = {}
        for sub in submissions:
            if sub.filename not in uploads:
                uploads[sub.filename] = {
                    'filename': sub.filename,
                    'created_at': sub.created_at,
                    'exercises': [],
                    'book': sub.exercise.chapter.book
                }
            uploads[sub.filename]['exercises'].append(sub.exercise)
        
        uploads_list = sorted(uploads.values(), key=lambda x: x['created_at'], reverse=True)
        
        return render_template('my_uploads.html', uploads=uploads_list)
    
    @app.route('/profile/<username>')
    @login_required
    def user_profile(username):
        """View user profile page."""
        from datetime import datetime, timedelta
        
        user = User.query.filter_by(username=username).first_or_404()
        
        # Check if profile is public or if viewing own profile
        if not user.public_profile and user.id != current_user.id:
            flash('This profile is private.', 'warning')
            return redirect(url_for('dashboard'))
        
        # Get user stats if public or own profile
        stats_visible = user.public_stats or user.id == current_user.id
        activity_visible = user.public_activity or user.id == current_user.id
        uploads_visible = user.public_uploads or user.id == current_user.id
        
        user_data = {
            'username': user.username,
            'date_joined': user.date_joined,
            'stats_visible': stats_visible,
            'activity_visible': activity_visible,
            'uploads_visible': uploads_visible
        }
        
        if stats_visible:
            # Calculate statistics
            today = datetime.now().date()
            week_start = today - timedelta(days=today.weekday())
            month_start = today.replace(day=1)
            year_start = today.replace(month=1, day=1)
            
            week_submissions = Submission.query.filter(
                Submission.user_id == user.id,
                Submission.created_at >= week_start
            ).count()
            
            month_submissions = Submission.query.filter(
                Submission.user_id == user.id,
                Submission.created_at >= month_start
            ).count()
            
            year_submissions = Submission.query.filter(
                Submission.user_id == user.id,
                Submission.created_at >= year_start
            ).count()
            
            # Calculate weekly average
            weeks_active = max(1, (datetime.now().date() - user.date_joined.date()).days // 7)
            total_exercises = user.get_total_exercises_completed()
            weekly_average = round(total_exercises / weeks_active, 1)
            
            user_data['stats'] = {
                'total_exercises': total_exercises,
                'streak_days': user.streak_days,
                'longest_streak': user.longest_streak,
                'week': week_submissions,
                'month': month_submissions,
                'year': year_submissions,
                'weekly_average': weekly_average
            }
        
        if activity_visible:
            # Get activity calendar
            user_data['activity_calendar'] = get_activity_calendar(user)
            
            # Get badges
            user_data['badges'] = get_user_badges(user)
        
        if uploads_visible:
            # Get user uploads
            submissions = Submission.query.filter_by(user_id=user.id)\
                .join(Exercise).join(Chapter).join(Book)\
                .order_by(Submission.created_at.desc()).all()
            
            uploads = {}
            for sub in submissions:
                if sub.filename not in uploads:
                    uploads[sub.filename] = {
                        'filename': sub.filename,
                        'created_at': sub.created_at,
                        'book': sub.exercise.chapter.book.title,
                        'exercises': []
                    }
                uploads[sub.filename]['exercises'].append(sub.exercise)
            
            user_data['uploads'] = sorted(uploads.values(), key=lambda x: x['created_at'], reverse=True)
        
        return render_template('profile.html', user=user_data, profile_user=user, is_own_profile=(user.id == current_user.id))
    
    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    def settings():
        """User settings page."""
        if request.method == 'POST':
            # Handle nickname change
            new_nickname = request.form.get('nickname', '').strip()
            if new_nickname and new_nickname != current_user.nickname:
                if current_user.can_change_nickname():
                    from datetime import datetime
                    current_user.nickname = new_nickname
                    current_user.nickname_changed_at = datetime.utcnow()
                    flash('Nickname updated successfully!', 'success')
                else:
                    flash('You can only change your nickname once per month.', 'warning')
            
            # Handle companion name change
            new_companion_name = request.form.get('companion_name', '').strip()
            if new_companion_name != current_user.companion_name:
                current_user.companion_name = new_companion_name if new_companion_name else None
                flash('Companion name updated successfully!', 'success')
            
            # Update privacy settings
            current_user.public_profile = 'public_profile' in request.form
            current_user.public_stats = 'public_stats' in request.form
            current_user.public_uploads = 'public_uploads' in request.form
            current_user.public_activity = 'public_activity' in request.form
            current_user.show_leaderboard = 'show_leaderboard' in request.form
            
            db.session.commit()
            flash('Settings updated successfully!', 'success')
            return redirect(url_for('settings'))
        
        # Import timedelta for template
        from datetime import timedelta
        return render_template('settings.html', timedelta=timedelta)
    
    @app.route('/request-book', methods=['POST'])
    @login_required
    def request_book():
        """Handle book request submissions."""
        from models import BookRequest
        
        book_title = request.form.get('book_title', '').strip()
        author = request.form.get('author', '').strip()
        reason = request.form.get('reason', '').strip()
        
        if not book_title:
            flash('Please provide a book title.', 'error')
            return redirect(url_for('weekly_plan'))
        
        # Create book request
        book_request = BookRequest(
            user_id=current_user.id,
            book_title=book_title,
            author=author,
            reason=reason
        )
        
        db.session.add(book_request)
        db.session.commit()
        
        flash('Thank you! Your book request has been submitted. We\'ll review it and try to add it soon!', 'success')
        return redirect(url_for('weekly_plan'))
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
