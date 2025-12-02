#!/bin/bash
# Startup script for Render deployment
# Runs migrations, starts server, and fetches news in background if needed

echo "Running migrations..."
python manage.py migrate --noinput

# Start gunicorn in background
echo "Starting Gunicorn server..."
gunicorn news_aggregator.wsgi:application --bind 0.0.0.0:$PORT &
GUNICORN_PID=$!

# Wait for server to be ready
sleep 3

# Check if we need to fetch articles
echo "Checking article count..."
ARTICLE_COUNT=$(python manage.py shell -c "from news.models import News; print(News.objects.count())" 2>/dev/null | tail -1 || echo "0")

if [ "$ARTICLE_COUNT" = "0" ]; then
    echo "No articles found. Fetching news in background..."
    python manage.py fetch_feeds > /tmp/fetch_feeds.log 2>&1 &
    echo "Fetch started in background. Articles will appear in 1-2 minutes."
else
    echo "Found $ARTICLE_COUNT articles. Server ready."
fi

# Wait for gunicorn (main process)
wait $GUNICORN_PID

