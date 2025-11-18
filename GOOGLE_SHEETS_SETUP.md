# Google Sheets Integration Guide

## Overview
The AI Article Scoring app now supports importing articles directly from Google Sheets! This makes it easy to collaborate with your team by maintaining a shared spreadsheet of articles to score.

## Quick Start

### 1. Create Your Google Sheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet or use an existing one
3. Add article URLs to your sheet:
   - URLs can be in any column
   - Can include titles in adjacent columns (optional)
   - Can have header rows (they'll be detected automatically)
   - Can have multiple columns of data

### 2. Share Your Sheet Publicly
For the simplest setup (no authentication needed):

1. Click the **Share** button (top right)
2. Click **Change to anyone with the link**
3. Set permission to **Viewer**
4. Copy the sharing link

**Important**: The sheet must be shared as "Anyone with the link can view" for public access to work.

### 3. Import in the App
1. Open the AI Article Scoring app
2. Click **📤 Import Articles**
3. Switch to the **📊 Google Sheets** tab
4. Paste your Google Sheets URL
5. (Optional) Enter the worksheet name if you have multiple sheets
6. Click **Import from Google Sheets**

## Sheet Format Examples

### Example 1: Simple URL List
```
https://example.com/article1
https://example.com/article2
https://example.com/article3
```

### Example 2: With Headers and Titles
```
Title                        | URL
----------------------------|----------------------------------
AI Breakthrough in 2025     | https://example.com/article1
Machine Learning Evolution  | https://example.com/article2
```

### Example 3: Multiple Columns
```
Date       | Source    | Title              | URL                          | Notes
-----------|-----------|-------------------|------------------------------|-------
2025-01-15 | TechNews  | AI Makes Progress | https://example.com/article1 | Check credibility
2025-01-16 | SciDaily  | New Algorithm     | https://example.com/article2 | High priority
```

## URL Detection
The app automatically detects URLs in your spreadsheet:
- Searches all columns for URLs starting with `http://` or `https://`
- Extracts titles from adjacent columns when available
- Ignores header rows and non-URL content
- Removes duplicate URLs automatically

## Supported URL Formats
You can paste any of these formats:
- Full URL: `https://docs.google.com/spreadsheets/d/1ABC123.../edit#gid=0`
- Short URL: `https://docs.google.com/spreadsheets/d/1ABC123...`
- Just the ID: `1ABC123...`

## Multiple Worksheets
If your spreadsheet has multiple worksheets (tabs):
1. Enter the worksheet name in the "Worksheet Name" field
2. Leave empty to use the first worksheet
3. Worksheet names are case-sensitive

## Advanced: Private Sheets with Service Account

If you don't want to share your sheet publicly, you can use a Google Cloud service account:

### Setup Steps:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the **Google Sheets API**
4. Go to **IAM & Admin** → **Service Accounts**
5. Create a service account
6. Create a JSON key for the service account
7. Share your Google Sheet with the service account email (found in the JSON)

### Configure the App:
Add the service account credentials as an environment variable:

**On Render.com:**
1. Go to your app's **Environment** settings
2. Add a new environment variable:
   - Key: `GOOGLE_SHEETS_CREDENTIALS`
   - Value: Paste the entire contents of your JSON key file

**Locally:**
```powershell
$env:GOOGLE_SHEETS_CREDENTIALS = Get-Content service-account-key.json -Raw
python webapp_secure.py
```

## Troubleshooting

### "Failed to import: Access denied"
- Make sure the sheet is shared publicly ("Anyone with the link can view")
- Or set up service account authentication (see Advanced section above)

### "Invalid Google Sheets URL"
- URL must contain `docs.google.com/spreadsheets`
- Try copying the full URL from your browser
- Remove any tracking parameters after the sheet ID

### "No URLs found in sheet"
- Make sure your sheet contains URLs starting with `http://` or `https://`
- URLs can be in any column
- Check that the worksheet name is correct (if specified)

### "Import successful but no new articles"
- All URLs in the sheet may already exist in your database
- Check the import message for "duplicates removed" count
- This is normal if you're re-importing the same sheet

## Best Practices

1. **Use descriptive worksheet names** if you have multiple tabs
2. **Include titles** in adjacent columns for better organization
3. **Keep one sheet per project** or scoring session
4. **Update the sheet regularly** as a central source of truth
5. **Share with your team** for collaborative article collection

## Integration with Existing Features

- **Duplicate Detection**: URLs already in the database are automatically skipped
- **Statistics**: Import count shows total, new, and duplicate articles
- **Persistence**: Imported articles are saved to the PostgreSQL database
- **Export**: Use "Export Results" to save scored articles back to files

## Example Workflow

1. **Collect**: Team members add articles to shared Google Sheet
2. **Import**: Load articles into scoring app via Google Sheets URL
3. **Score**: Team members score articles using the rubric
4. **Export**: Download scored results as TXT, JSON, or plain URLs
5. **Repeat**: Re-import sheet to get new articles (duplicates auto-removed)

---

**Need Help?** Check the main [README.md](README.md) for more information about the scoring app.
