import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import json
import os
import webbrowser
from datetime import datetime
from pathlib import Path

class ArticleScoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Article Credibility Scoring App")
        self.root.geometry("1200x800")
        
        # Data storage
        self.articles_df = None
        self.scores_file = "article_scores.json"
        self.scores_data = self.load_scores()
        
        # Configure styles
        self.setup_styles()
        
        # Create main UI
        self.create_ui()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Score.TButton', font=('Arial', 10), padding=5)
        
    def load_scores(self):
        """Load existing scores from JSON file"""
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_scores(self):
        """Save scores to JSON file"""
        with open(self.scores_file, 'w', encoding='utf-8') as f:
            json.dump(self.scores_data, f, indent=2, ensure_ascii=False)
    
    def create_ui(self):
        """Create main user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(header_frame, text="AI Article Credibility Scoring", 
                 style='Title.TLabel').pack(side=tk.LEFT)
        
        # Control buttons
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Import Spreadsheet", 
                  command=self.import_spreadsheet).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export Results", 
                  command=self.export_results).pack(side=tk.LEFT, padx=5)
        
        # Search and filter frame
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_articles)
        ttk.Entry(filter_frame, textvariable=self.search_var, width=40).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Filter by score:").pack(side=tk.LEFT, padx=(20, 5))
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                    values=["All", "Unscored", "1-3", "4-6", "7-8", "9-10"],
                                    state='readonly', width=15)
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_articles())
        
        # Articles list frame
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create Treeview with scrollbars
        tree_scroll_y = ttk.Scrollbar(list_frame)
        tree_scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        tree_scroll_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.tree = ttk.Treeview(list_frame, 
                                 columns=('URL', 'Title', 'Avg Score', 'Scores Count'),
                                 show='tree headings',
                                 yscrollcommand=tree_scroll_y.set,
                                 xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading('#0', text='#')
        self.tree.heading('URL', text='URL')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Avg Score', text='Avg Score')
        self.tree.heading('Scores Count', text='Peer Scores')
        
        self.tree.column('#0', width=50, stretch=False)
        self.tree.column('URL', width=400)
        self.tree.column('Title', width=400)
        self.tree.column('Avg Score', width=100, anchor=tk.CENTER)
        self.tree.column('Scores Count', width=100, anchor=tk.CENTER)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_article_double_click)
        
        # Action buttons frame
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(action_frame, text="Score Article", 
                  command=self.open_scoring_window,
                  style='Score.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Visit Article", 
                  command=self.visit_article,
                  style='Score.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="View Peer Scores", 
                  command=self.view_peer_scores,
                  style='Score.TButton').pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready. Import a spreadsheet to begin.")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def import_spreadsheet(self):
        """Import articles from Excel or CSV file"""
        filetypes = [
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Spreadsheet",
            filetypes=filetypes
        )
        
        if not filename:
            return
        
        try:
            # Read file based on extension
            if filename.endswith('.csv'):
                df = pd.read_csv(filename)
            else:
                df = pd.read_excel(filename)
            
            # Validate required columns
            if 'URL' not in df.columns:
                messagebox.showerror("Error", "Spreadsheet must contain a 'URL' column")
                return
            
            # Add Title column if not present
            if 'Title' not in df.columns:
                df['Title'] = df['URL'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
            
            self.articles_df = df
            self.populate_articles_list()
            self.status_var.set(f"Loaded {len(df)} articles from {Path(filename).name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import spreadsheet:\n{str(e)}")
    
    def populate_articles_list(self):
        """Populate the articles list with data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.articles_df is None:
            return
        
        # Add articles to tree
        for idx, row in self.articles_df.iterrows():
            url = row['URL']
            title = row.get('Title', url[:50] + '...')
            
            # Get score statistics
            avg_score, count = self.get_article_stats(url)
            avg_display = f"{avg_score:.1f}" if avg_score > 0 else "-"
            
            self.tree.insert('', tk.END, text=str(idx + 1),
                           values=(url, title, avg_display, count))
    
    def filter_articles(self, *args):
        """Filter articles based on search and score range"""
        if self.articles_df is None:
            return
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_var.get().lower()
        filter_range = self.filter_var.get()
        
        for idx, row in self.articles_df.iterrows():
            url = row['URL']
            title = row.get('Title', url)
            
            # Apply search filter
            if search_term and search_term not in url.lower() and search_term not in title.lower():
                continue
            
            # Get score statistics
            avg_score, count = self.get_article_stats(url)
            
            # Apply score filter
            if filter_range != "All":
                if filter_range == "Unscored" and avg_score > 0:
                    continue
                elif filter_range == "1-3" and not (1 <= avg_score <= 3):
                    continue
                elif filter_range == "4-6" and not (4 <= avg_score <= 6):
                    continue
                elif filter_range == "7-8" and not (7 <= avg_score <= 8):
                    continue
                elif filter_range == "9-10" and not (9 <= avg_score <= 10):
                    continue
            
            avg_display = f"{avg_score:.1f}" if avg_score > 0 else "-"
            self.tree.insert('', tk.END, text=str(idx + 1),
                           values=(url, title, avg_display, count))
    
    def get_article_stats(self, url):
        """Get average score and count for an article"""
        if url not in self.scores_data:
            return 0, 0
        
        scores = self.scores_data[url]
        if not scores:
            return 0, 0
        
        # Calculate average of all category scores
        total_avg = 0
        count = len(scores)
        
        for score_entry in scores:
            categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
            avg = sum(score_entry.get(cat, 0) for cat in categories) / len(categories)
            total_avg += avg
        
        return total_avg / count if count > 0 else 0, count
    
    def on_article_double_click(self, event):
        """Handle double-click on article"""
        self.open_scoring_window()
    
    def get_selected_article(self):
        """Get currently selected article"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an article first")
            return None
        
        item = self.tree.item(selection[0])
        url = item['values'][0]
        title = item['values'][1]
        return {'url': url, 'title': title}
    
    def open_scoring_window(self):
        """Open the scoring window for selected article"""
        article = self.get_selected_article()
        if not article:
            return
        
        ScoringWindow(self.root, article, self)
    
    def visit_article(self):
        """Open article in default browser"""
        article = self.get_selected_article()
        if not article:
            return
        
        try:
            webbrowser.open(article['url'])
            self.status_var.set(f"Opened: {article['url']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open URL:\n{str(e)}")
    
    def view_peer_scores(self):
        """View all peer scores for selected article"""
        article = self.get_selected_article()
        if not article:
            return
        
        PeerScoresWindow(self.root, article, self)
    
    def add_score(self, url, score_data):
        """Add a new score for an article"""
        if url not in self.scores_data:
            self.scores_data[url] = []
        
        score_data['timestamp'] = datetime.now().isoformat()
        self.scores_data[url].append(score_data)
        self.save_scores()
        self.populate_articles_list()
    
    def export_results(self):
        """Export scored articles to text files"""
        if not self.scores_data:
            messagebox.showwarning("Warning", "No scores to export")
            return
        
        ExportDialog(self.root, self)


class ScoringWindow:
    """Window for scoring an article"""
    
    def __init__(self, parent, article, app):
        self.article = article
        self.app = app
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Score Article")
        self.window.geometry("800x900")
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_ui()
    
    def create_ui(self):
        """Create scoring interface"""
        # Main container with scrollbar
        canvas = tk.Canvas(self.window)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Article info
        info_frame = ttk.LabelFrame(scrollable_frame, text="Article Information", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text="Title:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=self.article['title'], wraplength=700).grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(info_frame, text="URL:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=(5,0))
        url_label = ttk.Label(info_frame, text=self.article['url'], wraplength=700, foreground='blue', cursor='hand2')
        url_label.grid(row=1, column=1, sticky=tk.W, padx=10, pady=(5,0))
        url_label.bind('<Button-1>', lambda e: webbrowser.open(self.article['url']))
        
        # Scoring categories
        self.scores = {}
        categories = [
            ('accuracy', 'Accuracy of Truthfulness', 
             'Ability to correctly classify stories as True (10-8), Partially True (7-4), or False (3-1)'),
            ('credibility', 'Author and Source Credibility Assessment',
             'Evaluation of author identity, publication reputation, and historical accuracy'),
            ('citation', 'Citation and Evidence Quality',
             'Extent of real, relevant, and verifiable references supporting claims'),
            ('reasoning', 'Reasoning Transparency',
             'Quality of logical explanation chain and coherence'),
            ('confidence', 'Confidence Calibration',
             'Alignment between stated confidence and actual correctness')
        ]
        
        for cat_id, cat_name, cat_desc in categories:
            self.create_scoring_category(scrollable_frame, cat_id, cat_name, cat_desc)
        
        # Notes section
        notes_frame = ttk.LabelFrame(scrollable_frame, text="Additional Notes (Optional)", padding="10")
        notes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.notes_text = tk.Text(notes_frame, height=5, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Submit Score", command=self.submit_score).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0,10))
    
    def create_scoring_category(self, parent, cat_id, cat_name, cat_desc):
        """Create a scoring category with slider"""
        frame = ttk.LabelFrame(parent, text=cat_name, padding="10")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Description
        desc_label = ttk.Label(frame, text=cat_desc, wraplength=750, foreground='gray')
        desc_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Score display and slider
        score_frame = ttk.Frame(frame)
        score_frame.pack(fill=tk.X)
        
        # Current score label
        score_var = tk.IntVar(value=5)
        self.scores[cat_id] = score_var
        
        score_label = ttk.Label(score_frame, text="Score: 5", font=('Arial', 12, 'bold'))
        score_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Slider
        slider = ttk.Scale(score_frame, from_=1, to=10, orient=tk.HORIZONTAL, 
                          variable=score_var, command=lambda v: self.update_score_label(score_label, v))
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Min/Max labels
        ttk.Label(score_frame, text="1 (Low)").pack(side=tk.LEFT, padx=5)
        ttk.Label(score_frame, text="10 (High)").pack(side=tk.LEFT, padx=5)
    
    def update_score_label(self, label, value):
        """Update score label when slider moves"""
        score = int(float(value))
        label.config(text=f"Score: {score}")
    
    def submit_score(self):
        """Submit the score"""
        score_data = {
            'accuracy': self.scores['accuracy'].get(),
            'credibility': self.scores['credibility'].get(),
            'citation': self.scores['citation'].get(),
            'reasoning': self.scores['reasoning'].get(),
            'confidence': self.scores['confidence'].get(),
            'notes': self.notes_text.get('1.0', tk.END).strip()
        }
        
        self.app.add_score(self.article['url'], score_data)
        
        messagebox.showinfo("Success", "Score submitted successfully!")
        self.window.destroy()


class PeerScoresWindow:
    """Window to view all peer scores for an article"""
    
    def __init__(self, parent, article, app):
        self.article = article
        self.app = app
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Peer Scores")
        self.window.geometry("900x600")
        
        self.window.transient(parent)
        
        self.create_ui()
    
    def create_ui(self):
        """Create peer scores display"""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Article info
        ttk.Label(main_frame, text=self.article['title'], 
                 font=('Arial', 12, 'bold'), wraplength=850).pack(anchor=tk.W, pady=(0, 10))
        
        # Scores display
        url = self.article['url']
        if url not in self.app.scores_data or not self.app.scores_data[url]:
            ttk.Label(main_frame, text="No scores yet for this article.").pack(pady=20)
            return
        
        scores = self.app.scores_data[url]
        
        # Statistics
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
        
        # Calculate averages
        for i, cat in enumerate(categories):
            cat_scores = [s.get(cat, 0) for s in scores]
            avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
            
            ttk.Label(stats_frame, text=f"{cat.title()}:", font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Label(stats_frame, text=f"{avg:.2f}").grid(
                row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Overall average
        overall_avg = sum(s.get(cat, 0) for s in scores for cat in categories) / (len(scores) * len(categories))
        ttk.Separator(stats_frame, orient=tk.HORIZONTAL).grid(row=len(categories), column=0, columnspan=2, 
                                                               sticky=(tk.W, tk.E), pady=5)
        ttk.Label(stats_frame, text="Overall Average:", font=('Arial', 11, 'bold')).grid(
            row=len(categories)+1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(stats_frame, text=f"{overall_avg:.2f}", font=('Arial', 11, 'bold'), 
                 foreground='blue').grid(row=len(categories)+1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Individual scores
        scores_frame = ttk.LabelFrame(main_frame, text=f"Individual Scores ({len(scores)} total)", padding="10")
        scores_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable text widget
        text_scroll = ttk.Scrollbar(scores_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(scores_frame, wrap=tk.WORD, yscrollcommand=text_scroll.set)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_scroll.config(command=text_widget.yview)
        
        # Display each score
        for i, score in enumerate(scores, 1):
            timestamp = score.get('timestamp', 'Unknown')
            text_widget.insert(tk.END, f"Score #{i} - {timestamp}\n", 'header')
            text_widget.insert(tk.END, f"  Accuracy: {score.get('accuracy', 0)}\n")
            text_widget.insert(tk.END, f"  Credibility: {score.get('credibility', 0)}\n")
            text_widget.insert(tk.END, f"  Citation: {score.get('citation', 0)}\n")
            text_widget.insert(tk.END, f"  Reasoning: {score.get('reasoning', 0)}\n")
            text_widget.insert(tk.END, f"  Confidence: {score.get('confidence', 0)}\n")
            if score.get('notes'):
                text_widget.insert(tk.END, f"  Notes: {score['notes']}\n")
            text_widget.insert(tk.END, "\n" + "-"*80 + "\n\n")
        
        text_widget.tag_config('header', font=('Arial', 10, 'bold'))
        text_widget.config(state=tk.DISABLED)


class ExportDialog:
    """Dialog for exporting results"""
    
    def __init__(self, parent, app):
        self.app = app
        
        self.window = tk.Toplevel(parent)
        self.window.title("Export Results")
        self.window.geometry("500x400")
        
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_ui()
    
    def create_ui(self):
        """Create export dialog UI"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Export Scored Articles", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Score range selection
        range_frame = ttk.LabelFrame(main_frame, text="Score Range Filter", padding="10")
        range_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.range_var = tk.StringVar(value="All")
        
        ranges = [
            ("All scored articles", "All"),
            ("High (9-10)", "9-10"),
            ("Good (7-8)", "7-8"),
            ("Medium (4-6)", "4-6"),
            ("Low (1-3)", "1-3")
        ]
        
        for text, value in ranges:
            ttk.Radiobutton(range_frame, text=text, value=value, 
                           variable=self.range_var).pack(anchor=tk.W, pady=2)
        
        # Export options
        options_frame = ttk.LabelFrame(main_frame, text="Export Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.include_details = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include detailed scores", 
                       variable=self.include_details).pack(anchor=tk.W, pady=2)
        
        self.include_notes = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include notes", 
                       variable=self.include_notes).pack(anchor=tk.W, pady=2)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=(10, 0))
        
        ttk.Button(btn_frame, text="Export", command=self.export).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def export(self):
        """Perform the export"""
        score_range = self.range_var.get()
        
        # Ask for directory
        directory = filedialog.askdirectory(title="Select Export Directory")
        if not directory:
            return
        
        try:
            exported_count = 0
            
            for url, scores in self.app.scores_data.items():
                if not scores:
                    continue
                
                # Calculate average
                categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence']
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
                filepath = os.path.join(directory, filename)
                
                # Write file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write("ARTICLE SCORING REPORT\n")
                    f.write("=" * 80 + "\n\n")
                    
                    f.write(f"URL: {url}\n\n")
                    f.write(f"OVERALL AVERAGE SCORE: {avg:.2f} / 10\n")
                    f.write(f"NUMBER OF PEER SCORES: {len(scores)}\n\n")
                    
                    # Category averages
                    f.write("-" * 80 + "\n")
                    f.write("CATEGORY AVERAGES\n")
                    f.write("-" * 80 + "\n\n")
                    
                    for cat in categories:
                        cat_scores = [s.get(cat, 0) for s in scores]
                        cat_avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
                        f.write(f"{cat.title():30s}: {cat_avg:.2f} / 10\n")
                    
                    if self.include_details.get():
                        f.write("\n" + "-" * 80 + "\n")
                        f.write("DETAILED SCORES\n")
                        f.write("-" * 80 + "\n\n")
                        
                        for i, score in enumerate(scores, 1):
                            f.write(f"Score #{i}\n")
                            f.write(f"Timestamp: {score.get('timestamp', 'Unknown')}\n\n")
                            
                            for cat in categories:
                                f.write(f"  {cat.title():20s}: {score.get(cat, 0)} / 10\n")
                            
                            if self.include_notes.get() and score.get('notes'):
                                f.write(f"\n  Notes: {score['notes']}\n")
                            
                            f.write("\n")
                
                exported_count += 1
            
            messagebox.showinfo("Success", f"Exported {exported_count} articles to:\n{directory}")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")


def main():
    root = tk.Tk()
    app = ArticleScoringApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
