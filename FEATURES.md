# MathTracker Feature Showcase

## 🎯 Core Features Overview

### 1. User Authentication System
```
┌─────────────────────────────────────┐
│  Registration                       │
│  • Username (3-80 chars)            │
│  • Email (validated)                │
│  • Password (6+ chars, hashed)      │
│  • Duplicate checking               │
└─────────────────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│  Login                              │
│  • Username/Password authentication │
│  • "Remember Me" option             │
│  • Protected routes                 │
└─────────────────────────────────────┘
```

### 2. Dashboard Layout
```
┌───────────────────────────────────────────────────────────┐
│  DASHBOARD                                                │
├──────────────────┬────────────────────────────────────────┤
│  Your Stats      │  Active Weekly Plan                    │
│  • 42 exercises  │  Book: Undergraduate Algebra           │
│  • 🔥 7 day streak│  Chapter 2: Rings                     │
│  • 🏆 12 longest │  [████████░░] 80%                      │
│                  │  8/10 exercises | 2 days left          │
├──────────────────┴────────────────────────────────────────┤
│  Your Badges                                              │
│  [🎯 First Steps] [📚 Getting Serious] [⚡ One-Week Streak]│
├───────────────────────────────────────────────────────────┤
│  Activity Calendar (Last 60 Days)                         │
│  [■][■][□][□][■][■][■][■][□][■][■][■]... (green carpet) │
├───────────────────────────────────────────────────────────┤
│  Your Books                                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │
│  │ Undergraduate│ │ Real Analysis│ │ Linear Algebra│     │
│  │ Algebra      │ │              │ │               │     │
│  │ [████░░] 65% │ │ [██░░░░] 30% │ │ [███░░░] 45% │     │
│  └──────────────┘ └──────────────┘ └──────────────┘      │
└───────────────────────────────────────────────────────────┘
```

### 3. Book Detail & Upload System
```
┌───────────────────────────────────────────────────────────┐
│  Undergraduate Algebra by Serge Lang                      │
│  [📁 Select File] [Upload Solution]                       │
│  Selected exercises: 3                                    │
├───────────────────────────────────────────────────────────┤
│  ▼ Chapter 1: Groups                       [10 exercises] │
│  ┌────┬──────────┬────────┬────────┬─────────┐           │
│  │ ☑  │ 1.1      │ Easy   │ ✅ Done │ [View]  │           │
│  │ ☑  │ 1.2      │ Easy   │ ✅ Done │ [View]  │           │
│  │ ☐  │ 1.3      │ Medium │ Not Yet│   -     │           │
│  │ ☐  │ 1.4      │ Medium │ Not Yet│   -     │           │
│  └────┴──────────┴────────┴────────┴─────────┘           │
│                                                           │
│  ▼ Chapter 2: Rings                        [8 exercises]  │
│  ┌────┬──────────┬────────┬────────┬─────────┐           │
│  │ ☐  │ 2.1      │ Easy   │ Not Yet│   -     │           │
│  │ ☐  │ 2.2      │ Medium │ Not Yet│   -     │           │
│  └────┴──────────┴────────┴────────┴─────────┘           │
└───────────────────────────────────────────────────────────┘
```

### 4. Weekly Plan System
```
┌─────────────────────────────────────┐  ┌──────────────────────────┐
│  Create New Plan                    │  │  Your Plans              │
│  Book: [Undergraduate Algebra ▼]    │  │  ┌────────────────────┐  │
│  Chapter: [All chapters ▼]          │  │  │ Undergraduate Algebra│
│  Start: [2025-12-09]                │  │  │ Chapter 2: Rings     │
│  End: [2025-12-16]                  │  │  │ [██████░░] 75%      │
│  [Create Plan]                      │  │  │ 6/8 exercises       │
└─────────────────────────────────────┘  │  │ Active | 2 days left│
                                         │  └────────────────────┘  │
                                         │  ┌────────────────────┐  │
                                         │  │ Real Analysis        │
                                         │  │ [████████] 100%     │
                                         │  │ ✅ Completed        │
                                         │  └────────────────────┘  │
                                         └──────────────────────────┘
```

### 5. Leaderboard
```
┌───────────────────────────────────────────────────────────┐
│  🏆 Global Leaderboard                                    │
├────┬──────────────┬──────────┬───────────┬──────────────┤
│Rank│ User         │ Exercises│ 🔥 Streak │ 🏆 Longest   │
├────┼──────────────┼──────────┼───────────┼──────────────┤
│ 🥇1│ alice        │ [127]    │ [14]      │ [21]         │
│ 🥈2│ bob          │ [98]     │ [7]       │ [15]         │
│ 🥉3│ charlie      │ [87]     │ [3]       │ [18]         │
│  4 │ you → dave   │ [42]     │ [7]       │ [12]         │ ← highlighted
│  5 │ eve          │ [31]     │ [0]       │ [9]          │
└────┴──────────────┴──────────┴───────────┴──────────────┘
```

