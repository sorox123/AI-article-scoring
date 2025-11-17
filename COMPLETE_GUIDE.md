# 🎯 AI Article Scoring App - Complete Guide

## Two Versions Available

### 🖥️ Desktop App (`article_scoring_app.py`)
Traditional desktop application using Tkinter

### 🌐 Web App (`webapp.py`) - **RECOMMENDED**
Modern web-based application with enhanced features

---

## Feature Comparison

| Feature | Desktop App | Web App |
|---------|-------------|---------|
| **Installation** | Python + Tkinter | Python + Flask |
| **Access** | Local machine only | URL-based (local or network) |
| **Platform** | Windows, Mac, Linux | Any device with browser |
| **Mobile Support** | ❌ No | ✅ Yes (responsive design) |
| **Team Collaboration** | Share JSON file manually | Real-time via URL |
| **UI Style** | Native OS widgets | Modern web design |
| **Import Formats** | .csv, .xlsx, .xls | .csv, .xlsx, .xls, **.txt** |
| **Export Formats** | .txt (zip) | .txt (zip) + **.json** |
| **Drag & Drop** | ❌ No | ✅ Yes |
| **Search** | ✅ Yes | ✅ Yes |
| **Filtering** | ✅ Yes | ✅ Yes |
| **Peer Scores** | ✅ Yes | ✅ Yes |
| **Statistics** | ❌ No | ✅ Yes |
| **URL Sharing** | ❌ No | ✅ Yes |

---

## 🚀 Quick Start

### Desktop App
```powershell
cd c:\Users\sorox\ai-news-scraper
pip install -r scoring_app_requirements.txt
python article_scoring_app.py
```

### Web App (RECOMMENDED)
```powershell
cd c:\Users\sorox\ai-news-scraper
pip install -r webapp_requirements.txt
python webapp.py
# Open http://localhost:5000
```

---

## 📁 File Format Support

### CSV Format (Both Apps)
```csv
URL,Title
https://example.com/article1,Article Title 1
https://example.com/article2,Article Title 2
```

### Excel Format (Both Apps)
Standard .xlsx or .xls file with "URL" and optional "Title" columns

### TXT Format (Web App Only) ⭐ NEW
```txt
# Comments start with #
https://example.com/article1
https://example.com/article2,Custom Title
https://example.com/article3
```

**TXT Format Rules:**
- One URL per line
- Optional title: `URL,Title` (comma-separated)
- Comments: Lines starting with `#` are ignored
- Blank lines are ignored

---

## 💾 Export Options

### Text Export (Both Apps)
- Individual `.txt` files per article
- Bundled in `.zip` file
- Includes:
  - Overall average score
  - Category averages
  - Individual peer scores
  - Optional: Notes and timestamps
- Filter by score range (1-3, 4-6, 7-8, 9-10)

### JSON Export (Web App Only) ⭐ NEW
- Structured data format
- Perfect for analysis in Python, R, Excel
- Includes:
  - Export metadata (date, filters)
  - Article URLs
  - Overall averages
  - Category-by-category averages
  - Complete scoring history

**JSON Structure:**
```json
{
  "export_date": "2025-11-16T10:30:00.000000",
  "score_range_filter": "All",
  "articles": [
    {
      "url": "https://example.com/article",
      "overall_average": 7.8,
      "peer_scores_count": 3,
      "category_averages": {
        "accuracy": 8.0,
        "credibility": 7.7,
        "citation": 7.5,
        "reasoning": 8.0,
        "confidence": 7.8
      },
      "individual_scores": [
        {
          "accuracy": 8,
          "credibility": 8,
          "citation": 7,
          "reasoning": 8,
          "confidence": 8,
          "notes": "Well-sourced article",
          "timestamp": "2025-11-16T10:15:00.000000"
        }
      ]
    }
  ]
}
```

---

## 🤝 Collaboration Models

### Desktop App Workflow
1. **Person A** scores articles → `article_scores.json`
2. **Share file** via email/cloud
3. **Person B** copies file → continues scoring
4. **Merge manually** or use latest version

### Web App Workflow ⭐ RECOMMENDED
1. **Admin** runs web server
2. **Share URL** with team (e.g., `http://192.168.1.100:5000`)
3. **Everyone** scores simultaneously
4. **Real-time updates** - all scores visible immediately
5. **No file sharing needed**

