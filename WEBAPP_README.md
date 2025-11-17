# AI Article Scoring Web Application

A web-based application for scoring AI news articles based on credibility, accuracy, and quality metrics. Access via a private URL for secure, collaborative scoring.

## 🌐 Web App Features

### **Access Control**
- **Private URL Access**: Share the URL with authorized users only
- **No authentication required**: Simple link-based access
- **Local or network deployment**: Run on localhost or expose to network

### **Enhanced Import Support**
- ✅ **CSV Files** (.csv)
- ✅ **Excel Files** (.xlsx, .xls)
- ✅ **Text Files** (.txt) - NEW!
  - One URL per line
  - Or comma-separated: `URL,Title`
  - Lines starting with `#` are ignored (comments)

### **Enhanced Export Options**
- ✅ **Text Files** (.txt in .zip) - Individual reports per article
- ✅ **JSON Export** (.json) - NEW! Structured data format
  - Includes overall averages
  - Category-by-category statistics
  - All individual scores
  - Export date and filter metadata

### **Modern Web Interface**
- 📱 Responsive design (works on desktop, tablet, mobile)
- 🎨 Clean, intuitive UI with smooth animations
- 🔍 Real-time search and filtering
- 📊 Interactive scoring with visual sliders
- 📈 Live statistics and peer score viewing

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
cd c:\Users\sorox\ai-news-scraper
pip install -r webapp_requirements.txt
```

### 2. Launch the Web App

```powershell
python webapp.py
```

You'll see output like:
```
================================================================================
AI ARTICLE SCORING WEB APP
================================================================================

🌐 Access URL: http://localhost:5000
🔒 Share this URL with others to grant access

⚠️  Keep this URL private - anyone with the link can access the app

Press CTRL+C to stop the server
================================================================================
```

### 3. Open in Browser

Visit `http://localhost:5000` in your web browser.

## 📖 User Guide

### Importing Articles

**Supported File Formats:**

1. **CSV Format**:
```csv
URL,Title
https://example.com/article1,AI Breakthrough Announced
https://example.com/article2,New Model Released
```

2. **Excel Format** (.xlsx, .xls):
| URL | Title |
|-----|-------|
| https://example.com/article1 | AI Breakthrough Announced |

3. **Text Format** (.txt) - NEW:
```
# This is a comment line (ignored)
https://example.com/article1
https://example.com/article2,Custom Title Here
https://example.com/article3
```

**Import Steps:**
1. Click **"📤 Import Articles"**
2. Drag & drop file or click "Choose File"
3. Articles appear automatically

### Scoring Articles

1. Click **"📝 Score Article"** on any article card
2. Adjust the 5 sliders (1-10 scale):
   - **Accuracy of Truthfulness**
   - **Author & Source Credibility**
   - **Citation & Evidence Quality**
   - **Reasoning Transparency**
   - **Confidence Calibration**
3. Add optional notes
4. Click **"Submit Score"**

### Viewing Peer Scores

1. Click **"📊 Peer Scores"** on any article
2. View:
   - Overall average score
   - Category-by-category averages
   - Individual score history with timestamps
   - Reviewer notes

### Exporting Results

**Export as Text Files (.zip)**:
1. Click **"💾 Export Results"**
2. Select score range filter
3. Choose "Text Files (.txt in .zip)"
4. Toggle options:
   - Include detailed scores
   - Include notes
5. Click **"Export"**

**Export as JSON (.json)** - NEW:
1. Click **"💾 Export Results"**
2. Select score range filter
3. Choose "JSON File (.json)"
4. Click **"Export"**

**JSON Export Format**:
```json
{
  "export_date": "2025-11-16T10:30:00",
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
          "timestamp": "2025-11-16T10:15:00"
        }
      ]
    }
  ]
}
```

### Search & Filter

**Search Bar**: Type keywords to filter by title or URL
**Filter Dropdown**:
- All
- Unscored (no ratings yet)
- 1-3 (Low scores)
- 4-6 (Medium scores)
- 7-8 (Good scores)
- 9-10 (High scores)

### Statistics

Click **"📊 Statistics"** to view:
- Total articles imported
- Total scores submitted
- Articles with/without scores

## 🔒 Security & Access

### Private URL Access

**Default Setup** (localhost only):
```
http://localhost:5000
```
Only accessible from the computer running the server.

**Network Access** (same WiFi/LAN):
To allow others on your network to access:

