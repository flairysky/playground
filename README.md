# MathTracker

A local-only Flask web application for tracking progress through mathematics textbook exercises. Think "LeetCode for math books" - upload solutions, track streaks, compete on leaderboards, and maintain weekly study plans.

## Features

- **User Authentication**: Secure registration and login system with password hashing
- **Book Catalog**: Pre-loaded with classic math textbooks (Serge Lang's Algebra, Rudin's Analysis, Axler's Linear Algebra)
- **Progress Tracking**: Visual progress bars showing completion percentage for each book
- **Solution Uploads**: Upload PDF/image files as solutions to exercises
- **Weekly Plans**: Set goals with start/end dates and track progress toward completion
- **Activity Calendar**: GitHub-style "green carpet" showing daily exercise completion
- **Streak Tracking**: Monitor current and longest study streaks
- **Leaderboard**: Global rankings based on total exercises completed
- **Achievement Badges**: Earn badges for milestones (First Steps, Getting Serious, Chapter Finisher, etc.)
- **Modern UI**: Clean, responsive design using Bootstrap 5

## Tech Stack

- **Backend**: Python 3 + Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF + WTForms
- **Frontend**: Bootstrap 5 + Custom CSS
- **Templates**: Jinja2

## Project Structure

```
playground/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # SQLAlchemy database models
├── forms.py               # WTForms form definitions
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── instance/
│   └── app.db            # SQLite database (created on init)
├── uploads/              # User-uploaded solution files
├── templates/
│   ├── base.html         # Base template with navbar
│   ├── index.html        # Landing page
│   ├── register.html     # User registration
│   ├── login.html        # User login
│   ├── dashboard.html    # Main dashboard
│   ├── book_detail.html  # Book exercises view
│   ├── leaderboard.html  # Global leaderboard
│   └── weekly_plan.html  # Weekly plan management
└── static/
    └── style.css         # Custom CSS styles
```

## Installation & Setup

### 1. Clone or Download

```bash
cd "c:\Users\dnadr\OneDrive\desktop\Github Pull\playground"
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Initialize Database

This will create the database and seed it with sample books/exercises:

```bash
python init_db.py
```

When prompted, you can optionally create a demo user:
- **Username**: `demo`
- **Password**: `demo123`

### 6. Run the Application

```bash
flask run
```

Or:

```bash
python app.py
```

The application will be available at: **http://127.0.0.1:5000**

## Usage

### First Time Setup

1. Navigate to http://127.0.0.1:5000
2. Click **Register** and create an account
3. Log in with your credentials
4. You'll be redirected to the dashboard

### Using the App

**Dashboard**: View your stats, active weekly plan, badges, activity calendar, and book progress

**Browse Books**: Click on any book card to view chapters and exercises

**Submit Solutions**:
1. Go to a book detail page
2. Select one or more exercises using checkboxes
3. Upload a solution file (PDF, PNG, JPG, JPEG)
4. Click "Upload Solution"
5. Your progress and activity calendar will update automatically

**Create Weekly Plans**:
1. Navigate to "Weekly Plan" from the navbar
2. Select a book and optionally a specific chapter
3. Set start and end dates
4. Click "Create Plan"
5. Track progress on your dashboard

**View Leaderboard**: Check your ranking against other users

**Earn Badges**: Complete exercises to unlock achievements

## Database Models

- **User**: User accounts with authentication and streak tracking
- **Book**: Math textbooks in the catalog
- **Chapter**: Chapters within books
- **Exercise**: Individual exercises within chapters
- **Submission**: User-uploaded solutions
- **WeeklyPlan**: User-defined weekly study goals
- **ActivityLog**: Daily exercise completion tracking

## Features in Detail

### Progress Tracking
- Per-book completion percentages
- Exercise-level status (completed/not started)
- Visual progress bars throughout the UI

### Streak System
- Automatically tracks consecutive days with at least one completed exercise
- Shows current streak and all-time longest streak
- Updates in real-time with submissions

### Activity Calendar
- Last 60 days of activity
- Color-coded by number of exercises completed per day
- GitHub-style visualization

### Badge System
- **First Steps**: Complete 1+ exercise
- **Getting Serious**: Complete 20+ exercises
- **Book Grinder**: Complete 100+ exercises
- **One-Week Streak**: Maintain 7+ day streak
- **Chapter Finisher**: Complete all exercises in any chapter

## Sample Data

The database is pre-seeded with:

### Books
1. **Undergraduate Algebra** by Serge Lang (4 chapters, 34 exercises)
2. **Principles of Mathematical Analysis** by Walter Rudin (3 chapters, 38 exercises)
3. **Linear Algebra Done Right** by Sheldon Axler (3 chapters, 30 exercises)

Total: **102 exercises** across 10 chapters

## Future Enhancements (Version 2)

This is **Version 1** - a local-only prototype. Planned improvements:

- [ ] Migrate to Supabase for cloud database
- [ ] Add OAuth login (Google, GitHub)
- [ ] Exercise difficulty ratings and filtering
- [ ] Study session timers
- [ ] Social features (friends, study groups)
- [ ] Mobile-responsive improvements
- [ ] Exercise hints and solution discussions
- [ ] Export progress reports
- [ ] Dark mode toggle
- [ ] More books and auto-import from external sources

## Development Notes

### Adding New Books

Edit `init_db.py` and add books/chapters/exercises following the existing pattern, or manually insert via SQLAlchemy in a Python shell:

```python
from app import create_app
from models import db, Book, Chapter, Exercise

app = create_app()
with app.app_context():
    book = Book(slug='new-book', title='New Book', author='Author Name')
    db.session.add(book)
    db.session.commit()
```

### Modular Design

The codebase is structured to make backend migration easy:
- All database operations use SQLAlchemy ORM
- Models are in a separate file
- Business logic is separated from routes
- Authentication uses Flask-Login (easily replaceable)

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'flask'`  
**Solution**: Make sure virtual environment is activated and dependencies are installed

**Issue**: Database doesn't exist  
**Solution**: Run `python init_db.py` to create and seed the database

**Issue**: File upload fails  
**Solution**: Check that the `uploads/` directory exists and is writable

**Issue**: Can't log in  
**Solution**: Verify username and password are correct, or create a new account

## License

This is a prototype project for educational purposes. Free to use and modify.

## Credits

Built with Flask, Bootstrap, and lots of ☕

---

**Happy Learning! 📚✨**
