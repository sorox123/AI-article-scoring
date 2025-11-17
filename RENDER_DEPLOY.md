# Deploy to Render.com - Quick Guide

## Step 1: Sign Up
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email

## Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub account if not already connected
3. Select repository: `sorox123/AI-article-scoring`
4. Click "Connect"

## Step 3: Configure Service
Fill in these settings:

**Basic Settings:**
- **Name**: `ai-article-scoring` (or any name you prefer)
- **Region**: Choose closest to you (e.g., Oregon, Ohio, Frankfurt)
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements_deploy.txt`
- **Start Command**: `gunicorn webapp_secure:app`

**Instance Type:**
- Select "Free" (0.1 CPU, 512 MB RAM)

## Step 4: Set Environment Variables
Click "Add Environment Variable" and add these:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ADMIN_PASSWORD` | Your chosen password (e.g., `mySecurePass2025`) |
| `FLASK_ENV` | `production` |
| `PORT` | `10000` (Render sets this automatically) |

**To generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and paste as SECRET_KEY value.

## Step 5: Deploy
1. Click "Create Web Service"
2. Wait 3-5 minutes for deployment
3. Watch the logs for any errors

## Step 6: Access Your App
Once deployed, you'll get a URL like:
```
https://ai-article-scoring.onrender.com
```

Open it in your browser and log in with your ADMIN_PASSWORD!

## Troubleshooting

### Build Failed
- Check that `requirements_deploy.txt` exists
- Verify Python version in `runtime.txt` is `python-3.12.0`

### App Won't Start
- Verify Start Command is exactly: `gunicorn webapp_secure:app`
- Check environment variables are set correctly

### Login Not Working
- Make sure ADMIN_PASSWORD environment variable is set
- Try clearing browser cookies

### App Sleeps After Inactivity
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Upgrade to paid tier ($7/month) for always-on service

## What's Included
✅ Password protection
✅ Article import (CSV, Excel, TXT)
✅ Persistent article database
✅ Duplicate removal
✅ Scoring system
✅ Export as TXT reports, JSON, or plain URL list
✅ Mobile responsive design

## Updating Your App
1. Make changes locally
2. Commit: `git add -A && git commit -m "Update message"`
3. Push: `git push origin main`
4. Render auto-deploys in ~2 minutes

## Cost
- **Free tier**: Perfect for testing and personal use
- **Starter**: $7/month for always-on service
- No credit card required for free tier
