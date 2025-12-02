import feedparser
import requests
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from datetime import datetime
from time import mktime
from news.models import News, Category

class Command(BaseCommand):
    help = 'Fetches news from RSS feeds and NewsAPI'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting news fetch...")
        
        # 1. RSS Feeds
        rss_feeds = [
            ('http://feeds.bbci.co.uk/news/rss.xml', 'BBC', 'World'),
            ('https://techcrunch.com/feed/', 'TechCrunch', 'Technology'),
            ('http://rss.cnn.com/rss/edition.rss', 'CNN', 'World'),
            ('https://www.theguardian.com/world/rss', 'The Guardian', 'World'),
            ('https://www.espn.com/espn/rss/news', 'ESPN', 'Sports'),
        ]

        for url, source, category_name in rss_feeds:
            self.stdout.write(f"Fetching RSS: {source}")
            feed = feedparser.parse(url)
            category, _ = Category.objects.get_or_create(name=category_name)

            for entry in feed.entries[:10]: # Limit to 10 per feed
                if News.objects.filter(link=entry.link).exists():
                    continue
                
                # Date parsing
                pub_date = None
                if hasattr(entry, 'published_parsed'):
                    dt = datetime.fromtimestamp(mktime(entry.published_parsed))
                    pub_date = make_aware(dt)
                
                News.objects.create(
                    title=entry.title,
                    link=entry.link,
                    description=entry.get('summary', '')[:500], # Truncate description
                    pub_date=pub_date,
                    source=source,
                    category=category,
                    guid=entry.get('id', entry.link)
                )

        # 2. NewsAPI
        api_key = '72b988930c994d329db4fe8743f7e901'
        countries = ['us', 'in', 'gb']
        
        for country in countries:
            self.stdout.write(f"Fetching NewsAPI for country: {country.upper()}...")
            newsapi_url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}'
            
            response = requests.get(newsapi_url)
            if response.status_code == 200:
                data = response.json()
                for article in data.get('articles', []):
                    if News.objects.filter(link=article['url']).exists():
                        continue

                    # Map NewsAPI categories if possible, else default to 'General'
                    cat_name = 'General'
                    
                    # Simple keyword matching for category
                    title_lower = (article['title'] or '').lower()
                    if 'tech' in title_lower: cat_name = 'Technology'
                    elif 'sport' in title_lower: cat_name = 'Sports'
                    elif 'business' in title_lower: cat_name = 'Business'
                    elif 'health' in title_lower: cat_name = 'Health'
                    
                    category, _ = Category.objects.get_or_create(name=cat_name)

                    # Date parsing for ISO format
                    pub_date = None
                    if article.get('publishedAt'):
                        pub_date = parse_datetime(article['publishedAt'])

                    News.objects.create(
                        title=article['title'],
                        link=article['url'],
                        image=article['urlToImage'],
                        description=article.get('description', '') or '',
                        pub_date=pub_date,
                        source=f"{article['source']['name']} ({country.upper()})",
                        category=category
                    )

        self.stdout.write(self.style.SUCCESS('Successfully fetched news'))
