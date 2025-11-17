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

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SCORES_FILE'] = 'article_scores.json'

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

def parse_txt_file(filepath):
    """Parse a .txt file with URLs (one per line or URL,Title format)"""
    articles = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ',' in line:
                parts = line.split(',', 1)
                url = parts[0].strip()
                title = parts[1].strip() if len(parts) > 1 else url
            else:
                url = line
                title = url[:50] + '...' if len(url) > 50 else url
            
            if url.startswith('http'):
                articles.append({'URL': url, 'Title': title})
    
    return pd.DataFrame(articles)

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

@app.route('/api/import', methods=['POST'])
@login_required
def import_file():
    """Import articles from uploaded file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath)
        elif filename.endswith('.txt'):
            df = parse_txt_file(filepath)
        else:
            return jsonify({'error': 'Unsupported file format. Use .csv, .xlsx, .xls, or .txt'}), 400
        
        if 'URL' not in df.columns:
            return jsonify({'error': 'File must contain a "URL" column'}), 400
        
        if 'Title' not in df.columns:
            df['Title'] = df['URL'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
        
        articles = df[['URL', 'Title']].to_dict('records')
        
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'articles': articles,
            'count': len(articles)
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to import file: {str(e)}'}), 500

@app.route('/api/scores', methods=['GET'])
@login_required
def get_scores():
    """Get all scores"""
    scores_data = load_scores()
    return jsonify(scores_data)

@app.route('/api/scores/<path:url>', methods=['GET'])
@login_required
def get_article_scores(url):
    """Get scores for a specific article"""
    scores_data = load_scores()
    article_scores = scores_data.get(url, [])
    
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
        
        scores_data = load_scores()
        if url not in scores_data:
            scores_data[url] = []
        
        scores_data[url].append(score_data)
        save_scores(scores_data)
        
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
    scores_data = load_scores()
    
    stats = {
        'total_articles': len(scores_data),
        'total_scores': sum(len(scores) for scores in scores_data.values()),
        'articles_with_scores': len([url for url, scores in scores_data.items() if scores]),
        'articles_without_scores': len([url for url, scores in scores_data.items() if not scores])
    }
    
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
        
        scores_data = load_scores()
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
        
        scores_data = load_scores()
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
