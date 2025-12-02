import feedparser
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import datetime
from time import mktime
from news.models import News, Category
import re

class Command(BaseCommand):
    help = 'Fetches news from RSS feeds'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting RSS fetch...")
        
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

                for entry in feed.entries[:20]: # Fetch up to 20 articles per feed (reduced for faster initial fetch)
                    if News.objects.filter(link=entry.link).exists():
                        continue
                    
                    # Date parsing
                    pub_date = None
                    if hasattr(entry, 'published_parsed'):
                        try:
                            dt = datetime.fromtimestamp(mktime(entry.published_parsed))
                            pub_date = make_aware(dt)
                        except Exception:
                            pub_date = None
                    
                    # Image extraction (comprehensive)
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
                    
                    # Method 3: Check links for image types
                    if not image_url and 'links' in entry:
                        for link in entry.links:
                            if link.get('type', '').startswith('image/'):
                                image_url = link.get('href', '')
                                break
                    
                    # Method 4: Extract from summary/description HTML
                    if not image_url and 'summary' in entry:
                        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', entry.summary)
                        if img_match:
                            image_url = img_match.group(1)
                    
                    # Method 5: Extract from content if available
                    if not image_url and 'content' in entry:
                        for content_item in entry.content:
                            img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content_item.value)
                            if img_match:
                                image_url = img_match.group(1)
                                break
                    
                    # Method 6: Fetch from article page (for TechCrunch, ESPN, etc.)
                    # Skip this on first run to speed up - can be done later
                    if not image_url and entry.link and False:  # Disabled for faster initial fetch
                        try:
                            # Fetch the article page
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            }
                            response = requests.get(entry.link, headers=headers, timeout=3)
                            if response.status_code == 200:
                                soup = BeautifulSoup(response.content, 'html.parser')
                                
                                # Try Open Graph image (og:image)
                                og_image = soup.find('meta', property='og:image')
                                if og_image and og_image.get('content'):
                                    image_url = og_image['content']
                                
                                # Try Twitter card image
                                if not image_url:
                                    twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
                                    if twitter_image and twitter_image.get('content'):
                                        image_url = twitter_image['content']
                                
                                # Try article image meta tag
                                if not image_url:
                                    article_image = soup.find('meta', attrs={'name': 'article:image'})
                                    if article_image and article_image.get('content'):
                                        image_url = article_image['content']
                                
                                # Try to find first large image in article
                                if not image_url:
                                    # Look for images with common article image classes
                                    img_tags = soup.find_all('img', class_=re.compile(r'article|feature|hero|main|content', re.I))
                                    if img_tags:
                                        for img in img_tags:
                                            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                                            if src and not src.startswith('data:'):
                                                # Make absolute URL if relative
                                                if src.startswith('//'):
                                                    image_url = 'https:' + src
                                                elif src.startswith('/'):
                                                    from urllib.parse import urljoin
                                                    image_url = urljoin(entry.link, src)
                                                else:
                                                    image_url = src
                                                break
                                    
                                    # Fallback: find largest image
                                    if not image_url:
                                        all_imgs = soup.find_all('img')
                                        largest_img = None
                                        max_size = 0
                                        for img in all_imgs:
                                            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                                            if src and not src.startswith('data:'):
                                                width = int(img.get('width', 0) or 0)
                                                height = int(img.get('height', 0) or 0)
                                                size = width * height
                                                if size > max_size and size > 10000:  # At least 100x100
                                                    max_size = size
                                                    largest_img = src
                                        
                                        if largest_img:
                                            if largest_img.startswith('//'):
                                                image_url = 'https:' + largest_img
                                            elif largest_img.startswith('/'):
                                                from urllib.parse import urljoin
                                                image_url = urljoin(entry.link, largest_img)
                                            else:
                                                image_url = largest_img
                        except Exception as e:
                            # Silently fail - article page might not be accessible
                            pass
                    
                    News.objects.create(
                        title=entry.title[:500],
                        link=entry.link,
                        image=image_url,
                        description=entry.get('summary', '')[:500],
                        pub_date=pub_date,
                        source=source,
                        category=category,
                        guid=entry.get('id', entry.link)
                    )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to fetch {source}: {str(e)}"))
                continue

        self.stdout.write(self.style.SUCCESS('Successfully fetched RSS news'))