1. Find your IP address:
```powershell
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

2. Share this URL with team members:
```
http://192.168.1.100:5000
```

3. Ensure firewall allows connections on port 5000

**Custom Port**:
```powershell
$env:PORT=8080; python webapp.py
```

### Security Best Practices

⚠️ **Important**:
- Keep the URL private - anyone with the link can access
- Do not expose to public internet without additional authentication
- Use for trusted team members on secure networks
- Consider VPN for remote access

## 📁 Data Storage

### Automatic Persistence
- All scores saved to `article_scores.json`
- Auto-saves after each submission
- Data persists across server restarts

### Backup & Sharing
```powershell
# Backup scores
Copy-Item article_scores.json article_scores_backup.json

# Share with team (merge scores)
# Simply copy article_scores.json to shared location
```

## 🛠️ Technical Details

### Architecture
- **Backend**: Flask (Python web framework)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Data Format**: JSON for storage and API
- **File Processing**: Pandas for CSV/Excel, custom parser for TXT

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/api/import` | POST | Import articles from file |
| `/api/scores` | GET | Get all scores |
| `/api/scores/<url>` | GET | Get scores for specific article |
| `/api/scores/<url>` | POST | Add new score |
| `/api/statistics` | GET | Get overall statistics |
| `/api/export/txt` | POST | Export as text files (.zip) |
| `/api/export/json` | POST | Export as JSON |
| `/api/export/all` | GET | Export complete database |

### File Structure
```
ai-news-scraper/
├── webapp.py                  # Flask server
├── templates/
│   └── index.html            # Main HTML template
├── static/
│   ├── style.css             # Styles
│   └── app.js                # JavaScript application
├── uploads/                   # Temporary file uploads
├── article_scores.json       # Persistent data storage
└── webapp_requirements.txt   # Python dependencies
```

## 🔧 Configuration

### Environment Variables

```powershell
# Custom port
$env:PORT=8080

# Flask debug mode (development only)
$env:FLASK_DEBUG=1
```

### Maximum Upload Size
Default: 16MB

To change, edit `webapp.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Use different port
$env:PORT=5001; python webapp.py
```

### Cannot Access from Other Devices
- Check firewall settings
- Verify devices are on same network
- Use correct IP address (not localhost)

### Import Fails
- Verify file format (.csv, .xlsx, .xls, .txt)
- Ensure "URL" column exists (for CSV/Excel)
- Check file encoding (UTF-8 recommended for .txt)

### Scores Not Saving
- Check write permissions in application directory
- Verify `article_scores.json` is not read-only
- Check console for error messages

## 📱 Browser Compatibility

Tested on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 🆚 Desktop App vs Web App

| Feature | Desktop App | Web App |
|---------|-------------|---------|
| Installation | Python + Tkinter | Python + Flask |
| Access | Local only | URL-based (local or network) |
| Collaboration | Share JSON file | Real-time via URL |
| UI | Native Tkinter | Modern web interface |
| Mobile Support | ❌ No | ✅ Yes (responsive) |
| TXT Import | ❌ No | ✅ Yes |
| JSON Export | ❌ No | ✅ Yes |

## 🎯 Use Cases

### Individual Research
- Run on localhost
- Import articles from various sources
- Score and take notes
- Export results for analysis

### Team Collaboration
- Run on one machine
- Share URL with team members
- Multiple people score simultaneously
- View peer scores in real-time
- Export combined results

### Academic Studies
- Import study corpus via .txt file
- Multiple annotators score articles
- Export JSON for statistical analysis
- Track inter-rater reliability via peer scores

## 📄 License & Credits

Built for AI article credibility assessment research.

## 🔗 Quick Links

- **Desktop Version**: See `SCORING_APP_README.md`
- **Quick Start**: See `QUICK_START.md`
- **Sample Data**: `sample_articles.csv`

## 🚦 Getting Started Now

```powershell
# 1. Install
pip install -r webapp_requirements.txt

# 2. Run
python webapp.py

# 3. Open browser
# Go to http://localhost:5000

# 4. Import sample data
# Use sample_articles.csv to test

# 5. Start scoring!
```

## 💡 Tips

- **Keyboard navigation**: Use Tab to move between form fields
- **Quick scoring**: Double-click articles to open scoring modal
- **Bulk export**: Use score filters to export specific quality tiers
- **Data portability**: JSON exports work with analysis tools (Python, R, Excel)
- **Team workflow**: Have lead researcher run server, share URL in team chat

---

**Need Help?** Check the status bar at bottom of the web page for error messages and tips.
