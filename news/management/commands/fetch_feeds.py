import feedparser
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import datetime
from time import mktime, sleep
from news.models import News, Category
from django.db import transaction
import re

class Command(BaseCommand):
    help = 'Fetches news from RSS feeds'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting RSS fetch...")
        
        # Track success by category
        category_counts = {}
        
        rss_feeds = [
            # World News Sources (multiple to get 50+ articles)
            ('http://feeds.bbci.co.uk/news/rss.xml', 'BBC', 'World'),
            ('http://rss.cnn.com/rss/edition.rss', 'CNN', 'World'),
            ('https://www.theguardian.com/world/rss', 'The Guardian', 'World'),
            ('https://feeds.reuters.com/reuters/worldNews', 'Reuters', 'World'),
            ('https://rss.cbc.ca/lineup/topstories.xml', 'CBC', 'World'),
            ('https://feeds.npr.org/1001/rss.xml', 'NPR', 'World'),
            
            # Technology Sources (multiple to get 50+ articles)
            ('https://techcrunch.com/feed/', 'TechCrunch', 'Technology'),
            ('https://feeds.feedburner.com/oreilly/radar', 'O\'Reilly', 'Technology'),
            ('https://www.wired.com/feed/rss', 'Wired', 'Technology'),
            ('https://feeds.arstechnica.com/arstechnica/index', 'Ars Technica', 'Technology'),
            ('https://www.theverge.com/rss/index.xml', 'The Verge', 'Technology'),
            ('https://feeds.feedburner.com/venturebeat/SZYF', 'VentureBeat', 'Technology'),
            
            # Sports Sources (multiple to get 50+ articles)
            ('https://www.espn.com/espn/rss/news', 'ESPN', 'Sports'),
            ('https://feeds.feedburner.com/sportsillustrated', 'Sports Illustrated', 'Sports'),
            ('https://www.skysports.com/rss/12040', 'Sky Sports', 'Sports'),
            ('https://feeds.bbci.co.uk/sport/rss.xml', 'BBC Sport', 'Sports'),
            ('https://www.theguardian.com/sport/rss', 'The Guardian Sport', 'Sports'),
        ]

        for url, source, category_name in rss_feeds:
            try:
                self.stdout.write(f"Fetching RSS: {source}")
                feed = feedparser.parse(url)
                category, _ = Category.objects.get_or_create(name=category_name)
                
                if not hasattr(feed, 'entries') or not feed.entries:
                    self.stdout.write(self.style.WARNING(f"No entries found for {source}"))
                    continue

                article_count = 0
                for entry in feed.entries[:20]: # Fetch up to 20 articles per feed
                    # Check if article already exists (with retry for database locking)
                    max_retries = 3
                    retry_count = 0
                    article_exists = False
                    
                    while retry_count < max_retries:
                        try:
                            article_exists = News.objects.filter(link=entry.link).exists()
                            break
                        except Exception as e:
                            retry_count += 1
                            if retry_count < max_retries:
                                sleep(0.1 * retry_count)  # Exponential backoff
                            else:
                                self.stdout.write(self.style.WARNING(f"Database error checking article: {str(e)}"))
                                break
                    
                    if article_exists:
                        continue
                    
                    # Date parsing
                    pub_date = None
                    if hasattr(entry, 'published_parsed'):
                        try:
                            dt = datetime.fromtimestamp(mktime(entry.published_parsed))
                            pub_date = make_aware(dt)
                        except Exception:
                            pub_date = None
                    
                    # Image extraction (simplified for faster fetching)
                    image_url = None
                    
                    # Method 1: Try media_content (RSS media extensions)
                    if 'media_content' in entry and len(entry.media_content) > 0:
                        for media in entry.media_content:
                            if media.get('type', '').startswith('image/'):
                                image_url = media.get('url', '')
                                break
                    
                    # Method 2: Try media_thumbnail
                    if not image_url and 'media_thumbnail' in entry and len(entry.media_thumbnail) > 0:
                        image_url = entry.media_thumbnail[0].get('url', '')
                    
                    # Method 3: Extract from summary/description HTML
                    if not image_url and 'summary' in entry:
                        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', entry.summary)
                        if img_match:
                            image_url = img_match.group(1)
                    
                    # Create article with retry logic for database locking
                    retry_count = 0
                    created = False
                    while retry_count < max_retries and not created:
                        try:
                            with transaction.atomic():
                                News.objects.create(
                                    title=entry.title[:500],
                                    link=entry.link,
                                    image=image_url,
                                    description=entry.get('summary', '')[:500] if entry.get('summary') else '',
                                    pub_date=pub_date,
                                    source=source,
                                    category=category,
                                    guid=entry.get('id', entry.link)
                                )
                            created = True
                            article_count += 1
                        except Exception as e:
                            retry_count += 1
                            if 'locked' in str(e).lower() or 'database' in str(e).lower():
                                if retry_count < max_retries:
                                    sleep(0.2 * retry_count)  # Wait longer for database locks
                                else:
                                    self.stdout.write(self.style.WARNING(f"Failed to create article after {max_retries} retries: {str(e)}"))
                            else:
                                # Other errors, don't retry
                                break
                    
                    # Small delay between articles to reduce database contention
                    if article_count % 5 == 0:
                        sleep(0.1)
                
                if article_count > 0:
                    self.stdout.write(self.style.SUCCESS(f"✅ Fetched {article_count} articles from {source}"))
                    # Track category counts
                    if category_name not in category_counts:
                        category_counts[category_name] = 0
                    category_counts[category_name] += article_count
            except Exception as e:
                error_msg = str(e)
                if 'locked' in error_msg.lower():
                    self.stdout.write(self.style.WARNING(f"⚠️ Database locked for {source}, will retry later. Error: {error_msg}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ Failed to fetch {source}: {error_msg}"))
                # Continue with next feed even if one fails
                continue
                # Small delay before next feed
                sleep(0.5)

        # Summary
        total_articles = News.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\n✅ RSS fetch completed!'))
        self.stdout.write(self.style.SUCCESS(f'Total articles in database: {total_articles}'))
        
        if category_counts:
            self.stdout.write(self.style.SUCCESS('\nArticles by category:'))
            for category, count in category_counts.items():
                self.stdout.write(self.style.SUCCESS(f'  - {category}: {count} articles'))
        
        # Verify all categories have articles
        from news.models import Category
        all_categories = Category.objects.all()
        missing_categories = []
        for cat in all_categories:
            cat_count = News.objects.filter(category=cat).count()
            if cat_count == 0:
                missing_categories.append(cat.name)
        
        if missing_categories:
            self.stdout.write(self.style.WARNING(f'\n⚠️ Categories with no articles: {", ".join(missing_categories)}'))
            self.stdout.write(self.style.WARNING('You may want to run this command again to fetch articles for these categories.'))
