# Google Sheets Integration - Test Checklist

## ✅ Pre-Test Setup

- [x] Dependencies installed (`gspread`, `google-auth`, etc.)
- [x] Flask app starts without errors
- [x] UI loads with new Google Sheets tab visible
- [x] Backend endpoint `/api/import/google-sheet` exists
- [x] Code pushed to GitHub

## 🧪 Manual Testing Steps

### Test 1: Public Sheet Import (Basic)
- [ ] Create new Google Sheet
- [ ] Add 5-10 article URLs (one per row)
- [ ] Share sheet: "Anyone with the link can view"
- [ ] Copy sharing URL
- [ ] Open app at http://localhost:5000
- [ ] Click "Import Articles" → "Google Sheets" tab
- [ ] Paste URL
- [ ] Click "Import from Google Sheets"
- [ ] Verify: Success message shows correct count
- [ ] Verify: Articles appear in list

### Test 2: Sheet with Headers and Titles
- [ ] Create Google Sheet with format:
  ```
  Title             | URL
  Article Title 1   | https://example.com/1
  Article Title 2   | https://example.com/2
  ```
- [ ] Import into app
- [ ] Verify: Titles are extracted correctly
- [ ] Verify: URLs are detected despite headers

### Test 3: Duplicate Detection
- [ ] Import sheet with 5 URLs
- [ ] Import same sheet again
- [ ] Verify: Message shows "5 duplicates removed"
- [ ] Verify: No duplicate articles in list

### Test 4: Multiple Worksheets
- [ ] Create sheet with multiple tabs (Sheet1, Sheet2)
- [ ] Put URLs in Sheet2
- [ ] Import with worksheet name "Sheet2"
- [ ] Verify: Articles from Sheet2 imported
- [ ] Try without worksheet name
- [ ] Verify: Articles from Sheet1 imported (first sheet)

### Test 5: URL Format Variations
Test these URL formats work:
- [ ] Full URL: `https://docs.google.com/spreadsheets/d/ABC123/edit#gid=0`
- [ ] Short URL: `https://docs.google.com/spreadsheets/d/ABC123`
- [ ] Direct link from "Share" button

### Test 6: Error Handling
- [ ] Try importing private sheet (not shared)
  - Expected: "Access denied" error
- [ ] Try invalid URL (not Google Sheets)
  - Expected: "Invalid Google Sheets URL" error
- [ ] Try empty sheet
  - Expected: "No URLs detected" error
- [ ] Try sheet with no URLs (just text)
  - Expected: "No URLs detected" error

### Test 7: Mixed Content
- [ ] Create sheet with:
  - Comment rows (start with #)
  - URLs with adjacent titles
  - URLs without titles
  - Empty rows
  - Non-URL text
- [ ] Import and verify only URLs extracted

### Test 8: Large Sheet
- [ ] Create sheet with 50+ URLs
- [ ] Import and verify:
  - Progress indicator shows
  - All URLs imported
  - No timeout errors

## 🔧 Service Account Testing (Advanced)

### Setup
- [ ] Create Google Cloud service account
- [ ] Download JSON credentials
- [ ] Set environment variable:
  ```powershell
  $env:GOOGLE_SHEETS_CREDENTIALS = Get-Content service-account.json -Raw
  ```
- [ ] Restart Flask app

### Test Private Sheet
- [ ] Create private Google Sheet (not publicly shared)
- [ ] Share with service account email
- [ ] Import via app
- [ ] Verify: Import succeeds without public sharing

## 📱 UI/UX Testing

- [ ] Tab switching works smoothly
- [ ] Input fields have proper focus styling
- [ ] Help text is readable and helpful
- [ ] Error messages are clear
- [ ] Success messages show import statistics
- [ ] Modal closes after successful import
- [ ] Form resets after import

## 🌐 Deployment Testing (Render.com)

After deploying to Render:
- [ ] Dependencies install correctly
- [ ] App starts without errors
- [ ] Google Sheets tab visible
- [ ] Public sheet import works
- [ ] Environment variable for credentials (if set)
- [ ] No CORS or security issues

## 🐛 Known Issues / Edge Cases

Document any issues found:

1. **Issue:** [Description]
   - **Steps:** [How to reproduce]
   - **Expected:** [What should happen]
   - **Actual:** [What actually happens]
   - **Workaround:** [Temporary solution if any]

---

## ✅ Test Results Summary

**Date Tested:** _______________  
**Tester:** _______________  
**Environment:** Local / Production (circle one)

**Pass:** ___ / ___ tests  
**Fail:** ___ / ___ tests  

**Overall Status:** 🟢 Ready / 🟡 Needs fixes / 🔴 Major issues

**Notes:**
_______________________________________________
_______________________________________________
_______________________________________________

---

## 📋 Sample Test Data

### Sample Google Sheet URL (Public)
Create a test sheet and paste URL here:
```
https://docs.google.com/spreadsheets/d/[YOUR_SHEET_ID]/edit
```

### Sample URLs for Testing
```
https://techcrunch.com/ai-news-article-1
https://arstechnica.com/ai-story-2
https://theverge.com/artificial-intelligence-3
https://venturebeat.com/ai/ai-breakthrough-4
https://wired.com/story/machine-learning-5
```

### Expected Import Result
```
Import complete: 5 total articles, 5 new, 0 duplicates removed
```
