# 🌍 Public Deployment Guide

## Important: Squarespace Limitations

**⚠️ Squarespace does not support hosting Python/Flask applications directly.**

Squarespace is a website builder for static content (HTML/CSS/JavaScript) and cannot run Python backend servers.

## ✅ Recommended Hosting Solutions

### Option 1: Free Hosting Platforms (RECOMMENDED)

#### 🔷 **Render.com** (Best for Flask apps - FREE tier available)
- ✅ Free tier with automatic SSL
- ✅ Easy deployment from GitHub
- ✅ Automatic restarts
- ✅ Custom domains supported
- ⏱️ Setup time: 10 minutes

#### 🔷 **Railway.app** (Great for beginners - $5/month)
- ✅ Simple deployment
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⏱️ Setup time: 5 minutes

#### 🔷 **PythonAnywhere** (Python-specific - Free tier)
- ✅ Python-focused hosting
- ✅ Free tier available
- ✅ Web-based console
- ⏱️ Setup time: 15 minutes

#### 🔷 **Heroku** (Popular choice - $5-7/month)
- ✅ Widely used
- ✅ Good documentation
- ✅ Add-ons available
- ⏱️ Setup time: 15 minutes

### Option 2: Connect to Squarespace

You can:
1. Host the Flask app on a platform above
2. Create a page on your Squarespace site
3. Embed the app using an iframe or link to it

---

## 🚀 Quick Deploy to Render.com (FREE)

### Step 1: Prepare for Deployment

I've created all necessary files for you. Just follow these steps:

### Step 2: Create GitHub Repository

```powershell
cd c:\Users\sorox\ai-news-scraper

# Initialize git (if not already)
git init

# Add files
git add webapp.py templates/ static/ webapp_requirements.txt Procfile runtime.txt

# Commit
git commit -m "Initial commit - AI Article Scoring Web App"

# Create repo on GitHub and push
# (Follow GitHub's instructions to create new repo)
git remote add origin https://github.com/YOUR_USERNAME/ai-scoring-app.git
git push -u origin main
```

### Step 3: Deploy to Render

1. Go to **https://render.com** and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `ai-article-scoring`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r webapp_requirements.txt`
   - **Start Command:** `gunicorn webapp:app`
   - **Plan:** `Free`
5. Click **"Create Web Service"**

**Your app will be live at:** `https://ai-article-scoring.onrender.com`

### Step 4: Access Your Public App

Once deployed, share this URL with anyone:
- `https://your-app-name.onrender.com`

⚠️ **Security Note:** Anyone with the URL can access. Consider adding authentication for sensitive data.

---

## 🚀 Alternative: Deploy to Railway.app

### Step 1: Install Railway CLI

```powershell
npm install -g @railway/cli
```

### Step 2: Deploy

```powershell
cd c:\Users\sorox\ai-news-scraper

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

**Done!** Railway provides a URL automatically.

---

## 🚀 Alternative: Deploy to PythonAnywhere

### Step 1: Sign Up
Go to **https://www.pythonanywhere.com** and create free account

### Step 2: Upload Files
1. Go to **Files** tab
2. Upload your files:
   - `webapp.py`
   - `webapp_requirements.txt`
   - `templates/` folder
   - `static/` folder

### Step 3: Configure Web App
1. Go to **Web** tab
2. Click **"Add a new web app"**
3. Choose **Flask**
4. Set WSGI configuration to point to `webapp.py`
5. Install requirements in console:
   ```bash
   pip3 install --user -r webapp_requirements.txt
   ```

### Step 4: Access
Your app will be at: `https://yourusername.pythonanywhere.com`

---

## 🔗 Integrating with Squarespace

### Option A: Direct Link (Simple)

Add a link on your Squarespace site:

1. Go to your Squarespace editor
2. Add a **Button** or **Link** block
3. Set the URL to your deployed app:
   - `https://your-app-name.onrender.com`
4. Text: "AI Article Scoring Tool"

### Option B: Iframe Embed (Advanced)

Embed the app directly in a Squarespace page:

1. Go to your Squarespace page editor
2. Add a **Code Block**
3. Paste this HTML:

```html
<iframe 
  src="https://your-app-name.onrender.com" 
  width="100%" 
  height="800px" 
  frameborder="0"
  style="border: 2px solid #e2e8f0; border-radius: 12px;">
</iframe>
```

4. Save and publish

**Note:** Some hosting platforms may block iframe embedding. Test first.

### Option C: Subdomain (Professional)

1. Deploy app to Render/Railway/etc.
2. Get custom domain from your host
3. Add CNAME record in Squarespace DNS:
   - **Host:** `scoring` (or any name)
   - **Points to:** Your app's URL
4. Access at: `https://scoring.yourdomain.com`

---

## 🔒 Security Considerations

### ⚠️ Important: Add Authentication

Your app currently has **no authentication**. Anyone with the URL can:
- View all articles
- Add scores
- Export data

### Quick Fix: Add Basic Auth

I've created a secure version with password protection. See `webapp_secure.py`.

### Better Solution: OAuth

For production, consider:
- Google OAuth
- GitHub OAuth
- Email-based authentication

---