---

## 🎯 Use Case Recommendations

### Use Desktop App When:
- ❌ Working alone
- ❌ No need for team collaboration
- ❌ Prefer native OS interface
- ❌ Don't need mobile access

### Use Web App When: ⭐
- ✅ Working with a team
- ✅ Need mobile/tablet access
- ✅ Want real-time collaboration
- ✅ Need JSON export for analysis
- ✅ Want to import .txt files
- ✅ Prefer modern UI/UX

---

## 📊 The 5 Scoring Categories

Both apps use the same rubric-based scoring system:

### 1. Accuracy of Truthfulness (1-10)
Classification as True (10-8), Partially True (7-4), or False (3-1)

### 2. Author and Source Credibility (1-10)
Publisher reputation, author expertise, historical accuracy

### 3. Citation and Evidence Quality (1-10)
Quality and verifiability of references

### 4. Reasoning Transparency (1-10)
Logical coherence and explanation quality

### 5. Confidence Calibration (1-10)
Alignment between stated confidence and correctness

---

## 🔒 Security & Access Control

### Desktop App
- ✅ Runs locally - no network exposure
- ✅ Data stored locally only
- ❌ No multi-user access

### Web App
- ⚠️ **Private URL access** - keep link confidential
- ⚠️ **No authentication** - anyone with URL can access
- ✅ **Local network only** by default
- ✅ Can expose to team on same WiFi/LAN

**Best Practices:**
- Don't expose to public internet
- Share URL only with trusted team members
- Use VPN for remote team members
- Consider adding authentication for sensitive data

---

## 💾 Data Storage

Both apps use the same format: `article_scores.json`

**Structure:**
```json
{
  "https://example.com/article": [
    {
      "accuracy": 8,
      "credibility": 7,
      "citation": 9,
      "reasoning": 8,
      "confidence": 7,
      "notes": "Optional notes",
      "timestamp": "2025-11-16T10:30:00.000000"
    }
  ]
}
```

**Backup:**
```powershell
Copy-Item article_scores.json article_scores_backup_$(Get-Date -Format 'yyyyMMdd').json
```

---

## 📱 Mobile Access (Web App Only)

The web app is fully responsive:

- ✅ **Phones** - Touch-friendly interface
- ✅ **Tablets** - Optimized layout
- ✅ **Desktop** - Full-featured experience

Access from any device on the network!

---

## 🎨 User Interface

### Desktop App
- Native OS widgets (Tkinter)
- Traditional desktop feel
- Windows/Mac/Linux native look

### Web App
- Modern gradient design
- Smooth animations
- Card-based layout
- Modal dialogs
- Interactive sliders
- Responsive grid

---

## 🔧 Technical Details

### Desktop App
- **Framework:** Tkinter (Python standard library)
- **Dependencies:** pandas, openpyxl
- **File:** `article_scoring_app.py` (800+ lines)

### Web App
- **Backend:** Flask (Python web framework)
- **Frontend:** Vanilla JS, HTML5, CSS3
- **Dependencies:** Flask, pandas, openpyxl, Werkzeug
- **Files:**
  - `webapp.py` (backend)
  - `templates/index.html` (UI)
  - `static/style.css` (styling)
  - `static/app.js` (frontend logic)

---

## 📖 Documentation

| Document | Desktop | Web | Purpose |
|----------|---------|-----|---------|
| `SCORING_APP_README.md` | ✅ | ❌ | Desktop app guide |
| `QUICK_START.md` | ✅ | ❌ | Desktop quick start |
| `WEBAPP_README.md` | ❌ | ✅ | Web app guide |
| `WEBAPP_QUICK_START.md` | ❌ | ✅ | Web quick start |
| `Scoring rubric.txt` | ✅ | ✅ | Rubric details |

---

## 🎯 Which Should I Use?

### Choose Web App If:
- You have a team (even 2+ people)
- You want the easiest collaboration
- You need mobile access
- You want JSON exports for analysis
- You prefer modern UI
- You need .txt file import

### Choose Desktop App If:
- You're working completely alone
- You prefer traditional desktop apps
- You don't need any web features
- You want zero network exposure

