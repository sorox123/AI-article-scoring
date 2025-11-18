// Global state
let articles = [];
let scoresData = {};
let currentArticleUrl = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadArticles();
    loadScores();
});

function initializeEventListeners() {
    // Import button
    document.getElementById('importBtn').addEventListener('click', () => {
        showModal('importModal');
    });

    // Export button
    document.getElementById('exportBtn').addEventListener('click', () => {
        showModal('exportModal');
    });

    // Stats button
    document.getElementById('statsBtn').addEventListener('click', showStatistics);

    // File upload
    const fileInput = document.getElementById('fileInput');
    const fileUploadArea = document.getElementById('fileUploadArea');

    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadArea.classList.add('drag-over');
    });

    fileUploadArea.addEventListener('dragleave', () => {
        fileUploadArea.classList.remove('drag-over');
    });

    fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadArea.classList.remove('drag-over');
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect();
        }
    });

    // Search and filter
    document.getElementById('searchInput').addEventListener('input', filterArticles);
    document.getElementById('filterSelect').addEventListener('change', filterArticles);

    // Scoring sliders
    const sliders = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence'];
    sliders.forEach(category => {
        const slider = document.getElementById(`${category}Slider`);
        const valueDisplay = document.getElementById(`${category}Value`);
        slider.addEventListener('input', (e) => {
            valueDisplay.textContent = e.target.value;
        });
    });

    // Submit score
    document.getElementById('submitScoreBtn').addEventListener('click', submitScore);

    // Perform export
    document.getElementById('performExportBtn').addEventListener('click', performExport);

    // Export format toggle
    document.querySelectorAll('input[name="exportFormat"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            document.getElementById('txtOptions').style.display = 
                e.target.value === 'txt' ? 'block' : 'none';
            document.getElementById('urlOptions').style.display = 
                e.target.value === 'urls' ? 'block' : 'none';
        });
    });

    // Close modals
    document.querySelectorAll('.modal .close').forEach(closeBtn => {
        closeBtn.addEventListener('click', () => {
            closeBtn.closest('.modal').classList.remove('show');
        });
    });

    // Close modal on background click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
            }
        });
    });

    // Initialize import tabs
    initializeTabs();
    
    // Google Sheets import button
    const importSheetsBtn = document.getElementById('importSheetsBtn');
    if (importSheetsBtn) {
        importSheetsBtn.addEventListener('click', handleGoogleSheetsImport);
    }
    
    // Allow Enter key in Google Sheets URL field
    const sheetsUrlInput = document.getElementById('sheetsUrl');
    if (sheetsUrlInput) {
        sheetsUrlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleGoogleSheetsImport();
            }
        });
    }
}

function showModal(modalId) {
    document.getElementById(modalId).classList.add('show');
}

function hideModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

async function loadArticles() {
    try {
        const response = await fetch('/api/articles');
        if (response.ok) {
            const result = await response.json();
            articles = result.articles;
            if (articles.length > 0) {
                setStatus(`${result.count} article${result.count !== 1 ? 's' : ''} in database`);
                renderArticles();
            }
        }
    } catch (error) {
        console.error('Failed to load articles:', error);
    }
}

async function handleFileSelect() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) return;

    // Show progress
    document.getElementById('fileUploadArea').style.display = 'none';
    document.getElementById('uploadProgress').style.display = 'block';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/import', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            articles = result.articles;
            
            // Build status message
            let statusMsg = `Import complete: ${result.total_count} total articles`;
            if (result.new_count > 0) {
                statusMsg += ` (${result.new_count} new)`;
            }
            if (result.duplicate_count > 0) {
                statusMsg += ` - ${result.duplicate_count} duplicates removed`;
            }
            
            setStatus(statusMsg);
            
            // Show detailed feedback if duplicates found
            if (result.duplicate_count > 0 && result.duplicates.length > 0) {
                const dupList = result.duplicates.join(', ');
                console.log('Duplicate articles removed:', dupList);
            }
            
            renderArticles();
            hideModal('importModal');
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        alert(`Failed to import file: ${error.message}`);
    } finally {
        // Reset upload area
        document.getElementById('fileUploadArea').style.display = 'block';
        document.getElementById('uploadProgress').style.display = 'none';
        fileInput.value = '';
    }
}

