# AI Article Credibility Scoring App

An interactive desktop application for scoring AI news articles based on a comprehensive rubric covering accuracy, credibility, citation quality, reasoning transparency, and confidence calibration.

## Features

### Core Functionality
- **Import Spreadsheets**: Load articles from Excel (.xlsx, .xls) or CSV files
- **Interactive Scoring**: Score articles across 5 key dimensions (1-10 scale)
- **Peer Score Tracking**: View scoring history from multiple reviewers
- **Article Browser**: Open articles directly in your default web browser
- **Search & Filter**: Find articles by text or filter by average score ranges
- **Export Results**: Generate detailed text reports with customizable filters

### Scoring Categories

Based on the provided rubric, each article is evaluated on:

1. **Accuracy of Truthfulness (1-10)**: Classification as True/Partially True/False
2. **Author and Source Credibility (1-10)**: Publisher reputation and author expertise
3. **Citation and Evidence Quality (1-10)**: Quality and verifiability of references
4. **Reasoning Transparency (1-10)**: Logical coherence and explanation quality
5. **Confidence Calibration (1-10)**: Alignment between stated confidence and correctness

## Installation

### Prerequisites
- Python 3.8 or higher
- Tkinter (usually comes with Python)

### Setup

1. Install required dependencies:
```powershell
pip install -r scoring_app_requirements.txt
```

2. Run the application:
```powershell
python article_scoring_app.py
```

## Usage Guide

### 1. Importing Articles

**Step 1**: Click "Import Spreadsheet" button
**Step 2**: Select your Excel or CSV file

**Required Column**:
- `URL` - The article's web address

**Optional Column**:
- `Title` - Article title (if not provided, URL will be displayed)

**Example Spreadsheet Format**:

| URL | Title |
|-----|-------|
| https://techcrunch.com/ai-article | AI Breakthrough Achieves Superintelligence |
| https://venturebeat.com/example | New Model Outperforms Humans on All Tasks |

### 2. Viewing Articles

Once imported, articles appear in the main list showing:
- **#**: Row number
- **URL**: Article web address
- **Title**: Article title
- **Avg Score**: Average across all scoring dimensions (or "-" if unscored)
- **Peer Scores**: Number of times the article has been scored

### 3. Scoring an Article

**Method 1**: Double-click an article in the list
**Method 2**: Select an article and click "Score Article" button

The scoring window provides:
- Article title and URL (clickable to open in browser)
- 5 interactive sliders for each scoring category
- Detailed rubric descriptions for each category
- Optional notes field for additional observations
- Submit button to save your score

**Scoring Tips**:
- Read the rubric descriptions carefully
- Click the URL in the scoring window to open the article
- Use the full 1-10 range based on the detailed criteria
- Add notes to explain your reasoning for future reference

### 4. Viewing Peer Scores

Select an article and click "View Peer Scores" to see:
- **Statistics**: Average score for each category
- **Overall Average**: Combined score across all dimensions
- **Individual Scores**: Complete history with timestamps and notes

### 5. Visiting Articles

Select an article and click "Visit Article" to open it in your default web browser.

### 6. Searching and Filtering

**Search Bar**: Type keywords to filter by title or URL
**Score Filter**: Dropdown options include:
- All
- Unscored (no ratings yet)
- 1-3 (Low scores)
- 4-6 (Medium scores)
- 7-8 (Good scores)
- 9-10 (High scores)

### 7. Exporting Results

**Step 1**: Click "Export Results"
**Step 2**: Choose score range filter:
- All scored articles
- High (9-10)
- Good (7-8)
- Medium (4-6)
- Low (1-3)

**Step 3**: Select export options:
- Include detailed scores (all peer scores)
- Include notes (reviewer observations)

**Step 4**: Choose destination directory

**Export Output**: Individual `.txt` files for each article containing:
- Article URL
- Overall average score
- Number of peer scores
- Category-by-category averages
- Detailed individual scores (optional)
- Reviewer notes (optional)

## Data Storage

### Persistent Storage
All scores are automatically saved to `article_scores.json` in the application directory. This file preserves:
- All scoring data
- Timestamps for each score
- Reviewer notes
- Complete scoring history

### Data Structure
```json
{
  "article_url": [
    {
      "accuracy": 8,
      "credibility": 9,
      "citation": 7,
      "reasoning": 8,
      "confidence": 7,
      "notes": "Well-researched article with credible sources",
      "timestamp": "2025-11-16T10:30:00"
    }
  ]
}
```

## Keyboard Shortcuts

- **Double-click article**: Open scoring window
- **Search field**: Start typing to filter immediately

## Troubleshooting

### Import Issues
- **Error: "Must contain URL column"**: Ensure your spreadsheet has a column named "URL"
- **Failed to import**: Check file format is .xlsx, .xls, or .csv
- **Encoding errors**: Save CSV files as UTF-8 encoding

### Scoring Issues
- **Score not saving**: Ensure all sliders are adjusted (default is 5)
- **Window not responding**: Check if modal dialogs are open behind main window

### Export Issues
- **No files created**: Ensure articles match the selected score range filter
- **Permission denied**: Choose a directory where you have write permissions

## Tips for Effective Scoring

1. **Be Consistent**: Use the same interpretation of the 1-10 scale across all articles
2. **Read Thoroughly**: Review the full article before scoring
3. **Use Notes**: Document your reasoning, especially for edge cases
4. **Check Peer Scores**: Review how others scored similar articles for calibration
5. **Focus on Evidence**: Base scores on observable article characteristics, not assumptions

## Score Interpretation Guide

### Accuracy (1-10)
- **9-10**: Verifiable facts with primary sources
- **7-8**: Mostly accurate with minor speculation
- **4-6**: Mix of facts and unverified claims
- **1-3**: Primarily speculation or demonstrably false

### Credibility (1-10)
- **9-10**: Renowned experts at top-tier publications
- **7-8**: Established journalists at reputable outlets
- **4-6**: Mixed credentials or mid-tier sources
- **1-3**: Anonymous or unreliable sources

### Citation (1-10)
- **9-10**: Comprehensive citations with primary sources
- **7-8**: Good citations with some secondary sources
- **4-6**: Limited or incomplete citations
- **1-3**: No citations or fabricated references

### Reasoning (1-10)
- **9-10**: Clear, logical progression with strong evidence
- **7-8**: Generally sound reasoning with minor gaps
- **4-6**: Some logical issues or unsupported leaps
- **1-3**: Circular reasoning or major logical flaws

### Confidence (1-10)
- **9-10**: Claims match evidence strength perfectly
- **7-8**: Mostly calibrated confidence levels
- **4-6**: Some overconfidence or hedging
- **1-3**: Severe overconfidence or extreme uncertainty

## Advanced Usage

### Batch Scoring Sessions
1. Import large spreadsheet
2. Filter to "Unscored" articles
3. Work through list systematically
4. Use peer scores to calibrate your ratings

### Comparative Analysis
1. Filter by score range (e.g., "9-10")
2. Export high-scoring articles
3. Review for common quality patterns
4. Use insights to refine future scoring

### Team Collaboration
1. Share `article_scores.json` file with team members
2. Each person scores independently
3. Compare peer score statistics
4. Discuss discrepancies in team meetings

## Contact & Support

For issues or feature requests, check the application status bar for helpful messages and error details.