### 6. Activity Calendar (Green Carpet)
```
Activity Calendar - Last 60 Days

Dec 2025
Mon [■][■][□][■][■][■][■][■][■][■]
Tue [□][■][■][■][□][■][■][■][■][■]
Wed [■][■][■][□][■][■][■][□][■][■]
Thu [■][□][■][■][■][■][■][■][■][□]
Fri [■][■][■][■][■][■][□][■][■][■]
Sat [□][□][■][■][■][■][■][■][■][■]
Sun [□][■][□][■][■][■][■][■][■][■]

Legend: □ None | ▪ 1-2 | ▬ 3-5 | ■ 6+
```

### 7. Badge System
```
Your Achievements:

🎯 First Steps
   Completed your first exercise

📚 Getting Serious  
   Completed 20+ exercises

⚡ One-Week Streak
   7+ day streak

🏆 Chapter Finisher
   Completed a full chapter

🔥 Book Grinder
   Completed 100+ exercises

[Locked badges show as greyed out]
```

## 📊 Data Flow

### Submission Flow
```
User selects exercises
       ↓
Uploads file (PDF/image)
       ↓
File saved to uploads/
       ↓
Submissions created in DB
       ↓
ActivityLog updated for today
       ↓
User streak recalculated
       ↓
Dashboard stats refresh
```

### Streak Calculation
```
Check ActivityLog for consecutive days
       ↓
Count backwards from today
       ↓
Stop at first gap (no activity)
       ↓
Update current_streak
       ↓
Update longest_streak if beaten
```

### Weekly Plan Progress
```
Get target exercise IDs from JSON
       ↓
Count how many user has submitted
       ↓
Calculate percentage: completed/total
       ↓
Check if overdue: today > end_date
       ↓
Display progress bar + status badge
```

## 🎨 Color Scheme

```
Primary (Blue):   #0d6efd  - Main actions, links
Success (Green):  #198754  - Completed, positive
Danger (Red):     #dc3545  - Streaks, overdue
Warning (Yellow): #ffc107  - Badges, caution
Info (Cyan):      #0dcaf0  - Information
Dark:             #212529  - Text, navbar
Light:            #f8f9fa  - Background, cards

Activity Calendar:
  Grey:         #ebedf0  - No activity
  Light Green:  #9be9a8  - 1-2 exercises
  Medium Green: #40c463  - 3-5 exercises
  Dark Green:   #30a14e  - 6+ exercises
```

## 🔄 Navigation Flow

```
Landing Page (/)
    ↓
┌───┴──────────────┐
│                  │
Register       Login
│                  │
└───┬──────────────┘
    ↓
Dashboard (/dashboard)
    │
    ├─→ Book Detail (/books/<slug>)
    │       ↓
    │   Submit Solution
    │       ↓
    │   Back to Dashboard
    │
    ├─→ Leaderboard (/leaderboard)
    │
    ├─→ Weekly Plan (/weekly-plan)
    │       ↓
    │   Create Plan
    │       ↓
    │   Back to Dashboard
    │
    └─→ Logout
            ↓
        Landing Page
```

## 📱 Responsive Breakpoints

```
Desktop (≥992px):  3 columns for books, full tables
Tablet (768-991px): 2 columns for books, scrollable tables
Mobile (<768px):    1 column, stacked layout, compact nav
```

## 🎯 Key UI States

### Exercise Status
```
✅ Completed   - Green row, view button enabled
⏳ Not Started - Grey row, checkbox enabled
🔒 Disabled    - Checkbox disabled (already submitted)
```

### Plan Status
```
✅ Completed - Green border, 100% progress
⏰ Active    - Blue border, < 100%, not overdue
⚠️ Overdue   - Red border, deadline passed, incomplete
```

### User Highlight
```
Leaderboard: Current user row has blue background
Badges: Earned badges show full color
        Locked badges show grey/transparent
```

## 🚀 Performance Features

- SQLAlchemy query optimization
- Lazy loading relationships
- Index on foreign keys
- Efficient submission counting (DISTINCT)
- Activity calendar cached per page load
- Progress bars calculated on-demand

## 🔐 Security Measures

- Password hashing (Werkzeug)
- CSRF tokens on all forms
- Login required decorators
- Secure filename sanitization
- File type validation
- File size limits (5MB)
- SQL injection prevention (ORM)

---

**All features are implemented and ready to use!**