async function loadScores() {
    try {
        const response = await fetch('/api/scores');
        scoresData = await response.json();
        if (articles.length > 0) {
            renderArticles();
        }
    } catch (error) {
        console.error('Failed to load scores:', error);
    }
}

function renderArticles() {
    const container = document.getElementById('articlesContainer');
    
    if (articles.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📚</div>
                <h2>No Articles Loaded</h2>
                <p>Click "Import Articles" to load your spreadsheet</p>
                <p class="supported-formats">Supported: .csv, .xlsx, .xls, .txt</p>
            </div>
        `;
        return;
    }

    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filterRange = document.getElementById('filterSelect').value;

    const filteredArticles = articles.filter(article => {
        // Search filter
        if (searchTerm) {
            const matchesSearch = 
                article.Title.toLowerCase().includes(searchTerm) ||
                article.URL.toLowerCase().includes(searchTerm);
            if (!matchesSearch) return false;
        }

        // Score filter
        const stats = getArticleStats(article.URL);
        const avgScore = stats.average;

        if (filterRange === 'Unscored' && avgScore > 0) return false;
        if (filterRange === '1-3' && (avgScore < 1 || avgScore > 3)) return false;
        if (filterRange === '4-6' && (avgScore < 4 || avgScore > 6)) return false;
        if (filterRange === '7-8' && (avgScore < 7 || avgScore > 8)) return false;
        if (filterRange === '9-10' && (avgScore < 9 || avgScore > 10)) return false;

        return true;
    });

    if (filteredArticles.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🔍</div>
                <h2>No Articles Found</h2>
                <p>Try adjusting your search or filter criteria</p>
            </div>
        `;
        return;
    }

    container.innerHTML = filteredArticles.map((article, index) => {
        const stats = getArticleStats(article.URL);
        const scoreClass = getScoreClass(stats.average);
        const scoreDisplay = stats.average > 0 ? stats.average.toFixed(1) : '-';

        return `
            <div class="article-card" data-url="${escapeHtml(article.URL)}">
                <div class="article-header">
                    <div class="article-number">#${index + 1}</div>
                    <div class="article-main">
                        <div class="article-title">${escapeHtml(article.Title)}</div>
                        <div class="article-url">${escapeHtml(article.URL)}</div>
                    </div>
                    <div class="article-score">
                        <span class="score-badge ${scoreClass}">${scoreDisplay}</span>
                        <div class="peer-count">${stats.count} ${stats.count === 1 ? 'score' : 'scores'}</div>
                    </div>
                </div>
                <div class="article-actions">
                    <button class="btn btn-primary btn-small" onclick="openScoringModal('${escapeHtml(article.URL)}', '${escapeHtml(article.Title)}')">
                        📝 Score Article
                    </button>
                    <button class="btn btn-secondary btn-small" onclick="openArticle('${escapeHtml(article.URL)}')">
                        🔗 Visit Article
                    </button>
                    <button class="btn btn-secondary btn-small" onclick="viewPeerScores('${escapeHtml(article.URL)}', '${escapeHtml(article.Title)}')">
                        📊 Peer Scores (${stats.count})
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function filterArticles() {
    renderArticles();
}

function getArticleStats(url) {
    const scores = scoresData[url] || [];
    
    if (scores.length === 0) {
        return { average: 0, count: 0 };
    }

    const categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence'];
    const total = scores.reduce((sum, score) => {
        return sum + categories.reduce((catSum, cat) => catSum + (score[cat] || 0), 0);
    }, 0);

    const average = total / (scores.length * categories.length);
    return { average, count: scores.length };
}

function getScoreClass(score) {
    if (score === 0) return 'score-unscored';
    if (score >= 9) return 'score-high';
    if (score >= 7) return 'score-good';
    if (score >= 4) return 'score-medium';
    return 'score-low';
}

function openScoringModal(url, title) {
    currentArticleUrl = url;
    document.getElementById('scoreArticleTitle').textContent = title;
    document.getElementById('scoreArticleUrl').href = url;
    
    // Reset sliders
    const sliders = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence'];
    sliders.forEach(category => {
        document.getElementById(`${category}Slider`).value = 5;
        document.getElementById(`${category}Value`).textContent = '5';
    });
    
    // Reset notes
    document.getElementById('notesInput').value = '';
    
    showModal('scoringModal');
}

function openArticle(url) {
    window.open(url, '_blank');
    setStatus(`Opened: ${url}`);
}

async function viewPeerScores(url, title) {
    document.getElementById('peerArticleTitle').textContent = title;
    document.getElementById('peerArticleUrl').href = url;
    
    try {
        const response = await fetch(`/api/scores/${encodeURIComponent(url)}`);
        const data = await response.json();
        
        const content = document.getElementById('peerScoresContent');
        
        if (data.count === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <p>No scores yet for this article.</p>
                </div>
            `;
        } else {
            const categories = ['accuracy', 'credibility', 'citation', 'reasoning', 'confidence'];
            
            let html = `
                <div class="stats-summary">
                    <h3>Overall Statistics</h3>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-label">Overall Average</div>
                            <div class="stat-value">${data.overall_average.toFixed(2)}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Total Scores</div>
                            <div class="stat-value">${data.count}</div>
                        </div>
                    </div>
                    <div class="stats-grid" style="margin-top: 16px;">
            `;
            
            categories.forEach(cat => {
                html += `
                    <div class="stat-item">
                        <div class="stat-label">${cat.charAt(0).toUpperCase() + cat.slice(1)}</div>
                        <div class="stat-value">${data.category_averages[cat].toFixed(2)}</div>
                    </div>
                `;
            });
            
            html += `</div></div><h3 style="margin: 24px 0 16px 0;">Individual Scores</h3>`;
            
            data.scores.forEach((score, index) => {
                html += `
                    <div class="peer-score-item">
                        <div class="peer-score-header">
                            Score #${index + 1} - ${new Date(score.timestamp).toLocaleString()}
                        </div>
                `;
                
                categories.forEach(cat => {
                    html += `
                        <div class="score-row">
                            <span class="score-label">${cat.charAt(0).toUpperCase() + cat.slice(1)}:</span>
                            <span class="score-value-text">${score[cat]} / 10</span>
                        </div>
                    `;
                });
                
                if (score.notes) {
                    html += `<div class="peer-notes"><strong>Notes:</strong> ${escapeHtml(score.notes)}</div>`;
                }
                
                html += `</div>`;
            });
            
            content.innerHTML = html;
        }
        
        showModal('peerScoresModal');
    } catch (error) {
        alert(`Failed to load peer scores: ${error.message}`);
    }
}

