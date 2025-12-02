# Render Deployment Guide for News Aggregator

This guide will walk you through deploying your Django News Aggregator project on Render step by step.

## Prerequisites

- A GitHub account with your project repository
- A Render account (sign up at https://render.com)
- MongoDB Atlas account (for database)

---

## Step 1: Prepare Your Repository

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Verify these files exist in your repository**:
   - `requirements.txt` ✓
   - `render.yaml` ✓
   - `app.py` ✓ (created for Render compatibility)
   - `manage.py` ✓
   - `news_aggregator/wsgi.py` ✓

---

## Step 2: Create a New Web Service on Render

1. **Log in to Render Dashboard**
   - Go to https://dashboard.render.com
   - Sign in or create an account

2. **Create New Web Service**
   - Click the **"New +"** button (top right)
   - Select **"Web Service"**

3. **Connect Your Repository**
   - Choose **"Connect account"** if not connected
   - Select your GitHub account
   - Authorize Render to access your repositories
   - Find and select your repository: `News-Aggregator-OJT` (or your repo name)
   - Click **"Connect"**

---

## Step 3: Configure Your Web Service

Fill in the following settings in the Render dashboard:

### Basic Settings

- **Name**: `news-aggregator-ojt` (or your preferred name)
- **Region**: Choose closest to your users (e.g., `Oregon (US West)`)
- **Branch**: `main` (or `master` if that's your default branch)
- **Root Directory**: Leave empty (or `./` if your project is in a subdirectory)

### Build & Deploy Settings

- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Start Command**: 
  ```
  gunicorn news_aggregator.wsgi:application --bind 0.0.0.0:$PORT
  ```
  **OR** (if Render dashboard uses default):
  ```
  gunicorn app:app --bind 0.0.0.0:$PORT
  ```

### Environment Variables

Click **"Add Environment Variable"** and add these one by one:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | Click "Generate" or use a strong random string | **Required** - Django secret key |
| `DEBUG` | `False` | Set to False for production |
| `ALLOWED_HOSTS` | `news-aggregator-ojt.onrender.com` | Replace with your actual Render URL |
| `MONGODB_URL` | `mongodb+srv://vikash:vikash%40123@cluster0.cz6joof.mongodb.net/?appName=Cluster0` | Your MongoDB connection string |
| `DATABASE_URL` | (Optional) If using PostgreSQL | Render provides this automatically if you add a PostgreSQL database |

### Advanced Settings (Optional)

- **Auto-Deploy**: `Yes` (deploys automatically on git push)
- **Health Check Path**: `/` (or leave empty)
- **Docker**: Leave unchecked (we're using Python runtime)

---

## Step 4: Add PostgreSQL Database (Optional but Recommended)

1. **Create PostgreSQL Database**:
   - In Render dashboard, click **"New +"**
   - Select **"PostgreSQL"**
   - Name: `news-aggregator-db`
   - Database: `news_aggregator`
   - User: (auto-generated)
   - Region: Same as your web service
   - Plan: `Free` (or upgrade for production)
   - Click **"Create Database"**

2. **Get Database URL**:
   - Once created, go to your database dashboard
   - Copy the **"Internal Database URL"** or **"External Database URL"**
   - Add it as `DATABASE_URL` environment variable in your web service

3. **Run Migrations**:
   - After first deployment, go to your web service
   - Open **"Shell"** tab
   - Run: `python manage.py migrate`

---

## Step 5: Deploy

1. **Review Settings**:
   - Double-check all environment variables
   - Verify build and start commands

2. **Create Web Service**:
   - Click **"Create Web Service"** button at the bottom
   - Render will start building your application

3. **Monitor Build**:
   - Watch the build logs in real-time
   - Wait for build to complete (usually 2-5 minutes)
   - Check for any errors

---

## Step 6: Post-Deployment Setup

### Run Database Migrations

1. **Via Render Shell**:
   - Go to your web service dashboard
   - Click **"Shell"** tab
   - Run: `python manage.py migrate`

2. **Create Superuser** (for admin access):
   - In Shell, run: `python manage.py createsuperuser`
   - Follow prompts to create admin account

### Verify Deployment

1. **Check Your URL**:
   - Your app will be available at: `https://news-aggregator-ojt.onrender.com`
   - (Replace with your actual service name)

2. **Test the Application**:
   - Visit your URL in browser
   - Check if homepage loads
   - Test login/registration
   - Verify news feeds are loading

---

## Step 7: Configure Scheduled Jobs (Optional)

If you want to automatically fetch news feeds:

1. **Create Background Worker**:
   - In Render dashboard, click **"New +"**
   - Select **"Background Worker"**
   - Connect same repository
   - **Start Command**: `python manage.py fetch_feeds`
   - Set same environment variables
   - Create the worker

2. **Or Use Cron Jobs**:
   - Render doesn't support cron directly
   - Consider using external services like:
     - Render Cron Jobs (paid plans)
     - GitHub Actions
     - External cron services

---

## Troubleshooting Common Issues

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution**: The `app.py` file has been created. Make sure:
- `app.py` is in your repository root
- Start command is: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Issue: Static files not loading

**Solution**: 
- Verify `collectstatic` runs in build command
- Check `STATIC_ROOT` in settings.py
- Ensure WhiteNoise is in `MIDDLEWARE`

### Issue: Database connection errors

**Solution**:
- Verify `DATABASE_URL` environment variable is set
- Check PostgreSQL database is running
- Ensure migrations are run: `python manage.py migrate`

### Issue: "DisallowedHost" error

**Solution**:
- Update `ALLOWED_HOSTS` environment variable
- Include your Render URL: `your-app-name.onrender.com`

### Issue: Build fails

**Solution**:
- Check build logs for specific errors
- Verify `requirements.txt` has all dependencies
- Ensure Python version is compatible (check `runtime.txt` if exists)

---

## Environment Variables Summary

Here's a complete list of environment variables you should set:

```bash
SECRET_KEY=<generated-secret-key>
DEBUG=False
ALLOWED_HOSTS=news-aggregator-ojt.onrender.com
MONGODB_URL=mongodb+srv://vikash:vikash%40123@cluster0.cz6joof.mongodb.net/?appName=Cluster0
DATABASE_URL=<postgresql-connection-string>  # Optional, if using PostgreSQL
```

---

## Render Dashboard Settings Summary

### Build Settings
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command**: `gunicorn news_aggregator.wsgi:application --bind 0.0.0.0:$PORT`

### Environment Variables
- `SECRET_KEY` - Generate or provide
- `DEBUG` - `False`
- `ALLOWED_HOSTS` - Your Render URL
- `MONGODB_URL` - Your MongoDB connection string
- `DATABASE_URL` - (Optional) PostgreSQL connection string

### Advanced
- **Auto-Deploy**: Enabled
- **Health Check**: `/` (optional)

---

## Important Notes

1. **Free Tier Limitations**:
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes ~50 seconds
   - Consider upgrading for production use

2. **Static Files**:
   - WhiteNoise is configured for serving static files
   - Static files are collected during build

3. **Database**:
   - SQLite won't work on Render (ephemeral filesystem)
   - Use PostgreSQL (recommended) or MongoDB

4. **Secrets**:
   - Never commit secrets to Git
   - Always use environment variables
   - Use Render's "Generate" for SECRET_KEY

---

## Quick Reference Commands

### Render Shell Commands
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (usually done in build)
python manage.py collectstatic --noinput

# Fetch news feeds manually
python manage.py fetch_feeds
```

---

## Support

If you encounter issues:
1. Check Render deployment logs
2. Review Django error logs in Render dashboard
3. Verify all environment variables are set correctly
4. Check Render documentation: https://render.com/docs

---

## Success Checklist

- [ ] Repository connected to Render
- [ ] Web service created with correct settings
- [ ] All environment variables configured
- [ ] Build completes successfully
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Application accessible via URL
- [ ] Static files loading correctly
- [ ] News feeds fetching properly

---

**Last Updated**: Based on current project configuration
**Project**: News Aggregator Django Application

