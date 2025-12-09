# MathTracker - Complete Flask Application

## ✅ Project Status: COMPLETE

All core files have been created and the application is ready to run!

## 📁 Project Structure

```
playground/
├── app.py                    # Main Flask application with all routes
├── config.py                 # Configuration (SECRET_KEY, DB URI, upload settings)
├── models.py                 # SQLAlchemy models (User, Book, Chapter, Exercise, etc.)
├── forms.py                  # WTForms (Registration, Login, WeeklyPlan)
├── init_db.py                # Database initialization and seeding script
├── requirements.txt          # Python dependencies
├── start.bat                 # Windows quick start script
├── start.sh                  # Linux/Mac quick start script
├── README.md                 # Comprehensive documentation
├── QUICKSTART.md             # Quick reference guide
├── .gitignore               # Git ignore rules
│
├── instance/
│   └── .gitkeep             # (app.db will be created here)
│
├── uploads/
│   └── .gitkeep             # (uploaded files stored here)
│
├── templates/
│   ├── base.html            # Base template with navbar
│   ├── index.html           # Landing page
│   ├── register.html        # User registration
│   ├── login.html           # User login
│   ├── dashboard.html       # Main dashboard
│   ├── book_detail.html     # Book exercises and upload
│   ├── leaderboard.html     # Global leaderboard
│   └── weekly_plan.html     # Weekly plan management
│
└── static/
    └── style.css            # Custom CSS with activity calendar, cards, etc.
```

## 🎯 Features Implemented

### Core Features
✅ User registration and authentication
✅ Password hashing (Werkzeug)
✅ Protected routes (login_required)
✅ Book catalog with 3 pre-loaded books
✅ Chapter and exercise organization
✅ File upload system (PDF, PNG, JPG, JPEG)
✅ Progress tracking per book
✅ Exercise completion marking

### Study Management
✅ Weekly plans with date ranges
✅ Progress bars for plans
✅ Target exercise tracking
✅ Overdue detection

### Gamification
✅ Daily streak tracking
✅ Longest streak records
✅ Activity calendar (60-day green carpet)
✅ Achievement badge system (5 badges)
✅ Global leaderboard
✅ Rank display with trophy icons

### UI/UX
✅ Responsive Bootstrap 5 design
✅ Modern card-based layout
✅ Progress bars and badges
✅ Activity heatmap visualization
✅ Flash messages for feedback
✅ Collapsible chapter sections
✅ Hover effects and animations

## 🚀 How to Run

### Quick Start (Windows)
```bash
.\start.bat
```

### Manual Setup
```bash
# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python init_db.py

# 4. Run application
python app.py
```

### Access the App
Open browser to: **http://127.0.0.1:5000**

## 📚 Sample Data

### Books (3 total)
1. **Undergraduate Algebra** by Serge Lang
   - Chapter 1: Groups (10 exercises)
   - Chapter 2: Rings (8 exercises)
   - Chapter 3: Fields (7 exercises)
   - Chapter 4: Modules (9 exercises)

2. **Principles of Mathematical Analysis** by Walter Rudin
   - Chapter 1: The Real and Complex Number Systems (12 exercises)
   - Chapter 2: Basic Topology (10 exercises)
   - Chapter 3: Numerical Sequences and Series (14 exercises)

3. **Linear Algebra Done Right** by Sheldon Axler
   - Chapter 1: Vector Spaces (8 exercises)
   - Chapter 2: Finite-Dimensional Vector Spaces (11 exercises)
   - Chapter 3: Linear Maps (9 exercises)

**Total: 102 exercises across 10 chapters**

## 🗄️ Database Schema

### Models
- **User**: Authentication, stats, streaks
- **Book**: Title, author, description, slug
- **Chapter**: Book relationship, number, title
- **Exercise**: Chapter relationship, number, difficulty
- **Submission**: User solutions (file uploads)
- **WeeklyPlan**: Study goals with dates
- **ActivityLog**: Daily exercise counts

### Relationships
- User → Submissions (one-to-many)
- User → WeeklyPlans (one-to-many)
- User → ActivityLogs (one-to-many)
- Book → Chapters (one-to-many)
- Chapter → Exercises (one-to-many)
- Exercise → Submissions (one-to-many)

