# MathTracker - Quick Start Guide

## 🚀 Fastest Way to Get Started

### Option 1: Use the Start Script (Recommended for Windows)

Just double-click `start.bat` or run:

```bash
.\start.bat
```

This will automatically:
- Create virtual environment
- Install dependencies
- Initialize database
- Start the server

### Option 2: Manual Setup

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python init_db.py

# 5. Run the app
python app.py
```

## 📱 First Login

1. Go to http://127.0.0.1:5000
2. Click **Register**
3. Create your account
4. Start tracking your progress!

## 🎯 Core Workflows

### Submit a Solution

1. Dashboard → Click on a book
2. Select exercise(s) with checkboxes
3. Upload your solution file (PDF/image)
4. Click "Upload Solution"
5. ✅ Exercise marked complete, activity log updated!

### Create Weekly Plan

1. Click "Weekly Plan" in navbar
2. Select book and chapter (optional)
3. Set dates (default: today to +7 days)
4. Click "Create Plan"
5. Track progress on dashboard

### Check Your Rank

Click "Leaderboard" to see global rankings!

## 📊 Database Schema Summary

```
User ←→ Submission ←→ Exercise ←→ Chapter ←→ Book
  ↓
WeeklyPlan
  ↓
ActivityLog
```

## 🎨 UI Components

- **Cards**: Book info, stats, plans
- **Progress Bars**: Book completion, weekly plans
- **Activity Calendar**: GitHub-style green squares
- **Badges**: Achievement pills (colored)
- **Tables**: Exercise lists, leaderboard

## 🔧 Key Files

- `app.py` - Main Flask app, all routes
- `models.py` - Database models (SQLAlchemy)
- `forms.py` - WTForms for login/register/plans
- `config.py` - App configuration
- `init_db.py` - Database initialization script
- `templates/` - Jinja2 HTML templates
- `static/style.css` - Custom CSS

## 📚 Pre-loaded Books

1. **Undergraduate Algebra** - Serge Lang
   - 4 chapters, 34 exercises

2. **Principles of Mathematical Analysis** - Walter Rudin
   - 3 chapters, 38 exercises

3. **Linear Algebra Done Right** - Sheldon Axler
   - 3 chapters, 30 exercises

**Total: 102 exercises** ready to solve!

## 🏆 Achievement Badges

- 🎯 **First Steps** - Complete 1 exercise
- 📚 **Getting Serious** - Complete 20 exercises
- 🔥 **Book Grinder** - Complete 100 exercises
- ⚡ **One-Week Streak** - 7+ day streak
- 🏆 **Chapter Finisher** - Complete all exercises in a chapter

## 💡 Tips

- Upload solutions daily to maintain your streak
- Use weekly plans to stay organized
- Check the leaderboard for motivation
- View your activity calendar to see patterns
- Complete easier exercises first to build momentum

## 🐛 Troubleshooting

**App won't start?**
- Make sure venv is activated
- Run `pip install -r requirements.txt`

**Can't log in?**
- Check username/password
- Create new account if needed

**No books showing?**
- Run `python init_db.py` to seed database

**File upload fails?**
- Check `uploads/` directory exists
- Verify file is PDF/PNG/JPG/JPEG under 5MB

## 🔐 Demo Account

If you chose to create a demo user during setup:

- **Username**: `demo`
- **Password**: `demo123`

## 🎓 Next Steps

1. Register an account
2. Pick a book you're studying
3. Complete 3-5 exercises to get started
4. Create your first weekly plan
5. Come back daily to maintain your streak!

---

**Ready to start? Run `.\start.bat` or `python app.py`**
