# 🚀 Deploy in 15 Minutes - Command Cheatsheet

## Step 1: Prepare Code (2 minutes)

```powershell
# Navigate to your project
cd c:\Users\sorox\ai-news-scraper

# Initialize Git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Article Scoring App"
```

---

## Step 2: Create GitHub Repository (3 minutes)

1. **Go to:** https://github.com/new
2. **Repository name:** `ai-article-scoring`
3. **Description:** "AI Article Credibility Scoring Web App"
4. **Visibility:** Public or Private
5. Click **"Create repository"**

6. **Push your code:**
```powershell
git remote add origin https://github.com/YOUR_USERNAME/ai-article-scoring.git
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy to Render.com (10 minutes)

### 3a. Sign Up
1. Go to: https://render.com
2. Click **"Get Started"**
3. Sign up with GitHub

### 3b. Create Web Service
1. Click **"New +"** button
2. Select **"Web Service"**
3. Connect your repository: `ai-article-scoring`
4. Click **"Connect"**

### 3c. Configure Service

Fill in these fields:

```
Name: ai-article-scoring
Region: Oregon (US West) [or closest to you]
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements_deploy.txt
Start Command: gunicorn webapp_secure:app
Instance Type: Free
```

### 3d. Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these THREE variables:

**Variable 1:**
```
Key: SECRET_KEY
Value: [Generate below]
```

**Variable 2:**
```
Key: ADMIN_PASSWORD
Value: your-secure-password-here
```

**Variable 3:**
```
Key: FLASK_ENV
Value: production
```

**Generate SECRET_KEY:**
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and paste as SECRET_KEY value.

### 3e. Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes (watch build logs)
3. When complete, you'll see: **"Your service is live at https://..."**

---

## Step 4: Test Your App (2 minutes)

1. Click the URL Render provides (e.g., `https://ai-article-scoring.onrender.com`)
2. You should see the login page
3. Enter your `ADMIN_PASSWORD`
4. Test importing a file
5. Test scoring an article

✅ **Your app is now PUBLIC!**

---

## Step 5: Add to Squarespace (3 minutes)

### Option A: Navigation Link

1. **In Squarespace:**
   - Go to **Design** → **Navigation**
   - Click **"+"** to add link
   - Label: `Article Scoring`
   - URL: `https://your-app.onrender.com` (your Render URL)
   - Save

### Option B: Button on Page

1. **Edit any Squarespace page**
2. Add **Button** block
3. Settings:
   - Button Text: `Access Scoring Tool`
   - URL: `https://your-app.onrender.com`
   - Style: Primary
   - Open in: New window
4. Save and publish

### Option C: Embed with Iframe

1. **Edit Squarespace page**
2. Add **Code** block
3. Paste this (replace URL):

```html
<div style="width: 100%; height: 800px;">
  <iframe 
    src="https://your-app.onrender.com" 
    width="100%" 
    height="100%" 
    frameborder="0"
    style="border: 2px solid #e2e8f0; border-radius: 12px;">
  </iframe>
</div>
```

4. Save and publish

---

## 🎉 You're Done!

**Your app is now:**
- ✅ Publicly accessible at: `https://your-app.onrender.com`
- ✅ Password protected with your custom password
- ✅ Linked from your Squarespace website
- ✅ Free hosting (with Render free tier)

---

## 🔑 Important Information

### Save These Details:

```
App URL: https://your-app-name.onrender.com
Password: [your ADMIN_PASSWORD]
GitHub Repo: https://github.com/YOUR_USERNAME/ai-article-scoring
Render Dashboard: https://dashboard.render.com
```

---

## 🔄 How to Update Later

```powershell
# Make changes to your code locally
# Then push to GitHub:

git add .
git commit -m "Update: describe your changes"
git push

# Render automatically redeploys in 2-5 minutes
```

---

## 🐛 Troubleshooting Quick Fixes

