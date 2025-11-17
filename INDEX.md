# 📚 AI Article Scoring App - File Index

## 🎯 Start Here

**New User?** → Read `COMPLETE_GUIDE.md` first

**Quick Start?** → Use `WEBAPP_QUICK_START.md`

---

## 🚀 Applications

### Web App (RECOMMENDED) ⭐
- **`webapp.py`** - Flask web server (main application)
- **Requirements:** `webapp_requirements.txt`
- **Launch:** `python webapp.py`
- **Access:** http://localhost:5000

### Desktop App
- **`article_scoring_app.py`** - Tkinter desktop application
- **Requirements:** `scoring_app_requirements.txt`
- **Launch:** `python article_scoring_app.py`

---

## 📖 Documentation

### Quick Start Guides
1. **`WEBAPP_QUICK_START.md`** - Web app in 3 steps ⭐ START HERE
2. **`QUICK_START.md`** - Desktop app quick start

### Complete Guides
3. **`COMPLETE_GUIDE.md`** - Compare both apps, choose the right one ⭐ READ THIS
4. **`WEBAPP_README.md`** - Comprehensive web app documentation
5. **`SCORING_APP_README.md`** - Comprehensive desktop app documentation

### Reference
6. **`Scoring rubric.txt`** - Detailed scoring criteria (provided by user)

---

## 🌐 Web App Files

### Backend
- **`webapp.py`** - Flask server with API endpoints

### Frontend
- **`templates/index.html`** - Main web interface
- **`static/style.css`** - Styling and animations
- **`static/app.js`** - JavaScript application logic

### Auto-Created
- **`uploads/`** - Temporary file upload directory (auto-created)
- **`article_scores.json`** - Persistent data storage (auto-created)

---

## 📁 Sample Data

- **`sample_articles.csv`** - Example CSV format
- **`sample_articles.txt`** - Example TXT format (web app only)

---

## 📦 Dependencies

- **`webapp_requirements.txt`** - Web app dependencies (Flask, pandas, openpyxl, Werkzeug)
- **`scoring_app_requirements.txt`** - Desktop app dependencies (pandas, openpyxl)

---

## 💾 Data Files

- **`article_scores.json`** - All scoring data (auto-created, shared between both apps)

---

## 🗂️ Directory Structure

```
ai-news-scraper/
├── 📱 Applications
│   ├── webapp.py                    # Web app (RECOMMENDED)
│   └── article_scoring_app.py       # Desktop app
│
├── 🌐 Web App Frontend
│   ├── templates/
│   │   └── index.html              # Main UI
│   └── static/
│       ├── style.css               # Styling
│       └── app.js                  # Frontend logic
│
├── 📖 Documentation
│   ├── COMPLETE_GUIDE.md           # Comprehensive comparison ⭐
│   ├── WEBAPP_QUICK_START.md       # Web quick start ⭐
│   ├── WEBAPP_README.md            # Web full guide
│   ├── QUICK_START.md              # Desktop quick start
│   ├── SCORING_APP_README.md       # Desktop full guide
│   ├── Scoring rubric.txt          # Scoring criteria
│   └── INDEX.md                    # This file
│
├── 📁 Sample Data
│   ├── sample_articles.csv         # CSV example
│   └── sample_articles.txt         # TXT example
│
├── 📦 Dependencies
│   ├── webapp_requirements.txt     # Web app deps
│   └── scoring_app_requirements.txt # Desktop deps
│
├── 💾 Data Storage (auto-created)
│   ├── article_scores.json         # All scores
│   └── uploads/                    # Temp uploads
│
└── 🗂️ Other Files (from previous work)
    ├── scraper.py                   # AI news scraper
    ├── requirements.txt             # Scraper deps
    └── various output files...
```

---

## 🎯 Usage Scenarios

### Scenario 1: First Time User (Solo)
1. Read `WEBAPP_QUICK_START.md`
2. Install: `pip install -r webapp_requirements.txt`
3. Run: `python webapp.py`
4. Import: `sample_articles.csv`
5. Score some articles

### Scenario 2: Team Collaboration
1. Read `COMPLETE_GUIDE.md` → "Team Collaboration" section
2. Host runs web app
3. Share URL with team
4. Import article list
5. Everyone scores simultaneously

### Scenario 3: Research Analysis
1. Score articles using web app
2. Export as JSON: `💾 Export Results` → JSON format
3. Import into Python/R for analysis
4. Calculate inter-rater reliability
5. Analyze patterns by category

### Scenario 4: Migrating from Desktop to Web
1. Keep existing `article_scores.json`
2. Install web app: `pip install -r webapp_requirements.txt`
3. Run: `python webapp.py`
4. Scores automatically available

---

