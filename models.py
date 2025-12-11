from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and tracking."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    nickname = db.Column(db.String(80))  # Display name for leaderboard
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    streak_days = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)  # Total points earned from completing exercises
    nickname_changed_at = db.Column(db.DateTime)  # Track when nickname was last changed
    
    # Privacy settings
    public_profile = db.Column(db.Boolean, default=True)
    public_stats = db.Column(db.Boolean, default=True)
    public_uploads = db.Column(db.Boolean, default=False)
    public_activity = db.Column(db.Boolean, default=True)
    show_leaderboard = db.Column(db.Boolean, default=True)  # Whether to show leaderboard on dashboard
    
    # Relationships
    submissions = db.relationship('Submission', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    weekly_plans = db.relationship('WeeklyPlan', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    activity_logs = db.relationship('ActivityLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def can_change_nickname(self):
        """Check if user can change nickname (once per month)."""
        if not self.nickname_changed_at:
            return True
        
        from datetime import datetime, timedelta
        one_month_ago = datetime.utcnow() - timedelta(days=30)
        return self.nickname_changed_at < one_month_ago
    
    def get_display_name(self):
        """Get the display name (nickname or username)."""
        return self.nickname if self.nickname else self.username
    
    def get_total_exercises_completed(self):
        """Get total unique exercises completed by this user."""
        return db.session.query(db.func.count(db.distinct(Submission.exercise_id)))\
            .filter(Submission.user_id == self.id).scalar() or 0
    
    def get_book_progress(self, book_id):
        """Get completion percentage for a specific book."""
        total_exercises = db.session.query(db.func.count(Exercise.id))\
            .join(Chapter).filter(Chapter.book_id == book_id).scalar() or 0
        
        if total_exercises == 0:
            return 0
        
        completed = db.session.query(db.func.count(db.distinct(Submission.exercise_id)))\
            .join(Exercise).join(Chapter)\
            .filter(Submission.user_id == self.id, Chapter.book_id == book_id).scalar() or 0
        
        return int((completed / total_exercises) * 100) if total_exercises > 0 else 0
    
    def update_streak(self, submission_date=None):
        """Update user's streak based on submissions."""
        if submission_date is None:
            submission_date = date.today()
        
        # Get activity logs sorted by date descending
        logs = ActivityLog.query.filter_by(user_id=self.id)\
            .order_by(ActivityLog.date.desc()).all()
        
        if not logs:
            self.streak_days = 1
            self.longest_streak = max(self.longest_streak, 1)
            return
        
        # Calculate current streak
        current_streak = 0
        today = date.today()
        expected_date = today
        
        for log in logs:
            if log.date == expected_date:
                current_streak += 1
                expected_date = date.fromordinal(expected_date.toordinal() - 1)
            else:
                break
        
        self.streak_days = current_streak
        self.longest_streak = max(self.longest_streak, current_streak)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Book(db.Model):
    """Book model for math textbooks."""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='undergraduate')  # high_school, undergraduate, graduate
    topic = db.Column(db.String(100), default='algebra')  # algebra, analysis, geometry_topology, logic, applied_mathematics
    
    # Relationships
    chapters = db.relationship('Chapter', backref='book', lazy='dynamic', 
                              cascade='all, delete-orphan', order_by='Chapter.number')
    weekly_plans = db.relationship('WeeklyPlan', backref='book', lazy='dynamic')
    
    def get_total_exercises(self):
        """Get total number of exercises in this book."""
        return db.session.query(db.func.count(Exercise.id))\
            .join(Chapter).filter(Chapter.book_id == self.id).scalar() or 0
    
    def __repr__(self):
        return f'<Book {self.title}>'


class Chapter(db.Model):
    """Chapter model for organizing exercises."""
    __tablename__ = 'chapters'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    
    # Relationships
    exercises = db.relationship('Exercise', backref='chapter', lazy='dynamic', 
                               cascade='all, delete-orphan', order_by='Exercise.number')
    weekly_plans = db.relationship('WeeklyPlan', backref='chapter', lazy='dynamic')
    
    def __repr__(self):
        return f'<Chapter {self.number}: {self.title}>'


class Exercise(db.Model):
    """Exercise model for individual problems."""
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False, index=True)
    section = db.Column(db.Integer)  # Section number within the chapter (e.g., 1, 2, 3 for §1, §2, §3)
    number = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20))  # 'easy', 'medium', 'hard'
    points = db.Column(db.Integer, default=0)  # Points awarded for completing this exercise
    
    # Relationships
    submissions = db.relationship('Submission', backref='exercise', lazy='dynamic', 
                                 cascade='all, delete-orphan')
    
    def is_completed_by(self, user_id):
        """Check if this exercise has been completed by a user."""
        return Submission.query.filter_by(user_id=user_id, exercise_id=self.id).first() is not None
    
    def get_display_number(self):
        """Get the display number in format chapter.section.exercise (e.g., 1.2.3)."""
        if self.section:
            return f"{self.chapter.number}.{self.section}.{self.number}"
        return f"{self.chapter.number}.{self.number}"
    
    def calculate_points(self, is_last_in_section=False, is_section_complete=False, is_chapter_complete=False):
        """Calculate points for this exercise based on difficulty, bonuses, and chapter multiplier.
        Each chapter increases points by 5% (1.0, 1.05, 1.10, 1.15, etc.)"""
        # Base points by difficulty
        base_points = {
            'easy': 10,
            'medium': 20,
            'hard': 30
        }.get(self.difficulty, 10)
        
        # Chapter multiplier: 5% increase per chapter (Chapter 1 = 1.0, Chapter 2 = 1.05, etc.)
        chapter_number = self.chapter.number
        chapter_multiplier = 1 + (0.05 * (chapter_number - 1))
        
        total_points = base_points
        
        # Last exercise in section bonus
        if is_last_in_section:
            total_points += 15
        
        # Section completion bonus
        if is_section_complete:
            total_points += 50
        
        # Chapter completion bonus
        if is_chapter_complete:
            total_points += 100
        
        # Apply chapter multiplier and round to nearest integer
        total_points = int(round(total_points * chapter_multiplier))
        
        return total_points
    
    def __repr__(self):
        if self.section:
            return f'<Exercise {self.chapter.number}.{self.section}.{self.number}>'
        return f'<Exercise {self.chapter.number}.{self.number}>'


