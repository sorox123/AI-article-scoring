# 🚀 Complete Deployment Guide

## 📋 Table of Contents
1. [Quick Deploy (Render.com)](#quick-deploy-rendercom)
2. [Alternative Platforms](#alternative-platforms)
3. [Squarespace Integration](#squarespace-integration)
4. [Security Setup](#security-setup)
5. [Custom Domain](#custom-domain)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Quick Deploy (Render.com) - FREE

### Prerequisites
- GitHub account
- Git installed locally

### Step 1: Prepare Your Code

```powershell
cd c:\Users\sorox\ai-news-scraper

# Create .gitignore
@"
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
uploads/
article_scores.json
.env
*.log
"@ | Out-File -FilePath .gitignore -Encoding utf8

# Initialize git repository
git init
git add .
git commit -m "Initial commit: AI Article Scoring App"
```

### Step 2: Push to GitHub

1. Go to **https://github.com** and create a new repository
   - Name: `ai-article-scoring`
   - Description: "AI Article Credibility Scoring Web App"
   - Public or Private: Your choice
   - Don't initialize with README

2. Push your code:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/ai-article-scoring.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render

1. **Sign up at Render.com**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub account
   - Select your repository: `ai-article-scoring`

3. **Configure Service**
   ```
   Name: ai-article-scoring
   Region: Oregon (or closest to you)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements_deploy.txt
   Start Command: gunicorn webapp_secure:app
   Instance Type: Free
   ```

4. **Set Environment Variables**
   
   Click **"Advanced"** → **"Add Environment Variable"**
   
   Add these:
   ```
   SECRET_KEY=your-random-secret-key-here-change-this
   ADMIN_PASSWORD=your-secure-password-here
   FLASK_ENV=production
   ```
   
   Generate secret key:
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Deploy**
   - Click **"Create Web Service"**
   - Wait 5-10 minutes for deployment
   - Your app will be live at: `https://your-app-name.onrender.com`

### Step 4: Test Your Deployment

1. Visit your Render URL
2. You should see the login page
3. Enter your `ADMIN_PASSWORD`
4. Test importing a file
5. Test scoring an article
6. Test export functionality

**✅ Your app is now publicly accessible!**

---

## 🔄 Alternative Platforms

### Railway.app ($5/month)

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
cd c:\Users\sorox\ai-news-scraper
railway login
railway init
railway up

# Set environment variables
railway variables set ADMIN_PASSWORD=your-password
railway variables set SECRET_KEY=your-secret-key
```

### PythonAnywhere (Free tier available)

1. Sign up at https://www.pythonanywhere.com
2. Go to **"Files"** tab
3. Upload all files:
   - `webapp_secure.py`
   - `requirements_deploy.txt`
   - `templates/` folder
   - `static/` folder
4. Go to **"Web"** tab
5. Create new web app (Flask)
6. Set WSGI file to point to `webapp_secure.py`
7. Open Bash console:
   ```bash
   pip3 install --user -r requirements_deploy.txt
   ```
8. Set environment variables in WSGI file
9. Reload web app

Your app: `https://yourusername.pythonanywhere.com`

### DigitalOcean App Platform ($5/month)

1. Sign up at https://www.digitalocean.com
2. Go to **"Apps"** → **"Create App"**
3. Connect GitHub repository
4. DigitalOcean auto-detects Python
5. Set environment variables
6. Deploy

### Heroku (Starting $5/month)

```powershell
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login and deploy
cd c:\Users\sorox\ai-news-scraper
heroku login
heroku create ai-article-scoring
git push heroku main

# Set environment variables
heroku config:set ADMIN_PASSWORD=your-password
heroku config:set SECRET_KEY=your-secret-key

# Open app
heroku open
```

---

## 🌐 Squarespace Integration

### Method 1: Direct Link (Easiest)

1. **In Squarespace Editor:**
   - Go to any page
   - Add a **Button** block
   - Set button text: "Access Scoring Tool"
   - Set URL: `https://your-app.onrender.com`
   - Style: Primary button
   - Open in: New window

2. **In Navigation Menu:**
   - **Settings** → **Navigation**
   - Add external link
   - Label: "Article Scoring"
   - URL: `https://your-app.onrender.com`

### Method 2: Iframe Embed

1. **Create a new page in Squarespace**
   - Name: "Article Scoring Tool"

2. **Add Code Block:**
   ```html
   <div style="width: 100%; height: 90vh; min-height: 800px;">
     <iframe 
       src="https://your-app.onrender.com" 
       width="100%" 
       height="100%" 
       frameborder="0"
       style="border: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
       allow="clipboard-write"
     >
       Your browser doesn't support iframes. 
       <a href="https://your-app.onrender.com">Click here to access the tool</a>
     </iframe>
   </div>
   ```

3. **Style the page:**
   - Remove header/footer if desired
   - Set page to full width
   - Adjust iframe height as needed

### Method 3: Custom Subdomain (Professional)

**Requirements:**
- Business Squarespace plan or higher
- Custom domain

**Steps:**

1. **In Render/Railway:**
   - Go to **Settings**
   - Add **Custom Domain**
   - Enter: `scoring.yourdomain.com`
   - Note the CNAME target

2. **In Squarespace:**
   - **Settings** → **Domains** → **DNS Settings**
   - Add CNAME record:
     ```
     Host: scoring
     Points to: your-app.onrender.com
     TTL: 3600
     ```

3. **Wait for DNS propagation** (up to 48 hours, usually < 1 hour)

4. **Access at:** `https://scoring.yourdomain.com`

### Method 4: Landing Page

Create a dedicated landing page on Squarespace:

```html
<!-- Hero Section -->
<div class="hero-section" style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
  <h1 style="font-size: 42px; margin-bottom: 20px;">
    🎯 AI Article Credibility Scoring
  </h1>
  <p style="font-size: 20px; margin-bottom: 30px;">
    Evaluate AI news articles on 5 key credibility metrics
  </p>
  <a href="https://your-app.onrender.com" 
     style="display: inline-block; padding: 15px 40px; background: white; color: #667eea; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px;">
    Launch Scoring Tool →
  </a>
</div>

<!-- Features Section -->
<div style="max-width: 1200px; margin: 60px auto; padding: 0 20px;">
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px;">
    
    <div style="text-align: center; padding: 30px;">
      <div style="font-size: 48px; margin-bottom: 15px;">📊</div>
      <h3>5 Scoring Categories</h3>
      <p>Accuracy, Credibility, Citation, Reasoning, Confidence</p>
    </div>
    
    <div style="text-align: center; padding: 30px;">
      <div style="font-size: 48px; margin-bottom: 15px;">👥</div>
      <h3>Peer Scoring</h3>
      <p>View and compare scores from multiple reviewers</p>
    </div>
    
    <div style="text-align: center; padding: 30px;">
      <div style="font-size: 48px; margin-bottom: 15px;">📱</div>
      <h3>Mobile Friendly</h3>
      <p>Score articles from any device, anywhere</p>
    </div>
    
    <div style="text-align: center; padding: 30px;">
      <div style="font-size: 48px; margin-bottom: 15px;">💾</div>
      <h3>Export Results</h3>
      <p>Download scores as TXT or JSON for analysis</p>
    </div>
    
  </div>
</div>

<!-- CTA Section -->
<div style="text-align: center; padding: 60px 20px; background: #f7fafc;">
  <h2 style="margin-bottom: 20px;">Ready to Start Scoring?</h2>
  <p style="margin-bottom: 30px; color: #718096;">
    Access the tool with your team password
  </p>
  <a href="https://your-app.onrender.com" 
     style="display: inline-block; padding: 15px 40px; background: #667eea; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">
    Access Tool →
  </a>
</div>
```

---

## 🔒 Security Setup

### Change Default Password

**Method 1: Environment Variable (Recommended)**

On Render/Railway/Heroku:
```
ADMIN_PASSWORD=your-secure-password-123
```

**Method 2: Edit Code**

In `webapp_secure.py`, change:
```python
DEFAULT_PASSWORD_HASH = generate_password_hash('scoring2025')
```
to:
```python
DEFAULT_PASSWORD_HASH = generate_password_hash('your-new-password')
```

### Generate Secure Password

```powershell
# Random password
python -c "import secrets; print(secrets.token_urlsafe(16))"

# Or use a password manager
# 1Password, LastPass, Bitwarden, etc.
```

### Enable HTTPS

All recommended platforms provide automatic HTTPS:
- ✅ Render: Automatic
- ✅ Railway: Automatic
- ✅ PythonAnywhere: Automatic
- ✅ Heroku: Automatic

### Additional Security (Optional)

**Rate Limiting:**

Install Flask-Limiter:
```powershell
pip install Flask-Limiter
```

Add to `webapp_secure.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

**CORS Protection:**

Install Flask-CORS:
```powershell
pip install Flask-CORS
```

Add to `webapp_secure.py`:
```python
from flask_cors import CORS
CORS(app, origins=["https://yourdomain.com"])
```

---

## 🌍 Custom Domain Setup

### Option 1: Through Hosting Platform

**Render.com:**
1. Go to your service → **Settings**
2. Click **"Add Custom Domain"**
3. Enter your domain: `scoring.yourdomain.com`
4. Add CNAME record in your DNS:
   - Host: `scoring`
   - Points to: `your-app.onrender.com`
5. Wait for SSL certificate (automatic)

**Railway.app:**
1. Go to your project → **Settings**
2. Under **"Domains"**, click **"Add Domain"**
3. Enter domain and follow instructions
4. Railway provides SSL automatically

### Option 2: Cloudflare (Recommended)

Benefits:
- ✅ Free SSL
- ✅ DDoS protection
- ✅ CDN (faster loading)
- ✅ Analytics

Setup:
1. Sign up at https://cloudflare.com
2. Add your domain
3. Update nameservers at your registrar
4. Add CNAME record:
   - Name: `scoring`
   - Target: `your-app.onrender.com`
   - Proxy status: Proxied (orange cloud)
5. SSL/TLS mode: **Full (strict)**

---

## 🐛 Troubleshooting

### Deployment Fails

**Error: "Build failed"**
- Check `requirements_deploy.txt` exists
- Verify Python version in `runtime.txt`
- Check build logs for specific error

**Error: "Application Error"**
- Check Start Command: `gunicorn webapp_secure:app`
- Verify all files uploaded to GitHub
- Check environment variables are set

### App Crashes

**Error: "H10 App Crashed"**
- Check logs on hosting platform
- Common issue: Missing environment variables
- Verify gunicorn is in requirements

**Error: "502 Bad Gateway"**
- App is starting, wait 30 seconds
- Check if port binding is correct
- Review application logs

### Login Issues

**Can't login with password**
- Check ADMIN_PASSWORD environment variable
- Try default: `scoring2025`
- Generate new password hash if edited code

### File Upload Fails

**Error: "File too large"**
- Max size is 16MB by default
- Increase in webapp_secure.py:
  ```python
  app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
  ```

### Data Loss After Restart

**Problem: Scores disappear**
- Free tiers have ephemeral storage
- Solution: Use persistent storage add-on
- Or: Upgrade to paid tier with persistent disk
- Or: Export scores regularly as backup

### Squarespace Iframe Not Working

**Problem: Iframe shows blank or error**
- Some platforms block iframe embedding
- Solution: Use direct link instead
- Or: Add X-Frame-Options header in app

---

## 📊 Monitoring & Maintenance

### Check App Health

**Render.com:**
- Dashboard shows uptime
- View logs: Service → **Logs** tab
- Metrics: CPU, Memory usage

**Railway.app:**
- Project → **Metrics**
- Real-time logs
- Build history

### Backup Data

**Manual Backup:**
```powershell
# Download article_scores.json from hosting platform
# Store in safe location

# Or use export feature in app:
# Export as JSON → Save locally
```

**Automated Backup:**
Set up GitHub Actions to backup daily:
```yaml
# .github/workflows/backup.yml
name: Daily Backup
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:
jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Download scores
        run: |
          curl https://your-app.onrender.com/api/export/all \
            -H "Cookie: session=your-session" \
            -o backup.json
      - name: Commit backup
        run: |
          git config user.name "Backup Bot"
          git config user.email "backup@example.com"
          git add backup.json
          git commit -m "Daily backup $(date)"
          git push
```

### Update Application

```powershell
# Make changes locally
git add .
git commit -m "Update: your changes"
git push

# Hosting platform auto-deploys from GitHub
# Wait 2-5 minutes for new version
```

---

## 📈 Scaling Considerations

### Current Limits (Free Tier)

- **Render:** 750 hours/month, sleeps after 15 min inactivity
- **Railway:** $5 credit/month (~40 hours)
- **PythonAnywhere:** 100 seconds CPU/day
- **Heroku:** Discontinued free tier

### When to Upgrade

Consider paid tier when:
- More than 10 concurrent users
- Need 24/7 uptime (no sleeping)
- Large file uploads (> 16MB)
- High traffic volume
- Need persistent storage

### Paid Tier Benefits

**Render ($7/month):**
- ✅ No sleeping
- ✅ Persistent disk
- ✅ Custom domains
- ✅ More CPU/RAM

**Railway ($5/month):**
- ✅ $5 usage credit
- ✅ Unlimited projects
- ✅ Priority support

---

## ✅ Final Checklist

Before going public:

- [ ] Password changed from default
- [ ] SECRET_KEY set to random value
- [ ] Environment variables configured
- [ ] App deployed and accessible
- [ ] Login tested
- [ ] File import tested
- [ ] Scoring functionality tested
- [ ] Export tested (TXT and JSON)
- [ ] Mobile responsiveness checked
- [ ] Squarespace integration completed
- [ ] Custom domain configured (optional)
- [ ] Backup strategy in place
- [ ] Team members can access
- [ ] Usage instructions shared

---

## 🎉 You're Live!

Your AI Article Scoring app is now:
- ✅ Publicly accessible
- ✅ Password protected
- ✅ Integrated with Squarespace
- ✅ Free or low-cost hosting
- ✅ SSL encrypted (HTTPS)

**Share your URL:**
`https://your-app-name.onrender.com`

**Default password:** `scoring2025` (change this!)

---

## 🆘 Need Help?

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app  
- **Flask Deployment:** https://flask.palletsprojects.com/deploying/
- **Check logs** on hosting platform for errors
- **Test locally first** before deploying

**Good luck with your deployment!** 🚀
