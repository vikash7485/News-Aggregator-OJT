# 🚀 Quick Deployment Guide

## ⚡ Fastest Way: Render.com (5 minutes)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Ready for deployment"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to **https://render.com** → Sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `news-aggregator`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn news_aggregator.wsgi:application`

### Step 3: Add Environment Variables
In Render dashboard → Environment:

```env
SECRET_KEY=generate-this-with-command-below
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
MONGODB_URL=mongodb+srv://vikash:vikash%40123@cluster0.cz6joof.mongodb.net/?appName=Cluster0
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Deploy & Run Setup
1. Click **"Create Web Service"**
2. Wait for deployment (~3-5 minutes)
3. Open **Shell** in Render dashboard
4. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py fetch_feeds
   ```

### ✅ Done! Your app is live at: `https://your-app-name.onrender.com`

---

## 🎯 Alternative: Railway.app (Even Easier)

1. Go to **https://railway.app** → Sign up
2. **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repo
4. Add environment variables (same as above)
5. Railway auto-detects Python and deploys!

---

## 📋 Pre-Deployment Checklist

- ✅ `gunicorn` in requirements.txt
- ✅ `whitenoise` configured
- ✅ `Procfile` created
- ✅ `render.yaml` created (optional)
- ✅ Environment variables ready
- ✅ MongoDB URL configured

---

## 🔧 Post-Deployment

After deployment, run these in the platform's shell:

```bash
# 1. Run migrations
python manage.py migrate

# 2. Create admin user
python manage.py createsuperuser

# 3. Fetch initial news
python manage.py fetch_feeds

# 4. (Optional) Sync to MongoDB
python manage.py sync_to_mongodb
```

---

## 📚 Full Guide

See `DEPLOYMENT_GUIDE.md` for detailed instructions for all platforms.