async function submitScore() {
    if (!currentArticleUrl) return;

    const scoreData = {
        accuracy: parseInt(document.getElementById('accuracySlider').value),
        credibility: parseInt(document.getElementById('credibilitySlider').value),
        citation: parseInt(document.getElementById('citationSlider').value),
        reasoning: parseInt(document.getElementById('reasoningSlider').value),
        confidence: parseInt(document.getElementById('confidenceSlider').value),
        notes: document.getElementById('notesInput').value.trim()
    };

    try {
        const response = await fetch(`/api/scores/${encodeURIComponent(currentArticleUrl)}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(scoreData)
        });

        const result = await response.json();

        if (response.ok) {
            setStatus('Score submitted successfully!');
            await loadScores();
            renderArticles();
            hideModal('scoringModal');
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        alert(`Failed to submit score: ${error.message}`);
    }
}

async function performExport() {
    console.log('Export function called');
    const scoreRange = document.querySelector('input[name="exportRange"]:checked').value;
    const exportFormat = document.querySelector('input[name="exportFormat"]:checked').value;
    
    const params = {
        scoreRange: scoreRange
    };

    if (exportFormat === 'txt') {
        params.includeDetails = document.getElementById('includeDetails').checked;
        params.includeNotes = document.getElementById('includeNotes').checked;
    }
    
    if (exportFormat === 'urls') {
        const onlyScoredEl = document.getElementById('onlyScored');
        const includeStatsEl = document.getElementById('includeStats');
        params.onlyScored = onlyScoredEl ? onlyScoredEl.checked : false;
        params.includeStats = includeStatsEl ? includeStatsEl.checked : false;
    }

    try {
        let endpoint;
        if (exportFormat === 'txt') {
            endpoint = '/api/export/txt';
        } else if (exportFormat === 'json') {
            endpoint = '/api/export/json';
        } else {
            endpoint = '/api/export/urls';
        }
        
        console.log('Fetching endpoint:', endpoint, 'with params:', params);
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            const contentDisposition = response.headers.get('content-disposition');
            let filename;
            if (contentDisposition) {
                filename = contentDisposition.split('filename=')[1].replace(/"/g, '');
            } else {
                if (exportFormat === 'txt') filename = 'export.zip';
                else if (exportFormat === 'json') filename = 'export.json';
                else filename = 'urls.txt';
            }
            
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            setStatus('Export completed successfully!');
            hideModal('exportModal');
        console.error('Export response not OK:', response.status, response.statusText);
            } else {
            const error = await response.json();
            alert(`Export failed: ${error.error}`);
        }
    } catch (error) {
        alert(`Export failed: ${error.message}`);
    }
}

async function showStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const stats = await response.json();
        
        const content = document.getElementById('statsContent');
        content.innerHTML = `
            <h3>Database Statistics</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-label">Total Articles</div>
                    <div class="stat-value">${stats.total_articles}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Total Scores</div>
                    <div class="stat-value">${stats.total_scores}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Articles with Scores</div>
                    <div class="stat-value">${stats.articles_with_scores}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Unscored Articles</div>
                    <div class="stat-value">${stats.articles_without_scores}</div>
                </div>
            </div>
        `;
        
        showModal('statsModal');
    } catch (error) {
        alert(`Failed to load statistics: ${error.message}`);
    }
}

function setStatus(message) {
    document.getElementById('statusBar').textContent = message;
}

// ===== Tab Switching =====
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const fileTab = document.getElementById('fileTab');
    const sheetsTab = document.getElementById('sheetsTab');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tab = button.getAttribute('data-tab');
            
            // Update button states
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show/hide tab content
            if (tab === 'file') {
                fileTab.classList.add('active');
                fileTab.style.display = 'block';
                sheetsTab.classList.remove('active');
                sheetsTab.style.display = 'none';
            } else if (tab === 'sheets') {
                sheetsTab.classList.add('active');
                sheetsTab.style.display = 'block';
                fileTab.classList.remove('active');
                fileTab.style.display = 'none';
            }
        });
    });
}

// ===== Google Sheets Import =====
async function handleGoogleSheetsImport() {
    const sheetsUrl = document.getElementById('sheetsUrl').value.trim();
    const sheetName = document.getElementById('sheetName').value.trim();

    if (!sheetsUrl) {
        showStatus('Please enter a Google Sheets URL', 'error');
        return;
    }

    // Validate URL format
    if (!sheetsUrl.includes('docs.google.com/spreadsheets')) {
        showStatus('Invalid Google Sheets URL. Please use a valid Google Sheets link.', 'error');
        return;
    }

    // Hide input area and show progress
    document.getElementById('sheetsTab').style.display = 'none';
    document.getElementById('uploadProgress').style.display = 'block';

    try {
        const requestBody = { url: sheetsUrl };
        if (sheetName) {
            requestBody.sheetName = sheetName;
        }

        const response = await fetch('/api/import/google-sheet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        const result = await response.json();

        if (response.ok) {
            articles = result.articles;

            // Build status message
            let statusMsg = `Import complete: ${result.total_count} total articles`;
            if (result.new_count > 0) {
                statusMsg += `, ${result.new_count} new`;
            }
            if (result.duplicate_count > 0) {
                statusMsg += `, ${result.duplicate_count} duplicates removed`;
            }

            showStatus(statusMsg, 'success');
            renderArticles();

            // Close modal and reset
            document.getElementById('importModal').style.display = 'none';
            document.getElementById('sheetsUrl').value = '';
            document.getElementById('sheetName').value = '';
        } else {
            showStatus(`Import failed: ${result.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Import error:', error);
        showStatus('Error importing from Google Sheets. Please try again.', 'error');
    } finally {
        // Reset UI
        document.getElementById('uploadProgress').style.display = 'none';
        document.getElementById('sheetsTab').style.display = 'block';
    }
}


function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}