class Submission(db.Model):
    """Submission model for user solutions."""
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    status = db.Column(db.String(20), default='submitted')
    points_earned = db.Column(db.Integer, default=0)  # Points earned for this submission
    
    def __repr__(self):
        return f'<Submission {self.id} by User {self.user_id}>'


class WeeklyPlan(db.Model):
    """Weekly plan model for goal setting."""
    __tablename__ = 'weekly_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=True, index=True)
    plan_mode = db.Column(db.String(20), default='chapterwise')  # 'chapterwise', 'subchapterwise', 'own_pace'
    current_chapter_number = db.Column(db.Integer, nullable=True)  # For tracking progression in chapterwise mode
    deadline_time = db.Column(db.String(5), nullable=True)  # Format: "HH:MM"
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    target_exercises = db.Column(db.Text)  # JSON string of exercise IDs or text description
    custom_text = db.Column(db.Text)  # User's custom exercise description
    completed = db.Column(db.Boolean, default=False)
    auto_renew = db.Column(db.Boolean, default=True)  # Auto-create next week's plan
    
    def get_progress(self):
        """Calculate progress percentage for this plan."""
        import json
        
        if not self.target_exercises:
            return 0
        
        try:
            target_ids = json.loads(self.target_exercises)
        except:
            return 0
        
        if not target_ids:
            return 0
        
        completed_count = db.session.query(db.func.count(db.distinct(Submission.exercise_id)))\
            .filter(Submission.user_id == self.user_id, 
                   Submission.exercise_id.in_(target_ids)).scalar() or 0
        
        return int((completed_count / len(target_ids)) * 100)
    
    def get_completed_count(self):
        """Get number of exercises completed in this plan."""
        import json
        
        if not self.target_exercises:
            return 0
        
        try:
            target_ids = json.loads(self.target_exercises)
        except:
            return 0
        
        return db.session.query(db.func.count(db.distinct(Submission.exercise_id)))\
            .filter(Submission.user_id == self.user_id, 
                   Submission.exercise_id.in_(target_ids)).scalar() or 0
    
    def get_target_count(self):
        """Get total number of target exercises."""
        import json
        
        if not self.target_exercises:
            return 0
        
        try:
            target_ids = json.loads(self.target_exercises)
            return len(target_ids)
        except:
            return 0
    
    def get_book_progress(self):
        """Calculate overall book completion percentage for this plan's book."""
        if not self.book_id:
            return 0
        
        total_exercises = db.session.query(db.func.count(Exercise.id))\
            .join(Chapter).filter(Chapter.book_id == self.book_id).scalar() or 0
        
        if total_exercises == 0:
            return 0
        
        completed = db.session.query(db.func.count(db.distinct(Submission.exercise_id)))\
            .join(Exercise).join(Chapter)\
            .filter(Submission.user_id == self.user_id, Chapter.book_id == self.book_id).scalar() or 0
        
        return int((completed / total_exercises) * 100) if total_exercises > 0 else 0
    
    def days_remaining(self):
        """Get number of days remaining in the plan."""
        if self.deadline_time and '_' in self.deadline_time:
            # Parse deadline_time format: "tuesday_16:05"
            from datetime import datetime, timedelta
            
            day_name, time_str = self.deadline_time.split('_')
            hour, minute = map(int, time_str.split(':'))
            
            # Map day names to weekday numbers (0=Monday, 6=Sunday)
            day_map = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                'friday': 4, 'saturday': 5, 'sunday': 6
            }
            target_weekday = day_map.get(day_name.lower(), 6)
            
            # Get current date and time
            now = datetime.now()
            current_weekday = now.weekday()
            
            # Calculate days until target weekday
            days_ahead = target_weekday - current_weekday
            if days_ahead < 0:  # Target day already passed this week
                days_ahead += 7
            elif days_ahead == 0:  # Target day is today
                # Check if deadline time has passed
                deadline_today = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if now > deadline_today:
                    days_ahead = 7  # Next week
            
            # Calculate exact deadline datetime
            deadline_date = now.date() + timedelta(days=days_ahead)
            deadline_datetime = datetime.combine(deadline_date, datetime.min.time()).replace(hour=hour, minute=minute)
            
            # Calculate time remaining
            time_remaining = deadline_datetime - now
            days = time_remaining.days
            hours = time_remaining.seconds // 3600
            
            # Return days, or 0 if less than a day
            return max(0, days) if days > 0 or hours > 0 else 0
        else:
            # Fallback to end_date
            delta = self.end_date - date.today()
            return max(0, delta.days)
    
    def is_overdue(self):
        """Check if plan is overdue."""
        if self.completed:
            return False
            
        if self.deadline_time and '_' in self.deadline_time:
            from datetime import datetime, timedelta
            
            day_name, time_str = self.deadline_time.split('_')
            hour, minute = map(int, time_str.split(':'))
            
            day_map = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                'friday': 4, 'saturday': 5, 'sunday': 6
            }
            target_weekday = day_map.get(day_name.lower(), 6)
            
            now = datetime.now()
            current_weekday = now.weekday()
            
            # Calculate days until target weekday
            days_ahead = target_weekday - current_weekday
            if days_ahead < 0:
                days_ahead += 7
            elif days_ahead == 0:
                deadline_today = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                return now > deadline_today
            
            # If deadline is in the future this week, not overdue
            return False
        else:
            return date.today() > self.end_date
    
    def time_remaining_text(self):
        """Get human-readable time remaining."""
        if self.deadline_time and '_' in self.deadline_time:
            from datetime import datetime, timedelta
            
            day_name, time_str = self.deadline_time.split('_')
            hour, minute = map(int, time_str.split(':'))
            
            day_map = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                'friday': 4, 'saturday': 5, 'sunday': 6
            }
            target_weekday = day_map.get(day_name.lower(), 6)
            
            now = datetime.now()
            current_weekday = now.weekday()
            
            days_ahead = target_weekday - current_weekday
            if days_ahead < 0:
                days_ahead += 7
            elif days_ahead == 0:
                deadline_today = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if now > deadline_today:
                    days_ahead = 7
            
            deadline_date = now.date() + timedelta(days=days_ahead)
            deadline_datetime = datetime.combine(deadline_date, datetime.min.time()).replace(hour=hour, minute=minute)
            
            time_remaining = deadline_datetime - now
            
            if time_remaining.total_seconds() <= 0:
                return "Overdue"
            
            days = time_remaining.days
            hours = time_remaining.seconds // 3600
            minutes = (time_remaining.seconds % 3600) // 60
            
            if days > 0:
                return f"{days} day(s), {hours} hour(s)"
            elif hours > 0:
                return f"{hours} hour(s), {minutes} minute(s)"
            else:
                return f"{minutes} minute(s)"
        else:
            delta = self.end_date - date.today()
            return f"{max(0, delta.days)} day(s)"
    
    def get_mode_display(self):
        """Get human-readable plan mode."""
        modes = {
            'chapterwise': 'Chapterwise',
            'subchapterwise': 'Subchapterwise',
            'own_pace': 'Own Pace'
        }
        return modes.get(self.plan_mode, 'Unknown')
    
    def __repr__(self):
        return f'<WeeklyPlan {self.id} for User {self.user_id}>'


