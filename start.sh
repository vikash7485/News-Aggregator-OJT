#!/bin/bash
# Startup script for Render deployment
# Runs migrations, starts server, and fetches news in background if needed

echo "Running migrations..."
python manage.py migrate --noinput

# Check if we need to fetch articles (before starting server)
echo "Checking article count..."
ARTICLE_COUNT=$(python manage.py shell -c "from news.models import News; print(News.objects.count())" 2>/dev/null | tail -1 || echo "0")

if [ "$ARTICLE_COUNT" = "0" ]; then
    echo "No articles found. Will fetch in background after server starts..."
    # Start fetch in background (wait longer for server to fully start)
    (sleep 10 && python manage.py fetch_feeds >> /tmp/fetch_feeds.log 2>&1 && echo "Fetch completed at $(date)" >> /tmp/fetch_feeds.log) &
    FETCH_PID=$!
    echo "Background fetch scheduled (PID: $FETCH_PID). Check /tmp/fetch_feeds.log for progress."
else
    echo "Found $ARTICLE_COUNT articles. Checking if we need to update..."
    # Even if articles exist, fetch new ones periodically (but don't block)
    (sleep 30 && python manage.py fetch_feeds >> /tmp/fetch_feeds.log 2>&1) &
fi

# Start gunicorn as main process (Render needs this to be the main process)
echo "Starting Gunicorn server..."
exec gunicorn news_aggregator.wsgi:application --bind 0.0.0.0:$PORT