## 💰 Hosting Costs Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Render.com** | ✅ Yes (with limits) | $7/mo | Flask apps |
| **Railway.app** | ❌ No | $5/mo | Simple deploy |
| **PythonAnywhere** | ✅ Yes | $5/mo | Python apps |
| **Heroku** | ❌ No (discontinued) | $7/mo | Large apps |
| **DigitalOcean** | ❌ No | $5/mo | Full control |
| **AWS/Azure** | ⚠️ Complex | Varies | Enterprise |

**Recommendation for starting:** Use **Render.com free tier**

---

## 📋 Pre-Deployment Checklist

Before making your app public:

- [ ] Add authentication (password protection)
- [ ] Test all features thoroughly
- [ ] Backup `article_scores.json` regularly
- [ ] Set up error logging
- [ ] Configure custom domain (optional)
- [ ] Add rate limiting (prevent abuse)
- [ ] Review security settings
- [ ] Test on mobile devices
- [ ] Add privacy policy (if collecting data)
- [ ] Set up monitoring/alerts

---

## 🛠️ Production Configuration

### Environment Variables

Set these on your hosting platform:

```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
MAX_UPLOAD_SIZE=16777216
```

### Database Considerations

Current setup uses JSON file (`article_scores.json`). For production:

**Pros of JSON:**
- ✅ Simple
- ✅ No database needed
- ✅ Easy backups

**Cons of JSON:**
- ❌ Not ideal for concurrent users
- ❌ File locking issues possible
- ❌ Scalability limits

**Consider upgrading to PostgreSQL for:**
- Multiple simultaneous users
- Better data integrity
- Easier scaling

---

## 🎯 Quick Start: Deploy to Render in 10 Minutes

1. **Create account:** https://render.com (free)

2. **Create GitHub repo:**
   ```powershell
   cd c:\Users\sorox\ai-news-scraper
   git init
   git add .
   git commit -m "Initial commit"
   # Push to GitHub
   ```

3. **Deploy on Render:**
   - Connect GitHub repo
   - Select "Web Service"
   - Use auto-detected settings
   - Click "Create"

4. **Get your URL:**
   - Render provides: `https://your-app.onrender.com`

5. **Share with world:**
   - Add link to Squarespace site
   - Share URL on social media
   - Send to collaborators

**That's it!** Your app is now public.

---

## 🔗 Squarespace Integration Examples

### Example 1: Navigation Link

In Squarespace:
1. **Design** → **Navigation**
2. Add new link:
   - **Label:** "Article Scoring"
   - **URL:** `https://your-app.onrender.com`
   - **Open in:** New window

### Example 2: Landing Page

Create a Squarespace page with:
- Title: "AI Article Credibility Scoring Tool"
- Description of the tool
- Big button linking to your app
- Instructions for users

### Example 3: Blog Post

Write a blog post about the tool:
- Explain its purpose
- Provide usage instructions
- Link to the live app
- Embed screenshots

---

## 📱 Mobile Optimization

Your web app is already mobile-responsive, but test on:
- [ ] iPhone (Safari)
- [ ] Android (Chrome)
- [ ] iPad (Safari)
- [ ] Small screens (< 400px)

---

## 🚨 Common Issues

### Issue: "Application Error"
**Solution:** Check logs on hosting platform. Usually missing dependencies.

### Issue: "502 Bad Gateway"
**Solution:** App crashed. Check start command and port configuration.

### Issue: "File upload fails"
**Solution:** Increase MAX_CONTENT_LENGTH in webapp.py

### Issue: "Slow loading"
**Solution:** Free tiers have limited resources. Consider upgrading.

### Issue: "Data lost after restart"
**Solution:** Use persistent storage. Render free tier restarts daily.

---

## 💾 Data Persistence on Free Tiers

**Problem:** Free hosting often has ephemeral storage (data lost on restart)

**Solutions:**

1. **Use external database** (PostgreSQL, MongoDB)
2. **Use cloud storage** (AWS S3, Google Cloud Storage)
3. **Regular backups** to GitHub/Dropbox
4. **Upgrade to paid tier** (persistent disk)

---

## 🎓 Next Steps

1. ✅ Choose hosting platform (Render recommended)
2. ✅ Deploy application
3. ✅ Test thoroughly
4. ✅ Add authentication (see `webapp_secure.py`)
5. ✅ Create Squarespace landing page
6. ✅ Add link/embed to Squarespace
7. ✅ Share with users
8. ✅ Monitor usage
9. ✅ Collect feedback
10. ✅ Iterate and improve

---

## 📞 Support Resources

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **PythonAnywhere Docs:** https://help.pythonanywhere.com
- **Flask Deployment:** https://flask.palletsprojects.com/deployment/

---

## 🎯 Summary

**You cannot host Python Flask apps directly on Squarespace.**

**Best solution:**
1. Deploy Flask app to **Render.com** (free)
2. Add link on your Squarespace site
3. Or embed using iframe

**This gives you:**
- ✅ Free hosting
- ✅ Public URL
- ✅ Integration with Squarespace
- ✅ Professional appearance

**Your app will be accessible at:** `https://your-app-name.onrender.com`

Then link to it from your Squarespace site!

---

**Ready to deploy?** See the files I've created:
- `Procfile` - For deployment
- `runtime.txt` - Python version
- `webapp_secure.py` - Version with authentication
- `DEPLOYMENT.md` - Detailed deployment guide
