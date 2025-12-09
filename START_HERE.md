# 🚀 START HERE - MathTracker Setup

## ⚡ Fastest Setup (Windows)

1. Open PowerShell in this directory
2. Run: `.\start.bat`
3. Open browser to: http://127.0.0.1:5000
4. Click "Register" and create your account
5. Start solving exercises!

---

## 📋 Manual Setup (All Platforms)

### Step 1: Create Virtual Environment
```powershell
python -m venv venv
```

### Step 2: Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python init_db.py
```

Choose "y" when asked to create demo user (optional)
- Username: `demo`
- Password: `demo123`

### Step 5: Run Application
```bash
python app.py
```

### Step 6: Open Browser
Navigate to: **http://127.0.0.1:5000**

---

## ✅ What You Get

- **3 pre-loaded math textbooks** with 102 exercises
- **User authentication** (register/login)
- **Progress tracking** per book
- **File uploads** for solutions (PDF, images)
- **Weekly study plans** with deadlines
- **Activity calendar** (GitHub-style green carpet)
- **Streak tracking** (current & longest)
- **Global leaderboard** with rankings
- **Achievement badges** system
- **Modern responsive UI** (Bootstrap 5)

---

## 📚 Pre-loaded Books

1. **Undergraduate Algebra** - Serge Lang (34 exercises)
2. **Principles of Mathematical Analysis** - Walter Rudin (38 exercises)  
3. **Linear Algebra Done Right** - Sheldon Axler (30 exercises)

---

## 🎯 First Steps After Setup

1. **Register** a new account (or use demo/demo123)
2. **Go to Dashboard** - see your stats and available books
3. **Click on a book** - view chapters and exercises
4. **Select exercises** with checkboxes
5. **Upload a solution file** (PDF or image)
6. **Watch your progress grow!**

---

## 📖 Documentation Available

- `README.md` - Full documentation (200+ lines)
- `QUICKSTART.md` - Quick reference guide
- `FEATURES.md` - Visual feature showcase
- `PROJECT_SUMMARY.md` - Technical overview
- `INDEX.md` - Master index

---

## 🆘 Troubleshooting

**"flask" module not found**
→ Activate virtual environment and run `pip install -r requirements.txt`

**Database doesn't exist**
→ Run `python init_db.py`

**Can't upload files**
→ Check that `uploads/` directory exists

**Permission denied (PowerShell)**
→ Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 🎉 That's It!

Your local math exercise tracker is ready to use.

**Happy studying! 📚✨**

---

## 🔗 Quick Links

- Landing page: http://127.0.0.1:5000
- Dashboard: http://127.0.0.1:5000/dashboard
- Leaderboard: http://127.0.0.1:5000/leaderboard
- Weekly Plans: http://127.0.0.1:5000/weekly-plan

---

*Need help? Check README.md or QUICKSTART.md*
