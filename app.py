import os
import json
from datetime import datetime, date, timedelta
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import func

from config import Config
from models import db, User, Book, Chapter, Exercise, Submission, WeeklyPlan, ActivityLog
from forms import RegistrationForm, LoginForm, WeeklyPlanForm


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
            user = User(username=form.username.data, email=form.email.data)
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
        
        # Get all books with progress
        books = Book.query.all()
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
        
        return render_template('dashboard.html',
                             books=book_data,
                             active_plans=active_plans,
                             badges=badges,
                             activity_calendar=activity_calendar,
                             recent_submissions=recent_submissions,
                             stats=stats)
    
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
        
        return render_template('book_detail.html',
                             book=book,
                             chapters=chapters,
                             submission_dict=submission_dict)
    
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
        today = date.today()
        
        for ex_id in exercise_ids:
            exercise = Exercise.query.get(int(ex_id))
            if exercise:
                # Check if already submitted
                existing = Submission.query.filter_by(
                    user_id=current_user.id,
                    exercise_id=exercise.id
                ).first()
                
                if not existing:
                    submission = Submission(
                        user_id=current_user.id,
                        exercise_id=exercise.id,
                        filename=new_filename
                    )
                    db.session.add(submission)
                    submission_count += 1
        
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
        
        db.session.commit()
        
        flash(f'Successfully submitted solution for {submission_count} exercise(s)!', 'success')
        return redirect(url_for('book_detail', slug=slug))
    
    @app.route('/leaderboard')
    @login_required
    def leaderboard():
        """Global leaderboard."""
        from datetime import datetime, timedelta
        
        # Get sort parameter (default: total_exercises)
        sort_by = request.args.get('sort', 'total_exercises')
        
        # Get all users
        users = User.query.all()
        
        # Calculate week/month/year start dates
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())  # Monday of current week
        month_start = today.replace(day=1)
        year_start = today.replace(month=1, day=1)
        
        leaderboard_data = []
        for user in users:
            # Get submissions for different time periods
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
            
            leaderboard_data.append({
                'user': user,
                'total_exercises': user.get_total_exercises_completed(),
                'streak': user.streak_days,
                'longest_streak': user.longest_streak,
                'week_exercises': week_submissions,
                'month_exercises': month_submissions,
                'year_exercises': year_submissions
            })
        
        # Sort based on selected criteria
        if sort_by == 'total_exercises':
            leaderboard_data.sort(key=lambda x: x['total_exercises'], reverse=True)
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
        
        return render_template('leaderboard.html', leaderboard=leaderboard_data, sort_by=sort_by)
    
    @app.route('/weekly-plan', methods=['GET', 'POST'])
    @login_required
    def weekly_plan():
        """Create and view weekly plans."""
        form = WeeklyPlanForm()
        
        # Populate book choices
        books = Book.query.all()
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
        
        return render_template('weekly_plan.html', form=form, plans=plans)
    
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
            # Update privacy settings
            current_user.public_profile = 'public_profile' in request.form
            current_user.public_stats = 'public_stats' in request.form
            current_user.public_uploads = 'public_uploads' in request.form
            current_user.public_activity = 'public_activity' in request.form
            
            db.session.commit()
            flash('Settings updated successfully!', 'success')
            return redirect(url_for('settings'))
        
        return render_template('settings.html')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
