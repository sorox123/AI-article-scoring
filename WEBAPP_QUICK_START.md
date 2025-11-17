# 🚀 Web App Quick Start

## Launch in 3 Steps

### 1️⃣ Install Dependencies
```powershell
cd c:\Users\sorox\ai-news-scraper
pip install -r webapp_requirements.txt
```

### 2️⃣ Start Server
```powershell
python webapp.py
```

You'll see:
```
================================================================================
AI ARTICLE SCORING WEB APP
================================================================================

🌐 Access URL: http://localhost:5000
🔒 Share this URL with others to grant access
================================================================================
```

### 3️⃣ Open Browser
Visit: **http://localhost:5000**

## 🎯 Quick Actions

| Action | Steps |
|--------|-------|
| **Import articles** | Click "📤 Import Articles" → Choose file (.csv, .xlsx, .txt) |
| **Score an article** | Click "📝 Score Article" on any card → Adjust sliders → Submit |
| **View peer scores** | Click "📊 Peer Scores" on any card |
| **Visit article** | Click "🔗 Visit Article" to open in new tab |
| **Export results** | Click "💾 Export Results" → Choose format (TXT/JSON) |
| **View statistics** | Click "📊 Statistics" |

## 📁 File Format Examples

### CSV Format
```csv
URL,Title
https://example.com/article1,AI Breakthrough
https://example.com/article2,New Model Released
```

### TXT Format (NEW!)
```txt
# Comments start with #
https://example.com/article1
https://example.com/article2,Custom Title
```

### Excel Format
Standard spreadsheet with "URL" and "Title" columns

## 🔗 Sharing with Team

### Local Network Access
1. Note your IP address from server output (e.g., `http://192.168.68.71:5000`)
2. Share this URL with team members on same network
3. They can access and score simultaneously

### Security Note
⚠️ Anyone with the URL can access - keep it private!

## 🆕 What's New in Web App

✅ **TXT file import** - Simple text files with URLs
✅ **JSON export** - Structured data for analysis
✅ **Mobile responsive** - Works on phones/tablets
✅ **Real-time collaboration** - Multiple users simultaneously
✅ **Modern UI** - Smooth animations and interactions

## 📊 Export Formats

### Text Export (.zip)
- Individual .txt files per article
- Includes averages and detailed scores
- Optional notes and timestamps

### JSON Export (.json) - NEW!
```json
{
  "export_date": "2025-11-16T10:30:00",
  "articles": [
    {
      "url": "...",
      "overall_average": 7.8,
      "category_averages": {...},
      "individual_scores": [...]
    }
  ]
}
```

## 🛑 Stop Server
Press **CTRL+C** in the terminal running the server

## 📖 Full Documentation
See **WEBAPP_README.md** for complete details

## 🆚 Desktop vs Web

| Feature | Desktop | Web |
|---------|---------|-----|
| Access | Local only | URL-based |
| Collaboration | Share files | Real-time |
| Mobile | ❌ | ✅ |
| TXT Import | ❌ | ✅ |
| JSON Export | ❌ | ✅ |

## 💡 Pro Tips

- **Test with samples**: Use `sample_articles.csv` or `sample_articles.txt`
- **Filter unscored**: Find articles that need attention
- **Export by quality**: Filter 9-10 for high-quality articles only
- **Use JSON for analysis**: Import into Python, R, or Excel for stats
- **Bookmark the URL**: Add to favorites for quick access

## 🐛 Troubleshooting

**Port already in use?**
```powershell
$env:PORT=5001; python webapp.py
```

**Can't import file?**
- Check file format (.csv, .xlsx, .xls, .txt)
- Ensure "URL" column exists (CSV/Excel)
- Verify UTF-8 encoding (.txt)

**Team can't access?**
- Check firewall settings
- Use IP address from server output
- Ensure on same network

## ✨ Ready to Score!

Your web app is now running at **http://localhost:5000**

Import some articles and start scoring! 🎯