---

## 🚀 Getting Started

### Recommended: Start with Web App

```powershell
# 1. Install
cd c:\Users\sorox\ai-news-scraper
pip install -r webapp_requirements.txt

# 2. Launch
python webapp.py

# 3. Open browser
# Visit http://localhost:5000

# 4. Import sample data
# Use sample_articles.csv or sample_articles.txt

# 5. Start scoring!
```

### Sample Files Included

- `sample_articles.csv` - CSV format example
- `sample_articles.txt` - TXT format example (web app)

---

## 📈 Workflow Example

### Research Team Workflow (Web App)

1. **Setup Phase**
   - Research lead runs `python webapp.py`
   - Shares URL with team: `http://192.168.1.100:5000`

2. **Import Phase**
   - Lead imports article list (CSV/Excel/TXT)
   - Articles appear for all team members

3. **Scoring Phase**
   - Each team member scores independently
   - Scores saved in real-time
   - Everyone sees updated peer score counts

4. **Analysis Phase**
   - Export JSON with all scores
   - Import into analysis tool (Python/R/SPSS)
   - Calculate inter-rater reliability
   - Analyze patterns by category

5. **Reporting Phase**
   - Export high-scoring articles (9-10)
   - Export low-scoring articles (1-3)
   - Compare credibility patterns

---

## 💡 Pro Tips

### For Desktop App
- Use search to find specific articles quickly
- Export regularly to backup scores
- Share `article_scores.json` for collaboration

### For Web App
- Bookmark the URL for quick access
- Use drag & drop for file imports
- Filter "Unscored" to see progress
- Export JSON for statistical analysis
- Use score filters to focus on quality tiers
- Mobile scoring: great for on-the-go evaluation

---

## 🐛 Troubleshooting

### Desktop App Issues
**Window doesn't open:** Check Tkinter installation
**Can't import file:** Verify file has "URL" column

### Web App Issues
**Port in use:** Change port with `$env:PORT=5001`
**Team can't access:** Check firewall and IP address
**Upload fails:** Check file size (max 16MB)

---

## 🔄 Migrating Between Apps

Both apps use the same `article_scores.json` format!

**Desktop → Web:**
1. Copy `article_scores.json` to web app folder
2. Launch web app
3. Scores appear automatically

**Web → Desktop:**
1. Copy `article_scores.json` to desktop app folder
2. Launch desktop app
3. Import articles spreadsheet
4. Scores appear automatically

---

## 📦 Complete File List

### Core Applications
- `article_scoring_app.py` - Desktop app
- `webapp.py` - Web app server

### Web App Files
- `templates/index.html` - Main UI
- `static/style.css` - Styling
- `static/app.js` - Frontend logic

### Documentation
- `SCORING_APP_README.md` - Desktop guide
- `WEBAPP_README.md` - Web guide
- `QUICK_START.md` - Desktop quick start
- `WEBAPP_QUICK_START.md` - Web quick start
- `Scoring rubric.txt` - Rubric details

### Sample Data
- `sample_articles.csv` - CSV example
- `sample_articles.txt` - TXT example

### Dependencies
- `scoring_app_requirements.txt` - Desktop
- `webapp_requirements.txt` - Web

### Data Storage
- `article_scores.json` - All scores (auto-created)

---

## 🎓 Learning Path

**New Users:**
1. Read this comparison guide
2. Choose web app (recommended)
3. Follow `WEBAPP_QUICK_START.md`
4. Import `sample_articles.csv`
5. Score 2-3 articles to learn interface
6. Read `WEBAPP_README.md` for advanced features

**Team Setup:**
1. Designate one person as "server host"
2. Host installs web app
3. Host shares URL with team
4. Everyone bookmarks URL
5. Import real article list
6. Start collaborative scoring

---

## 🎯 Summary

**TL;DR:** Use the **Web App** unless you have a specific reason not to.

The web app provides:
- ✅ Better collaboration
- ✅ More export options (JSON)
- ✅ More import options (.txt)
- ✅ Modern interface
- ✅ Mobile access
- ✅ Real-time updates

Both apps provide the same core scoring functionality based on the comprehensive rubric.

---

**Ready to start?** Run `python webapp.py` and visit http://localhost:5000! 🚀
