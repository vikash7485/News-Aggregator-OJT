# Deployment Guide - News Aggregator

## Best Deployment Options for Django

### 🥇 **Recommended: Render.com** (Free Tier Available)
- ✅ Free tier with PostgreSQL
- ✅ Easy Django deployment
- ✅ Automatic SSL
- ✅ Good for MongoDB connection
- ✅ Scheduled tasks support

### 🥈 **Alternative: Railway.app** (Easy Setup)
- ✅ Simple deployment
- ✅ Free tier available
- ✅ MongoDB support
- ✅ Auto-deploy from GitHub

### 🥉 **Alternative: Vercel** (Already Configured)
- ✅ Already has vercel.json
- ⚠️ Serverless (may need adjustments)
- ✅ Good for static sites

---

## Option 1: Deploy to Render.com (RECOMMENDED)

### Step 1: Prepare Your Code
1. **Push to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Connect your repository

### Step 3: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `news-aggregator` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main` (or `master`)
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     gunicorn news_aggregator.wsgi:application
     ```

### Step 4: Environment Variables
Add these in Render dashboard → Environment:

```env
SECRET_KEY=your-secret-key-here-generate-a-random-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
MONGODB_URL=mongodb+srv://vikash:vikash%40123@cluster0.cz6joof.mongodb.net/?appName=Cluster0
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Database Setup
1. In Render dashboard, go to your service
2. Open **Shell** (or use **Manual Deploy**)
3. Run migrations:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py fetch_feeds
   ```

### Step 6: Static Files
Render will handle static files automatically with the build command.

### ✅ Your app will be live at: `https://your-app-name.onrender.com`

---

## Option 2: Deploy to Railway.app

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository

### Step 3: Configure Environment Variables
In Railway dashboard → Variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app
MONGODB_URL=mongodb+srv://vikash:vikash%40123@cluster0.cz6joof.mongodb.net/?appName=Cluster0
```

### Step 4: Add Build/Start Commands
Railway will auto-detect Python, but you can add:

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start Command:**
```bash
gunicorn news_aggregator.wsgi:application --bind 0.0.0.0:$PORT
```

### Step 5: Run Migrations
1. Open **Railway Shell**
2. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py fetch_feeds
   ```

### ✅ Your app will be live at: `https://your-app-name.up.railway.app`

---

## Option 3: Deploy to Vercel (Already Configured)

### Step 1: Install Vercel CLI
```bash
npm i -g vercel
```

### Step 2: Deploy
```bash
cd /Users/pratyksh/Desktop/ojtproject2025-main
vercel
```

### Step 3: Configure Environment Variables
In Vercel dashboard → Settings → Environment Variables:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=.vercel.app
MONGODB_URL=mongodb+srv://vikash:vikash%40123@cluster0.cz6joof.mongodb.net/?appName=Cluster0
```

### Step 4: Update vercel.json (if needed)
Your `vercel.json` is already configured!

### ⚠️ Note: Vercel is serverless - you may need to adjust for Django
Consider using Render or Railway for better Django support.

---

## Pre-Deployment Checklist

### ✅ Before Deploying:

1. **Update settings.py for production:**
   - ✅ Already configured with `DEBUG=False` default
   - ✅ `ALLOWED_HOSTS` configured
   - ✅ Static files configured

2. **Environment Variables:**
   - ✅ SECRET_KEY (generate new one for production)
   - ✅ DEBUG=False
   - ✅ ALLOWED_HOSTS (your domain)
   - ✅ MONGODB_URL (already set)

3. **Database:**
   - ✅ Migrations ready
   - ✅ MongoDB connection configured

4. **Static Files:**
   - ✅ WhiteNoise configured
   - ✅ collectstatic command ready

5. **Dependencies:**
   - ✅ requirements.txt updated
   - ✅ All packages listed

---

## Post-Deployment Steps

### 1. Run Migrations
```bash
python manage.py migrate
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Fetch Initial News
```bash
python manage.py fetch_feeds
```

### 4. Sync to MongoDB (Optional)
```bash
python manage.py sync_to_mongodb
```

### 5. Set Up Scheduled Tasks (Optional)

**On Render:**
- Go to **Cron Jobs** → **New Cron Job**
- Command: `cd /opt/render/project/src && python manage.py fetch_feeds`
- Schedule: `0 */6 * * *` (every 6 hours)

**On Railway:**
- Use Railway's **Cron Jobs** feature
- Similar setup

---

## Quick Deploy Commands

### For Render:
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# 2. Go to Render.com and connect repo
# 3. Configure as above
```

### For Railway:
```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize
railway init

# 4. Deploy
railway up
```

---

## Troubleshooting

### Static Files Not Loading:
- Run: `python manage.py collectstatic --noinput`
- Check WhiteNoise configuration

### Database Errors:
- Run migrations: `python manage.py migrate`
- Check database connection

### MongoDB Connection:
- Verify `MONGODB_URL` in environment variables
- Check MongoDB Atlas IP whitelist (add 0.0.0.0/0 for Render/Railway)

### 500 Errors:
- Check logs in deployment platform
- Set `DEBUG=True` temporarily to see errors
- Check `ALLOWED_HOSTS` matches your domain

---

## Recommended: Render.com

**Why Render?**
- ✅ Free tier with PostgreSQL
- ✅ Easy Django deployment
- ✅ Automatic SSL certificates
- ✅ Scheduled tasks (cron jobs)
- ✅ Good documentation
- ✅ MongoDB connection works well

**Steps:**
1. Sign up at render.com
2. Connect GitHub repo
3. Create Web Service
4. Add environment variables
5. Deploy!

Your app will be live in ~5 minutes! 🚀

---

## Need Help?

Check the deployment platform's documentation:
- Render: https://render.com/docs
- Railway: https://docs.railway.app
- Vercel: https://vercel.com/docs