class ActivityLog(db.Model):
    """Activity log model for tracking daily exercises."""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    exercises_done = db.Column(db.Integer, default=0)
    
    # Unique constraint: one log per user per day
    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='_user_date_uc'),)
    
    def __repr__(self):
        return f'<ActivityLog User {self.user_id} on {self.date}>'


class ReadingSection(db.Model):
    """Model for tracking completion of reading-only sections (sections with 0 exercises)."""
    __tablename__ = 'reading_sections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False, index=True)
    section = db.Column(db.Integer, nullable=False)  # Section number (1-7, etc.)
    points_earned = db.Column(db.Integer, default=25)  # Points for reading section
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: one completion per user per section
    __table_args__ = (db.UniqueConstraint('user_id', 'chapter_id', 'section', name='_user_chapter_section_uc'),)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('reading_sections', lazy='dynamic'))
    chapter = db.relationship('Chapter', backref=db.backref('reading_completions', lazy='dynamic'))
    
    def __repr__(self):
        return f'<ReadingSection User {self.user_id} Chapter {self.chapter_id} Section {self.section}>'


class BookRequest(db.Model):
    """Book request model for users to suggest new books."""
    __tablename__ = 'book_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200))
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('book_requests', lazy='dynamic'))
    
    def __repr__(self):
        return f'<BookRequest {self.book_title} by User {self.user_id}>'
