# News Aggregator

A Django-based news aggregator that fetches articles from RSS feeds and NewsAPI, with global search capabilities, user authentication, and bookmark features.

## Features

- **Multi-source Aggregation**: Fetches news from RSS feeds (BBC, TechCrunch, CNN, Guardian, ESPN) and NewsAPI
- **Global Search**: Search for any keyword, topic, or country (e.g., "india", "bitcoin", "korea technology")
- **Categorization**: Automatically categorizes news into Technology, Sports, Business, Health, World, etc.
- **User Accounts**: Register, Login, Logout functionality
- **Save for Later**: Bookmark articles to read later
- **Responsive UI**: Built with Bootstrap 5
- **Deduplication**: Prevents storing duplicate articles by URL
- **Error Handling**: Graceful handling of API rate limits and feed failures

## Tech Stack

- **Backend**: Django 4.2+, Python 3.8+
- **APIs**: NewsAPI, RSS Feeds (feedparser)
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)

## Setup Instructions

### 1. Clone the Repository

```bash
cd news_aggregator
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the project root:

```env
NEWSAPI_KEY=72b988930c994d329db4fe8743f7e901
DEBUG=True
SECRET_KEY=your-secret-key-here
```

**Note**: Replace `your-secret-key-here` with a secure random string for production.

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Fetch Initial News

```bash
python manage.py fetch_feeds
```

This command fetches news from RSS feeds. Run this periodically (e.g., via cron job or task scheduler).

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage

### Searching for News

1. Use the search bar in the navbar
2. Type any keyword, country, or topic (e.g., "india cricket", "bitcoin", "usa politics")
3. The app will fetch live results from NewsAPI and save them to the database
4. You can then bookmark any article for later reading

### Managing Saved Articles

1. Login to your account
2. Click "Save" button on any article
3. Access your saved articles from "Saved Articles" in the navbar
4. Click "Unsave" to remove articles from your saved list

### Category Filtering

- Use the category buttons on the homepage to filter by Technology, Sports, World, etc.

## Project Structure

```
news_aggregator/
├── news/                          # Main app
│   ├── management/
│   │   └── commands/
│   │       ├── fetch_feeds.py     # RSS feed ingestion command
│   │       └── fetch_news.py      # Old NewsAPI command (deprecated)
│   ├── migrations/
│   ├── models.py                  # News, Category, SavedArticle models
│   ├── views.py                   # Home, search, auth, save views
│   ├── urls.py                    # URL routing
│   ├── forms.py                   # Search form
│   ├── admin.py                   # Admin interface
│   └── tests.py                   # Unit tests
├── templates/
│   ├── base.html                  # Base template with navbar
│   ├── news/
│   │   ├── home.html              # Homepage with search results
│   │   └── saved.html             # Saved articles page
│   └── registration/
│       ├── login.html             # Login page
│       └── register.html          # Registration page
├── static/
│   └── css/
│       └── style.css              # Custom styles
├── news_aggregator/
│   ├── settings.py                # Django settings (uses .env)
│   ├── urls.py                    # Main URL configuration
│   └── wsgi.py                    # WSGI config
├── .env                           # Environment variables (NOT in git)
├── .gitignore                     # Git ignore file
├── requirements.txt               # Python dependencies
├── manage.py                      # Django management script
└── README.md                      # This file
```

## RSS Feed Sources

- BBC News: http://feeds.bbci.co.uk/news/rss.xml
- TechCrunch: https://techcrunch.com/feed/
- CNN: http://rss.cnn.com/rss/edition.rss
- The Guardian: https://www.theguardian.com/world/rss
- ESPN: https://www.espn.com/espn/rss/news

## Testing

Run tests:

```bash
python manage.py test
```

## Deployment

### Production Checklist

1. Set `DEBUG=False` in `.env`
2. Use a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` in `settings.py`
4. Use PostgreSQL instead of SQLite:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'newsdb',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
5. Collect static files: `python manage.py collectstatic`
6. Set up a task scheduler (cron/celery) to run `fetch_feeds` periodically
7. Use a production server (Gunicorn, uWSGI)

### Scheduled News Fetching

**On Linux/Mac (crontab)**:
```bash
# Fetch news every 6 hours
0 */6 * * * cd /path/to/news_aggregator && /path/to/venv/bin/python manage.py fetch_feeds
```

**On Windows (Task Scheduler)**:
- Create a task to run `python manage.py fetch_feeds` every 6 hours

## API Key Management

- Keep your `.env` file secure and never commit it to version control
- For production, use environment variables on your hosting platform
- NewsAPI free tier has rate limits; monitor usage

## Troubleshooting

### No articles showing up
- Run `python manage.py fetch_feeds` to populate the database
- Check if `.env` file exists with proper `NEWSAPI_KEY`

### Search not working
- Verify `NEWSAPI_KEY` is set correctly in `.env`
- Check API rate limits (100 requests/day on free tier)

### Database errors
- Run `python manage.py migrate` to apply migrations
- Delete `db.sqlite3` and run migrations again if corrupted

## License

MIT License

## Support

For issues and questions, please check the code comments or create an issue in the repository.
