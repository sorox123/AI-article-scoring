from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd
import json
import os
import secrets
from datetime import datetime
from pathlib import Path
from functools import wraps
import io
import re
from database import get_db, init_db
from google_sheets import get_sheets_importer

app = Flask(__name__)
# Use a consistent secret key for development, or from environment for production
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345678901234567890')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SCORES_FILE'] = 'article_scores.json'
app.config['ARTICLES_FILE'] = 'article_list.json'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

# AUTHENTICATION CONFIGURATION
# Set these environment variables on your hosting platform:
# - ADMIN_PASSWORD: The password users must enter
# - Or edit the password hash below

# Generate password hash: python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-password'))"
DEFAULT_PASSWORD_HASH = generate_password_hash('scoring2025')  # Change this!

def get_password_hash():
    """Get password hash from environment or use default"""
    admin_password = os.environ.get('ADMIN_PASSWORD')
    if admin_password:
        return generate_password_hash(admin_password)
    return DEFAULT_PASSWORD_HASH

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db = init_db()

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Authentication required', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated_function

def load_scores():
    """Load existing scores from JSON file"""
    if os.path.exists(app.config['SCORES_FILE']):
        with open(app.config['SCORES_FILE'], 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_scores(scores_data):
    """Save scores to JSON file"""
    with open(app.config['SCORES_FILE'], 'w', encoding='utf-8') as f:
        json.dump(scores_data, f, indent=2, ensure_ascii=False)

def load_articles():
    """Load persisted article list from JSON file"""
    if os.path.exists(app.config['ARTICLES_FILE']):
        with open(app.config['ARTICLES_FILE'], 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_articles(articles_list):
    """Save article list to JSON file"""
    with open(app.config['ARTICLES_FILE'], 'w', encoding='utf-8') as f:
        json.dump(articles_list, f, indent=2, ensure_ascii=False)

def merge_articles(existing_articles, new_articles):
    """Merge new articles with existing ones, removing duplicates based on title"""
    # Create a dict with titles as keys for deduplication
    articles_dict = {}
    
    # Add existing articles first
    for article in existing_articles:
        title = article.get('Title', '').strip().lower()
        if title:
            articles_dict[title] = article
    
    # Add new articles (will overwrite if duplicate title found)
    duplicates = []
    new_count = 0
    for article in new_articles:
        title = article.get('Title', '').strip().lower()
        if title:
            if title in articles_dict:
                duplicates.append(article.get('Title', ''))
            else:
                articles_dict[title] = article
                new_count += 1
    
    # Convert back to list
    merged_list = list(articles_dict.values())
    
    return merged_list, new_count, duplicates

def is_url(text):
    """Smart URL detection using regex"""
    if not isinstance(text, str):
        return False
    
    # URL pattern - matches http://, https://, www., and common domains
    url_pattern = r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(com|org|net|edu|gov|io|co|ai|app|dev)[^\s]*'
    return bool(re.search(url_pattern, text.strip()))

def extract_url_and_title(row_data):
    """Extract URL and title from a row of data (list or dict)"""
    url = None
    title = None
    
    if isinstance(row_data, dict):
        # Dictionary - check all values for URLs
        values = list(row_data.values())
    else:
        # List or tuple
        values = list(row_data)
    
    # Find first URL
    for val in values:
        if is_url(val):
            url = str(val).strip()
            # Ensure URL has protocol
            if not url.startswith('http'):
                url = 'https://' + url
            break
    
    # Find title (first non-URL text value, or use URL)
    for val in values:
        if val and not is_url(val) and isinstance(val, str) and len(val.strip()) > 0:
            title = str(val).strip()
            break
    
    if not title and url:
        title = url[:50] + '...' if len(url) > 50 else url
    
    return url, title

def parse_txt_file(filepath):
    """Parse a .txt file - automatically detects URLs"""
    articles = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Try comma-separated format first
            if ',' in line:
                parts = [p.strip() for p in line.split(',')]
                url, title = extract_url_and_title(parts)
            else:
                # Single value - check if it's a URL
                url, title = extract_url_and_title([line])
            
            if url:
                articles.append({'URL': url, 'Title': title})
    
    return pd.DataFrame(articles) if articles else pd.DataFrame(columns=['URL', 'Title'])

def smart_parse_dataframe(df):
    """Smart parsing of dataframe - automatically detects URL and Title columns"""
    articles = []
    
    # Try to find columns by common names first
    url_col = None
    title_col = None
    
    # Check for common URL column names (case-insensitive)
    url_names = ['url', 'link', 'source', 'article', 'webpage', 'site']
    for col in df.columns:
        if str(col).lower().strip() in url_names:
            url_col = col
            break
    
    # Check for common title column names
    title_names = ['title', 'headline', 'name', 'article title', 'description']
    for col in df.columns:
        if str(col).lower().strip() in title_names:
            title_col = col
            break
    
    # If no obvious columns found, scan data to find URLs
    if not url_col:
        for col in df.columns:
            # Check first few non-null values
            sample_values = df[col].dropna().head(5)
            if any(is_url(str(val)) for val in sample_values):
                url_col = col
                break
    
    if not url_col:
        return []  # No URLs found
    
    # Process each row
    for idx, row in df.iterrows():
        url = str(row[url_col]).strip() if pd.notna(row[url_col]) else None
        
        if url and is_url(url):
            # Ensure URL has protocol
            if not url.startswith('http'):
                url = 'https://' + url
            
            # Get title
            if title_col and pd.notna(row[title_col]):
                title = str(row[title_col]).strip()
            else:
                # Look for first non-URL text column
                title = None
                for col in df.columns:
                    if col != url_col and pd.notna(row[col]):
                        val = str(row[col]).strip()
                        if not is_url(val) and len(val) > 0:
                            title = val
                            break
                
                if not title:
                    title = url[:50] + '...' if len(url) > 50 else url
            
            articles.append({'URL': url, 'Title': title})
    
    return articles

@app.route('/login')
def login_page():
    """Login page"""
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def login():
    """Handle login"""
    data = request.json
    password = data.get('password', '')
    
    if check_password_hash(get_password_hash(), password):
        session['authenticated'] = True
        session.permanent = True
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid password'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """Handle logout"""
    session.pop('authenticated', None)
    return jsonify({'success': True})

@app.route('/')
def index():
    """Main page - requires authentication"""
    if not session.get('authenticated'):
        return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/api/articles', methods=['GET'])
@login_required
def get_articles():
    """Get all persisted articles"""
    articles = db.get_all_articles()
    return jsonify({
        'articles': articles,
        'count': len(articles)
    })

@app.route('/api/import', methods=['POST'])
@login_required
def import_file():
    """Import articles from uploaded file - automatically detects URLs"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse file based on type
        if filename.endswith('.txt'):
            df = parse_txt_file(filepath)
            new_articles = df.to_dict('records') if not df.empty else []
        elif filename.endswith('.csv'):
            df = pd.read_csv(filepath)
            new_articles = smart_parse_dataframe(df)
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath)
            new_articles = smart_parse_dataframe(df)
        else:
            os.remove(filepath)
            return jsonify({'error': 'Unsupported file format. Use .csv, .xlsx, .xls, or .txt'}), 400
        
        if not new_articles:
            os.remove(filepath)
            return jsonify({'error': 'No URLs detected in file. Please ensure file contains valid URLs.'}), 400
        
        # Add articles to database (handles deduplication)
        merged_articles, new_count, duplicates = db.add_articles(new_articles)
        
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'articles': merged_articles,
            'total_count': len(merged_articles),
            'new_count': new_count,
            'duplicate_count': len(duplicates),
            'duplicates': duplicates[:10]  # Show first 10 duplicates
        })
    
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': f'Failed to import file: {str(e)}'}), 500

"""
Add this endpoint to webapp_secure.py after the /api/import endpoint
Insert around line 328 (after the file import endpoint)
"""

@app.route('/api/import/google-sheet', methods=['POST'])
@login_required
def import_google_sheet():
    """Import articles from a Google Sheets URL"""
    try:
        data = request.json
        sheet_url = data.get('url', '').strip()
        sheet_name = data.get('sheetName', None)  # Optional worksheet name
        
        if not sheet_url:
            return jsonify({'error': 'No Google Sheets URL provided'}), 400
        
        # Validate it looks like a Google Sheets URL
        if 'docs.google.com/spreadsheets' not in sheet_url and '/d/' not in sheet_url:
            return jsonify({'error': 'Invalid Google Sheets URL. Please provide a valid sheets.google.com link'}), 400
        
        # Get Google Sheets importer
        sheets_importer = get_sheets_importer()
        
        # Import the sheet
        df = sheets_importer.import_sheet(sheet_url, sheet_name)
        
        if df.empty:
            return jsonify({'error': 'Google Sheet is empty or could not be read'}), 400
        
        # Use smart parsing to detect URLs
        from webapp_secure import smart_parse_dataframe  # Import the function
        new_articles = smart_parse_dataframe(df)
        
        if not new_articles:
            return jsonify({'error': 'No URLs detected in Google Sheet. Make sure the sheet contains article URLs.'}), 400
        
        # Add articles to database (handles deduplication)
        merged_articles, new_count, duplicates = db.add_articles(new_articles)
        
        return jsonify({
            'success': True,
            'articles': merged_articles,
            'total_count': len(merged_articles),
            'new_count': new_count,
            'duplicate_count': len(duplicates),
            'duplicates': duplicates[:10]  # Show first 10 duplicates
        })
    
    except ValueError as e:
        # Specific error from Google Sheets importer
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to import Google Sheet: {str(e)}'}), 500


@app.route('/api/scores', methods=['GET'])
@login_required
def get_scores():
    """Get all scores"""
    scores_data = db.get_all_scores()
    return jsonify(scores_data)

@app.route('/api/scores/<path:url>', methods=['GET'])
@login_required
def get_article_scores(url):
    """Get scores for a specific article"""
    article_scores = db.get_scores_for_article(url)
    
    if article_scores:
        categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        
        cat_avgs = {}
        for cat in categories:
            cat_scores = [s.get(cat, 0) for s in article_scores]
            cat_avgs[cat] = sum(cat_scores) / len(cat_scores) if cat_scores else 0
        
        overall = sum(cat_avgs.values()) / len(categories)
        
        return jsonify({
            'scores': article_scores,
            'count': len(article_scores),
            'category_averages': cat_avgs,
            'overall_average': overall
        })
    
    return jsonify({
        'scores': [],
        'count': 0,
        'category_averages': {},
        'overall_average': 0
    })

@app.route('/api/scores/<path:url>', methods=['POST'])
@login_required
def add_score(url):
    """Add a score for an article"""
    try:
        score_data = request.json
        
        required_fields = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        for field in required_fields:
            if field not in score_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
            
            score_value = score_data[field]
            if not isinstance(score_value, (int, float)) or score_value < 1 or score_value > 10:
                return jsonify({'error': f'Invalid score for {field}: must be between 1 and 10'}), 400
        
        score_data['timestamp'] = datetime.now().isoformat()
        
        # Save score to database
        db.add_score(url, score_data)
        
        return jsonify({
            'success': True,
            'message': 'Score added successfully'
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to add score: {str(e)}'}), 500

@app.route('/api/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Get overall statistics for all articles"""
    stats = db.get_statistics()
    return jsonify(stats)

@app.route('/api/export/txt', methods=['POST'])
@login_required
def export_txt():
    """Export scored articles to text files"""
    try:
        params = request.json
        score_range = params.get('scoreRange', 'All')
        include_details = params.get('includeDetails', True)
        include_notes = params.get('includeNotes', True)
        
        scores_data = db.get_all_scores()
        categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        
        from io import BytesIO
        import zipfile
        
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            exported_count = 0
            
            for url, scores in scores_data.items():
                if not scores:
                    continue
                
                avg = sum(s.get(cat, 0) for s in scores for cat in categories) / (len(scores) * len(categories))
                
                if score_range != "All":
                    if score_range == "9-10" and not (9 <= avg <= 10):
                        continue
                    elif score_range == "7-8" and not (7 <= avg <= 8):
                        continue
                    elif score_range == "4-6" and not (4 <= avg <= 6):
                        continue
                    elif score_range == "1-3" and not (1 <= avg <= 3):
                        continue
                
                safe_url = "".join(c for c in url if c.isalnum() or c in (' ', '-', '_'))[:50]
                filename = f"article_{exported_count + 1}_{safe_url}.txt"
                
                content = []
                content.append("=" * 80)
                content.append("ARTICLE SCORING REPORT")
                content.append("=" * 80)
                content.append("")
                content.append(f"URL: {url}")
                content.append("")
                content.append(f"OVERALL AVERAGE SCORE: {avg:.2f} / 10")
                content.append(f"NUMBER OF PEER SCORES: {len(scores)}")
                content.append("")
                
                content.append("-" * 80)
                content.append("CATEGORY AVERAGES")
                content.append("-" * 80)
                content.append("")
                
                for cat in categories:
                    cat_scores = [s.get(cat, 0) for s in scores]
                    cat_avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
                    content.append(f"{cat.title():30s}: {cat_avg:.2f} / 10")
                
                if include_details:
                    content.append("")
                    content.append("-" * 80)
                    content.append("DETAILED SCORES")
                    content.append("-" * 80)
                    content.append("")
                    
                    for i, score in enumerate(scores, 1):
                        content.append(f"Score #{i}")
                        content.append(f"Timestamp: {score.get('timestamp', 'Unknown')}")
                        content.append("")
                        
                        for cat in categories:
                            content.append(f"  {cat.title():20s}: {score.get(cat, 0)} / 10")
                        
                        if include_notes and score.get('notes'):
                            content.append(f"\n  Notes: {score['notes']}")
                        
                        content.append("")
                
                zip_file.writestr(filename, '\n'.join(content))
                exported_count += 1
        
        if exported_count == 0:
            return jsonify({'error': 'No articles match the selected criteria'}), 400
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'article_scores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        )
    
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/api/export/json', methods=['POST'])
@login_required
def export_json():
    """Export scored articles to JSON file"""
    try:
        params = request.json
        score_range = params.get('scoreRange', 'All')
        
        scores_data = db.get_all_scores()
        categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'score_range_filter': score_range,
            'articles': []
        }
        
        for url, scores in scores_data.items():
            if not scores:
                continue
            
            avg = sum(s.get(cat, 0) for s in scores for cat in categories) / (len(scores) * len(categories))
            
            if score_range != "All":
                if score_range == "9-10" and not (9 <= avg <= 10):
                    continue
                elif score_range == "7-8" and not (7 <= avg <= 8):
                    continue
                elif score_range == "4-6" and not (4 <= avg <= 6):
                    continue
                elif score_range == "1-3" and not (1 <= avg <= 3):
                    continue
            
            cat_avgs = {}
            for cat in categories:
                cat_scores = [s.get(cat, 0) for s in scores]
                cat_avgs[cat] = sum(cat_scores) / len(cat_scores) if cat_scores else 0
            
            article_data = {
                'url': url,
                'overall_average': round(avg, 2),
                'peer_scores_count': len(scores),
                'category_averages': {k: round(v, 2) for k, v in cat_avgs.items()},
                'individual_scores': scores
            }
            
            export_data['articles'].append(article_data)
        
        if not export_data['articles']:
            return jsonify({'error': 'No articles match the selected criteria'}), 400
        
        json_buffer = io.BytesIO()
        json_buffer.write(json.dumps(export_data, indent=2, ensure_ascii=False).encode('utf-8'))
        json_buffer.seek(0)
        
        return send_file(
            json_buffer,
            mimetype='application/json',
            as_attachment=True,
            download_name=f'article_scores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
    
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/api/export/urls', methods=['POST'])
@login_required
def export_urls():
    """Export plain list of URLs (one per line)"""
    try:
        params = request.json
        score_range = params.get('scoreRange', 'All')
        only_scored = params.get('onlyScored', False)
        
        articles_list = db.get_all_articles()
        scores_data = db.get_all_scores()
        categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        
        urls_to_export = []
        
        for article in articles_list:
            url = article['URL']
            scores = scores_data.get(url, [])
            
            # Filter by scored/unscored
            if only_scored and not scores:
                continue
            
            # Filter by score range
            if scores and score_range != "All":
                avg = sum(s.get(cat, 0) for s in scores for cat in categories) / (len(scores) * len(categories))
                
                if score_range == "9-10" and not (9 <= avg <= 10):
                    continue
                elif score_range == "7-8" and not (7 <= avg <= 8):
                    continue
                elif score_range == "4-6" and not (4 <= avg <= 6):
                    continue
                elif score_range == "1-3" and not (1 <= avg <= 3):
                    continue
            elif not scores and score_range != "All":
                continue
            
            urls_to_export.append(url)
        
        if not urls_to_export:
            return jsonify({'error': 'No URLs match the selected criteria'}), 400
        
        # Create plain text file with one URL per line
        url_buffer = io.BytesIO()
        url_buffer.write('\n'.join(urls_to_export).encode('utf-8'))
        url_buffer.seek(0)
        
        return send_file(
            url_buffer,
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'article_urls_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        )
    
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Check if password has been changed
    if get_password_hash() == DEFAULT_PASSWORD_HASH:
        print("\n" + "⚠️ " * 20)
        print("WARNING: Using default password 'scoring2025'")
        print("Please set ADMIN_PASSWORD environment variable or change DEFAULT_PASSWORD_HASH in code")
        print("⚠️ " * 20 + "\n")
    
    print("\n" + "="*80)
    print("AI ARTICLE SCORING WEB APP (SECURE VERSION)")
    print("="*80)
    print(f"\n🌐 Access URL: http://localhost:{port}")
    print(f"🔒 Password protection enabled")
    print(f"🔑 Default password: scoring2025 (CHANGE THIS!)")
    print("\n⚠️  Set ADMIN_PASSWORD environment variable for production")
    print("\nPress CTRL+C to stop the server")
    print("="*80 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)