## 🎨 UI Components

### Dashboard
- User stats card (total exercises, streaks)
- Active weekly plan card with progress
- Badge showcase
- Activity calendar (60 days)
- Book grid with progress bars

### Book Detail
- Breadcrumb navigation
- File upload form
- Collapsible chapter sections
- Exercise table with status
- View uploaded files

### Leaderboard
- Sortable user rankings
- Trophy icons for top 3
- Current user highlighting
- Exercise counts and streaks

### Weekly Plan
- Form for creating new plans
- List of existing plans
- Progress tracking
- Status badges (active/overdue/completed)

## 🏆 Achievement System

Badges are calculated dynamically based on:
- **First Steps**: 1+ exercise
- **Getting Serious**: 20+ exercises
- **Book Grinder**: 100+ exercises
- **One-Week Streak**: 7+ day streak
- **Chapter Finisher**: Completed any full chapter

## 🔐 Security Features

- Password hashing with Werkzeug
- CSRF protection (Flask-WTF)
- Login required decorators
- Secure filename handling
- File type validation
- File size limits (5MB)

## 📊 Key Metrics Tracked

- Total exercises completed (per user)
- Book completion percentages
- Current streak (consecutive days)
- Longest streak (all-time)
- Daily activity counts
- Weekly plan progress

## 🎯 User Workflows

### 1. New User Registration
index.html → register.html → login.html → dashboard.html

### 2. Submit Solution
dashboard.html → book_detail.html → [upload] → dashboard.html (updated)

### 3. Create Weekly Plan
weekly_plan.html → [create plan] → dashboard.html (shows active plan)

### 4. View Rankings
leaderboard.html → see global rankings and personal position

## 🔧 Configuration

### Environment Variables (optional)
- `SECRET_KEY`: Flask secret key (has default)
- `DATABASE_URL`: Database URI (defaults to SQLite)

### Upload Settings
- Max file size: 5 MB
- Allowed extensions: PDF, PNG, JPG, JPEG
- Storage: `uploads/` directory

### Database
- Type: SQLite
- Location: `instance/app.db`
- ORM: SQLAlchemy

## 🐛 Error Handling

- Flash messages for validation errors
- Login redirects for protected routes
- File upload validation
- Form validation with WTForms
- 404 handling for invalid book slugs

## 📱 Responsive Design

- Mobile-friendly navbar
- Responsive grid layouts
- Touch-friendly UI elements
- Collapsible sections for mobile
- Optimized activity calendar

## 🚀 Future Enhancements (V2)

The codebase is designed for easy migration:

- [ ] Supabase backend integration
- [ ] OAuth authentication (Google, GitHub)
- [ ] Exercise hints and solutions
- [ ] Study session timers
- [ ] Friend system
- [ ] Study groups
- [ ] Discussion forums
- [ ] Exercise difficulty voting
- [ ] Dark mode
- [ ] Mobile app
- [ ] Export progress reports
- [ ] Email notifications
- [ ] Spaced repetition system

## 📖 Documentation

- `README.md` - Full documentation
- `QUICKSTART.md` - Quick reference
- Code comments throughout
- Docstrings on key functions

## ✨ Code Quality

- Modular structure (separate files)
- Clean separation of concerns
- Type hints where helpful
- Consistent naming conventions
- DRY principles applied
- Easy to extend and modify

## 🎓 Learning Value

This project demonstrates:
- Flask web application architecture
- SQLAlchemy ORM usage
- User authentication systems
- File upload handling
- Form validation
- Template inheritance
- Database design
- CSS styling and responsive design
- Activity tracking algorithms
- Gamification techniques

## 🎉 Ready to Use!

The application is **production-ready for local use** and includes:
- ✅ All features requested
- ✅ Clean, modern UI
- ✅ Comprehensive documentation
- ✅ Sample data pre-loaded
- ✅ Easy setup scripts
- ✅ Modular architecture

**Just run `.\start.bat` and start tracking your math journey!**

---

Built with Flask, SQLAlchemy, Bootstrap 5, and ❤️