### "Build failed"
```powershell
# Check these files exist:
dir requirements_deploy.txt
dir Procfile
dir runtime.txt
dir webapp_secure.py
```

### "Application Error"
- Check environment variables are set on Render
- Verify Start Command: `gunicorn webapp_secure:app`
- Check logs in Render dashboard

### Can't login
- Try password you set in `ADMIN_PASSWORD`
- If forgot, edit on Render → Settings → Environment

### App is slow
- Free tier sleeps after 15 min inactivity
- First request after sleep takes 30-60 seconds
- Upgrade to paid tier ($7/mo) for instant response

---

## 💰 Upgrade to Paid Tier (Optional)

**When:** App is slow or sleeps too often

**How:**
1. Render Dashboard → Your Service
2. Settings → Instance Type
3. Select: **Starter ($7/month)**
4. Benefits:
   - No sleeping
   - Faster response
   - Persistent storage
   - More resources

---

## 📱 Share Your App

Send this to users:

```
🎯 AI Article Scoring Tool

URL: https://your-app-name.onrender.com
Password: [your password]

Instructions:
1. Visit the URL
2. Enter the password
3. Click "Import Articles" to upload your file
4. Score articles by adjusting the 5 sliders
5. Export results when done

Supported formats: CSV, Excel (.xlsx), Text (.txt)
```

---

## 📊 Monitor Usage

**Render Dashboard:**
- View logs: See all activity
- Metrics: CPU and memory usage
- Events: Deployment history

**Access:**
https://dashboard.render.com/web/[your-service-id]

---

## 🔒 Security Best Practices

✅ **Changed default password**
✅ **Set strong SECRET_KEY**
✅ **Don't share password publicly**
✅ **Use HTTPS (automatic on Render)**
✅ **Regular data backups**

---

## 📋 Complete Command Reference

### Local Development
```powershell
python webapp_secure.py
# Access: http://localhost:5000
```

### Git Commands
```powershell
git status                    # Check changes
git add .                     # Stage all changes
git commit -m "message"       # Commit
git push                      # Deploy to Render
```

### Generate Passwords
```powershell
# Secret key (64 chars)
python -c "import secrets; print(secrets.token_hex(32))"

# Random password (22 chars)
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

### Test Locally with Authentication
```powershell
$env:ADMIN_PASSWORD="test123"
$env:SECRET_KEY="test-secret-key"
python webapp_secure.py
```

---

## 🎓 Next Steps After Deployment

1. ✅ Share URL and password with team
2. ✅ Import your first batch of articles
3. ✅ Test scoring workflow
4. ✅ Export and review results
5. ✅ Set up regular data backups
6. ✅ Monitor app performance
7. ✅ Collect user feedback
8. ✅ Consider custom domain (optional)

---

## 📞 Get Help

**Documentation:**
- `DEPLOYMENT.md` - Detailed guide
- `SQUARESPACE_HOSTING.md` - Integration guide
- `WEBAPP_README.md` - Feature documentation

**Platform Support:**
- Render: https://render.com/docs
- GitHub: https://docs.github.com
- Flask: https://flask.palletsprojects.com

**Check Logs:**
- Render Dashboard → Logs tab
- Look for error messages
- Google specific errors

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] Environment variables set
- [ ] App deployed successfully
- [ ] Login page accessible
- [ ] Password changed from default
- [ ] Can login successfully
- [ ] Import file works
- [ ] Scoring works
- [ ] Export works
- [ ] Link added to Squarespace
- [ ] Mobile tested
- [ ] Team notified
- [ ] Data backup plan created

---

## 🎉 Congratulations!

Your AI Article Scoring app is now:
- 🌍 **Live and public**
- 🔒 **Secure with password**
- 💻 **Accessible from anywhere**
- 📱 **Works on all devices**
- 🔗 **Integrated with Squarespace**

**Time to deployment: 15 minutes** ⚡

**Share your app with the world!** 🚀
