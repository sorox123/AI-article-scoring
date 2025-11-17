# Quick Start Guide - AI Article Scoring App

## Getting Started in 3 Steps

### Step 1: Launch the App
```powershell
cd c:\Users\sorox\ai-news-scraper
python article_scoring_app.py
```

### Step 2: Import Your Articles
1. Click **"Import Spreadsheet"**
2. Select your Excel or CSV file (must have "URL" column)
3. Try the included `sample_articles.csv` to test the app

### Step 3: Start Scoring
1. **Double-click** any article in the list
2. Adjust the **5 sliders** (1-10 scale) based on the rubric descriptions
3. Add optional notes
4. Click **"Submit Score"**

## Quick Actions

| Action | How To |
|--------|--------|
| **Open article in browser** | Select article → Click "Visit Article" |
| **View scoring history** | Select article → Click "View Peer Scores" |
| **Search articles** | Type in search box at top |
| **Filter by score** | Use dropdown: All/Unscored/1-3/4-6/7-8/9-10 |
| **Export reports** | Click "Export Results" → Select filters → Choose folder |

## Scoring Cheat Sheet

### Quick Rating Guide (1-10 scale)

| Score | Meaning | Use When... |
|-------|---------|-------------|
| **9-10** | Exceptional | Gold standard quality, verified facts, expert authors |
| **7-8** | Good | Solid journalism, minor issues, reputable sources |
| **5-6** | Acceptable | Mix of good/bad, some concerns, moderate quality |
| **3-4** | Poor | Significant issues, weak sources, speculation |
| **1-2** | Very Poor | Misinformation, no evidence, unreliable |

### The 5 Categories

1. **Accuracy**: Is it true?
2. **Credibility**: Is the source trustworthy?
3. **Citation**: Are claims backed up?
4. **Reasoning**: Does the logic hold up?
5. **Confidence**: Are claims proportional to evidence?

## Example Workflow

### Scenario: Scoring 50 Articles

1. **Import**: Load your spreadsheet with 50 URLs
2. **Filter**: Click "Unscored" to see articles needing scores
3. **Score First**: Double-click first article
   - Read the article (click URL in scoring window)
   - Adjust all 5 sliders
   - Add notes if needed
   - Submit
4. **Repeat**: Work through the "Unscored" list
5. **Check Progress**: View peer scores to see how many are done
6. **Export**: When finished, export all with score ranges

## Pro Tips

✅ **Score systematically** - Work through unscored articles in order
✅ **Read before scoring** - Click URL in scoring window to open article
✅ **Use the full range** - Don't cluster everything at 5-7
✅ **Add notes** - Future you will thank you
✅ **Check peer scores** - See how others rated similar articles
✅ **Export regularly** - Save progress reports as you go

## Common Questions

**Q: Where are my scores saved?**
A: Automatically saved to `article_scores.json` in the app folder

**Q: Can multiple people score the same articles?**
A: Yes! Share the `article_scores.json` file and all peer scores will appear

**Q: What if my spreadsheet doesn't have titles?**
A: No problem - the app will display URLs instead

**Q: Can I edit a score after submitting?**
A: Just score it again - all scores are preserved in the history

**Q: How do I see the average score?**
A: It's displayed in the main list for each article (or "-" if unscored)

## Keyboard Shortcuts

- **Double-click article** = Open scoring window
- **Type in search** = Instant filter
- **Tab** = Navigate between UI elements

## Files You'll Work With

| File | Purpose |
|------|---------|
| `article_scoring_app.py` | The main application |
| `article_scores.json` | Your scoring data (auto-saved) |
| `sample_articles.csv` | Example spreadsheet format |
| `scoring_app_requirements.txt` | Python dependencies |

## Sample CSV Format

```csv
URL,Title
https://example.com/article1,Amazing AI Breakthrough
https://example.com/article2,New Model Released
```

## Need Help?

Check the status bar at the bottom of the app for helpful messages and error details.

For detailed information, see **SCORING_APP_README.md**
