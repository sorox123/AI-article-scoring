# PostgreSQL Database Setup on Render

Your app now uses a **database** instead of JSON files. This means:
✅ Data persists across restarts
✅ Multiple users see the same articles and scores
✅ True collaborative scoring

## Step 1: Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +" → "PostgreSQL"**
3. Configure:
   - **Name**: `ai-article-scoring-db` (or any name)
   - **Database**: `article_scoring` (default is fine)
   - **User**: (auto-generated)
   - **Region**: Same as your web service (e.g., Oregon)
   - **Plan**: **Free** (1GB storage, expires after 90 days)
4. Click **"Create Database"**
5. Wait 1-2 minutes for creation

## Step 2: Get Database Connection String

1. Once created, click on your database
2. Scroll down to **"Connections"**
3. Copy the **"Internal Database URL"** (looks like: `postgres://user:pass@host/dbname`)
4. **Important**: You'll use the INTERNAL URL (faster, free bandwidth)

## Step 3: Connect Database to Web Service

1. Go to your web service dashboard
2. Click **"Environment"** in the left sidebar
3. Add new environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL you copied
4. Click **"Save Changes"**

## Step 4: Deploy

Render will automatically redeploy your app with the database connected!

### What Happens:
- App detects `DATABASE_URL` environment variable
- Connects to PostgreSQL instead of SQLite
- Creates tables automatically on first run
- All data is now persistent!

## Verification

1. Wait for deployment to complete (~2-3 minutes)
2. Open your app URL
3. Import some articles and add scores
4. **Restart your web service** (Settings → Manual Deploy → "Clear build cache & deploy")
5. Check that your data is still there! 🎉

## Local vs Production

**Local development** (your computer):
- Uses SQLite database (`article_scores.db` file)
- Fast and easy for testing

**Production** (Render.com):
- Uses PostgreSQL database
- Shared across all users
- Persists through restarts

## Free Tier Limitations

- **Storage**: 1 GB (plenty for thousands of articles)
- **Duration**: 90 days, then you need to create a new database
- **Connections**: 97 max concurrent connections
- **Backup**: Manual export only

To keep data beyond 90 days, export before expiration and re-import to a new database.

## Troubleshooting

### "No DATABASE_URL found"
- Make sure you added the environment variable
- Check spelling: `DATABASE_URL` (case sensitive)
- Use **Internal** URL, not External

### "Could not connect to database"
- Verify database is in same region as web service
- Check database is running (not suspended)
- Try redeploying the web service

### "Tables not found"
- Tables are created automatically on first run
- Check logs for any errors during startup
- Redeploy if needed

## Data Migration (Optional)

If you have existing JSON data locally and want to import it:

```python
# Run this script locally to migrate data
python migrate_json_to_db.py
```

(Script not included - let me know if you need it!)

## Costs

**Current setup: 100% FREE** ✅
- Free PostgreSQL (90 days)
- Free web service (with sleep after inactivity)

**Upgrade options:**
- **Starter DB**: $7/month (persistent, no expiration, automated backups)
- **Starter Web**: $7/month (always-on, no sleep)

Total for always-on + persistent: **$14/month**
