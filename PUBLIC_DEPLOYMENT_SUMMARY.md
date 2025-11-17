# 🌍 Making Your App Public - Summary

## ⚠️ Important: Squarespace Cannot Host Python Apps

**Squarespace does not support Flask/Python applications.** You need to:
1. Host the Flask app elsewhere (Render, Railway, etc.)
2. Link to it from your Squarespace site

---

## ✅ What I've Created for You

### 🔒 Secure Version with Authentication
- **`webapp_secure.py`** - Password-protected Flask app
- **`templates/login.html`** - Login page
- Default password: `scoring2025` (change this!)

### 📦 Deployment Files
- **`Procfile`** - Tells hosting platform how to run your app
- **`runtime.txt`** - Specifies Python version (3.12)
- **`requirements_deploy.txt`** - Dependencies including gunicorn
- **`.gitignore`** - Prevents sensitive files from being uploaded

### 📖 Complete Documentation
- **`DEPLOYMENT.md`** - Step-by-step deployment guide
- **`SQUARESPACE_HOSTING.md`** - How to integrate with Squarespace
- **`README.md`** - GitHub repository README

---

## 🚀 Quick Deploy Steps

### 1. Push to GitHub (5 minutes)

```powershell
cd c:\Users\sorox\ai-news-scraper

# Initialize git
git init
git add .
git commit -m "Initial commit: AI Article Scoring App"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/ai-article-scoring.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Render.com (10 minutes - FREE)

1. Go to https://render.com and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements_deploy.txt`
   - **Start Command:** `gunicorn webapp_secure:app`
   - **Plan:** Free
5. Add Environment Variables:
   ```
   SECRET_KEY=<generate random string>
   ADMIN_PASSWORD=<your secure password>
   FLASK_ENV=production
   ```
6. Click **"Create Web Service"**

**Your public URL:** `https://your-app-name.onrender.com`

### 3. Link from Squarespace (2 minutes)

**Option A: Navigation Link**
- Squarespace → Design → Navigation
- Add external link: `https://your-app-name.onrender.com`
- Label: "Article Scoring Tool"

**Option B: Button on Page**
- Add Button block
- Text: "Access Scoring Tool"
- URL: `https://your-app-name.onrender.com`
- Style: Primary, Open in new window

**Option C: Iframe Embed**
```html
<iframe 
  src="https://your-app-name.onrender.com" 
  width="100%" 
  height="800px" 
  style="border: 2px solid #e2e8f0; border-radius: 12px;">
</iframe>
```

---

## 🔒 Security Setup

### Change Default Password

**Method 1: Environment Variable (Best)**
On Render.com dashboard:
```
ADMIN_PASSWORD=your-secure-password-here
```

**Method 2: Edit Code**
In `webapp_secure.py`, line 21:
```python
DEFAULT_PASSWORD_HASH = generate_password_hash('your-new-password')
```

### Generate Secure Values

```powershell
# Secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Secure password
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

---

## 💰 Hosting Costs

| Platform | Free Tier | Paid | Best For |
|----------|-----------|------|----------|
| **Render** | ✅ Yes | $7/mo | Recommended |
| **Railway** | ❌ No | $5/mo | Simple |
| **PythonAnywhere** | ✅ Yes | $5/mo | Python focus |
| **Heroku** | ❌ No | $7/mo | Popular |

**Recommendation:** Start with **Render.com free tier**

Free tier limitations:
- Sleeps after 15 minutes of inactivity
- 750 hours/month
- Shared resources

---

## 🌐 Access URLs

After deployment, you'll have:

**Primary URL (Render):**
- `https://your-app-name.onrender.com`

**Custom Domain (Optional):**
- `https://scoring.yourdomain.com`

**Squarespace Integration:**
- Link from navigation
- Button on page
- Iframe embed

---

## 📋 Pre-Launch Checklist

Before sharing your app:

- [ ] Changed default password
- [ ] Set SECRET_KEY environment variable
- [ ] Tested login functionality
- [ ] Tested file import (CSV, Excel, TXT)
- [ ] Tested scoring workflow
- [ ] Tested export (TXT and JSON)
- [ ] Added link to Squarespace site
- [ ] Tested on mobile device
- [ ] Shared password with team
- [ ] Created backup plan for data

---

## 🎯 What Users Will See

1. **Visit your URL** → Login page with password field
2. **Enter password** → Main dashboard
3. **Import articles** → Upload CSV/Excel/TXT
4. **Score articles** → Interactive sliders (1-10)
5. **View peer scores** → See all ratings and stats
6. **Export results** → Download as TXT or JSON

---

## 🔄 Updating Your App

```powershell
# Make changes to code
git add .
git commit -m "Update: description of changes"
git push

# Render automatically redeploys (2-5 minutes)
```

---

## 🐛 Common Issues & Solutions

### "Application Error" after deployment
- Check environment variables are set
- Verify Start Command: `gunicorn webapp_secure:app`
- Check logs on Render dashboard

### Can't login
- Verify ADMIN_PASSWORD is set correctly
- Try default password: `scoring2025`
- Check browser cookies are enabled

### Iframe not working on Squarespace
- Some platforms block iframe embedding
- Use direct link instead
- Or add X-Frame-Options header

### Data lost after app restarts
- Free tiers have ephemeral storage
- Upgrade to paid tier for persistent disk
- Or export data regularly as backup

---

## 📊 Monitoring

### Check App Status
- Render Dashboard: View uptime, logs, metrics
- Test URL periodically
- Set up uptime monitoring (UptimeRobot)

### Backup Data
```powershell
# Export all scores as JSON
# Click "Export Results" → JSON format
# Save file locally or to cloud storage
```

---

## 🎓 Next Steps

### Immediate (Today)
1. ✅ Push code to GitHub
2. ✅ Deploy to Render.com
3. ✅ Change default password
4. ✅ Test the live app
5. ✅ Add link to Squarespace

### Short Term (This Week)
6. ✅ Share URL with team
7. ✅ Import real article data
8. ✅ Set up custom domain (optional)
9. ✅ Create backup schedule
10. ✅ Monitor usage and errors

### Long Term (This Month)
11. ⬜ Consider paid tier if needed
12. ⬜ Add advanced features
13. ⬜ Integrate analytics
14. ⬜ Collect user feedback
15. ⬜ Optimize performance

---

## 📞 Support Resources

- **Render Docs:** https://render.com/docs
- **Flask Deployment:** https://flask.palletsprojects.com/deploying/
- **Your Docs:**
  - `DEPLOYMENT.md` - Detailed deployment guide
  - `SQUARESPACE_HOSTING.md` - Squarespace integration
  - `WEBAPP_README.md` - Full app documentation

---

## ✨ Summary

**You now have:**
1. ✅ Secure web app with password protection
2. ✅ Ready-to-deploy files and configuration
3. ✅ Complete documentation
4. ✅ Multiple hosting options (free and paid)
5. ✅ Squarespace integration methods

**To go live:**
1. Push to GitHub (5 min)
2. Deploy to Render (10 min)
3. Link from Squarespace (2 min)

**Total time: ~20 minutes**

**Your app will be:**
- 🌍 Publicly accessible at custom URL
- 🔒 Password protected
- 📱 Mobile responsive
- 💾 Persistent data storage
- 🔗 Integrated with Squarespace

---

## 🎉 Ready to Launch!

Follow the steps in **`DEPLOYMENT.md`** to go live!

**Questions?** Check the documentation files or hosting platform support.

**Good luck with your deployment!** 🚀