## 📋 Cheat Sheet

### Installation
```powershell
# Web App (recommended)
pip install -r webapp_requirements.txt

# Desktop App
pip install -r scoring_app_requirements.txt
```

### Launch
```powershell
# Web App
python webapp.py
# Then open: http://localhost:5000

# Desktop App
python article_scoring_app.py
```

### Supported File Formats

#### Import
- ✅ CSV (.csv) - Both apps
- ✅ Excel (.xlsx, .xls) - Both apps
- ✅ Text (.txt) - Web app only ⭐

#### Export
- ✅ Text files (.txt in .zip) - Both apps
- ✅ JSON (.json) - Web app only ⭐

---

## 🔑 Key Features

### Both Apps
- Import articles from spreadsheets
- Score on 5 categories (1-10 scale)
- View peer scoring history
- Search and filter articles
- Export scored articles

### Web App Exclusive ⭐
- URL-based access (shareable)
- Import .txt files
- Export as JSON
- Mobile responsive
- Real-time collaboration
- Statistics dashboard
- Drag & drop file upload

---

## 🆘 Help & Troubleshooting

### Getting Started
- **Unsure which to use?** → Read `COMPLETE_GUIDE.md`
- **Want fastest start?** → Follow `WEBAPP_QUICK_START.md`
- **Need detailed info?** → See `WEBAPP_README.md`

### Common Issues
- **Port in use?** → Use different port: `$env:PORT=5001; python webapp.py`
- **Can't import?** → Check file has "URL" column
- **Team can't access?** → Share IP address from server output
- **Need .txt import?** → Use web app (desktop doesn't support it)
- **Need JSON export?** → Use web app (desktop doesn't support it)

### Documentation Hierarchy
1. **Quick Start** → Get running in 3 steps
2. **Complete Guide** → Understand both apps, choose one
3. **Full README** → Comprehensive feature documentation
4. **Rubric** → Understand scoring criteria

---

## 🎓 Learning Path

**Beginner Path:**
1. Start → `WEBAPP_QUICK_START.md`
2. Use sample data → `sample_articles.csv`
3. Score 2-3 articles
4. Explore features
5. Read → `WEBAPP_README.md` for advanced features

**Team Setup Path:**
1. Read → `COMPLETE_GUIDE.md` → "Collaboration" section
2. Follow → `WEBAPP_QUICK_START.md`
3. Share URL with team
4. Import real data
5. Start collaborative scoring

**Analysis Path:**
1. Score articles (web app)
2. Export as JSON
3. Import into analysis tool
4. Calculate statistics
5. Generate reports

---

## 📊 Feature Matrix

| Feature | Desktop | Web | Priority |
|---------|---------|-----|----------|
| CSV Import | ✅ | ✅ | High |
| Excel Import | ✅ | ✅ | High |
| TXT Import | ❌ | ✅ | Medium |
| Text Export | ✅ | ✅ | High |
| JSON Export | ❌ | ✅ | High |
| Scoring UI | ✅ | ✅ | Critical |
| Peer Scores | ✅ | ✅ | Critical |
| Search | ✅ | ✅ | High |
| Filtering | ✅ | ✅ | High |
| Statistics | ❌ | ✅ | Medium |
| URL Sharing | ❌ | ✅ | High |
| Mobile Access | ❌ | ✅ | Medium |
| Drag & Drop | ❌ | ✅ | Low |
| Real-time Collab | ❌ | ✅ | High |

---

## 🎯 Quick Recommendations

**Choose Web App if you:**
- Have 2+ people scoring
- Want JSON exports
- Need mobile access
- Want to import .txt files
- Prefer modern UI

**Choose Desktop App if you:**
- Work alone
- Prefer desktop apps
- Don't need web features
- Want minimal setup

**Recommendation: Use Web App** (covers 90% of use cases)

---

## 📞 Support

Check status bars and console output for error messages.

For questions:
1. Check relevant README file
2. Review COMPLETE_GUIDE.md
3. Check troubleshooting sections

---

## 🔄 Updates & Version History

### Current Version
- ✅ Web app with Flask
- ✅ Desktop app with Tkinter
- ✅ TXT file import (web only)
- ✅ JSON export (web only)
- ✅ Full rubric-based scoring
- ✅ Comprehensive documentation

### Recent Additions
- Added web application
- Added .txt file import support
- Added JSON export format
- Enhanced documentation
- Added mobile responsive design

---

## 🚀 Next Steps

**Right now:**
```powershell
cd c:\Users\sorox\ai-news-scraper
python webapp.py
```

**Then open:** http://localhost:5000

**Start scoring!** 🎯

---

**Last Updated:** November 16, 2025
**Version:** 2.0 (Web App + Desktop App)
