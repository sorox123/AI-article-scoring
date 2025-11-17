from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import pandas as pd
import json
import os
import secrets
from datetime import datetime
from pathlib import Path
import io

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SCORES_FILE'] = 'article_scores.json'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
            
            # Check if line has comma-separated URL and Title
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

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/import', methods=['POST'])
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
        
        # Parse file based on extension
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath)
        elif filename.endswith('.txt'):
            df = parse_txt_file(filepath)
        else:
            return jsonify({'error': 'Unsupported file format. Use .csv, .xlsx, .xls, or .txt'}), 400
        
        # Validate required columns
        if 'URL' not in df.columns:
            return jsonify({'error': 'File must contain a "URL" column'}), 400
        
        # Add Title column if not present
        if 'Title' not in df.columns:
            df['Title'] = df['URL'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
        
        # Convert to list of dicts
        articles = df[['URL', 'Title']].to_dict('records')
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'articles': articles,
            'count': len(articles)
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to import file: {str(e)}'}), 500

@app.route('/api/scores', methods=['GET'])
def get_scores():
    """Get all scores"""
    scores_data = load_scores()
    return jsonify(scores_data)

@app.route('/api/scores/<path:url>', methods=['GET'])
def get_article_scores(url):
    """Get scores for a specific article"""
    scores_data = load_scores()
    article_scores = scores_data.get(url, [])
    
    # Calculate statistics
    if article_scores:
        categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        
        # Category averages
        cat_avgs = {}
        for cat in categories:
            cat_scores = [s.get(cat, 0) for s in article_scores]
            cat_avgs[cat] = sum(cat_scores) / len(cat_scores) if cat_scores else 0
        
        # Overall average
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
def add_score(url):
    """Add a score for an article"""
    try:
        score_data = request.json
        
        # Validate score data
        required_fields = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        for field in required_fields:
            if field not in score_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
            
            score_value = score_data[field]
            if not isinstance(score_value, (int, float)) or score_value < 1 or score_value > 10:
                return jsonify({'error': f'Invalid score for {field}: must be between 1 and 10'}), 400
        
        # Add timestamp
        score_data['timestamp'] = datetime.now().isoformat()
        
        # Load, update, and save scores
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
def export_txt():
    """Export scored articles to text files"""
    try:
        params = request.json
        score_range = params.get('scoreRange', 'All')
        include_details = params.get('includeDetails', True)
        include_notes = params.get('includeNotes', True)
        
        scores_data = load_scores()
        categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        
        # Create in-memory zip file
        from io import BytesIO
        import zipfile
        
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            exported_count = 0
            
            for url, scores in scores_data.items():
                if not scores:
                    continue
                
                # Calculate average
                avg = sum(s.get(cat, 0) for s in scores for cat in categories) / (len(scores) * len(categories))
                
                # Apply filter
                if score_range != "All":
                    if score_range == "9-10" and not (9 <= avg <= 10):
                        continue
                    elif score_range == "7-8" and not (7 <= avg <= 8):
                        continue
                    elif score_range == "4-6" and not (4 <= avg <= 6):
                        continue
                    elif score_range == "1-3" and not (1 <= avg <= 3):
                        continue
                
                # Create filename
                safe_url = "".join(c for c in url if c.isalnum() or c in (' ', '-', '_'))[:50]
                filename = f"article_{exported_count + 1}_{safe_url}.txt"
                
                # Build content
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
                
                # Category averages
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
                
                # Add to zip
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
def export_json():
    """Export scored articles to JSON file"""
    try:
        params = request.json
        score_range = params.get('scoreRange', 'All')
        
        scores_data = load_scores()
        categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        
        # Filter and enhance data
        export_data = {
            'export_date': datetime.now().isoformat(),
            'score_range_filter': score_range,
            'articles': []
        }
        
        for url, scores in scores_data.items():
            if not scores:
                continue
            
            # Calculate statistics
            avg = sum(s.get(cat, 0) for s in scores for cat in categories) / (len(scores) * len(categories))
            
            # Apply filter
            if score_range != "All":
                if score_range == "9-10" and not (9 <= avg <= 10):
                    continue
                elif score_range == "7-8" and not (7 <= avg <= 8):
                    continue
                elif score_range == "4-6" and not (4 <= avg <= 6):
                    continue
                elif score_range == "1-3" and not (1 <= avg <= 3):
                    continue
            
            # Category averages
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
        
        # Create JSON file
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

@app.route('/api/export/all', methods=['GET'])
def export_all_json():
    """Export complete database as JSON"""
    try:
        scores_data = load_scores()
        
        json_buffer = io.BytesIO()
        json_buffer.write(json.dumps(scores_data, indent=2, ensure_ascii=False).encode('utf-8'))
        json_buffer.seek(0)
        
        return send_file(
            json_buffer,
            mimetype='application/json',
            as_attachment=True,
            download_name=f'all_scores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
    
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Generate a random port for security through obscurity
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*80)
    print("AI ARTICLE SCORING WEB APP")
    print("="*80)
    print(f"\n🌐 Access URL: http://localhost:{port}")
    print(f"🔒 Share this URL with others to grant access")
    print("\n⚠️  Keep this URL private - anyone with the link can access the app")
    print("\nPress CTRL+C to stop the server")
    print("="*80 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
