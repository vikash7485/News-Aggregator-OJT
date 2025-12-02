"""
Management command to update existing articles with missing images
"""
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db.models import Q
from news.models import News
import re
from urllib.parse import urljoin

class Command(BaseCommand):
    help = 'Update existing articles that are missing images by fetching from article pages'

    def handle(self, *args, **kwargs):
        self.stdout.write("Updating articles with missing images...")
        
        # Get articles without images
        articles_without_images = News.objects.filter(
            Q(image__isnull=True) | Q(image='')
        )
        
        total = articles_without_images.count()
        self.stdout.write(f"Found {total} articles without images")
        
        updated = 0
        failed = 0
        
        for article in articles_without_images:
            if not article.link:
                continue
            
            try:
                # Fetch the article page
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(article.link, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    image_url = None
                    
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
                        img_tags = soup.find_all('img', class_=re.compile(r'article|feature|hero|main|content', re.I))
                        if img_tags:
                            for img in img_tags:
                                src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                                if src and not src.startswith('data:'):
                                    if src.startswith('//'):
                                        image_url = 'https:' + src
                                    elif src.startswith('/'):
                                        image_url = urljoin(article.link, src)
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
                                    if size > max_size and size > 10000:
                                        max_size = size
                                        largest_img = src
                            
                            if largest_img:
                                if largest_img.startswith('//'):
                                    image_url = 'https:' + largest_img
                                elif largest_img.startswith('/'):
                                    image_url = urljoin(article.link, largest_img)
                                else:
                                    image_url = largest_img
                    
                    if image_url:
                        article.image = image_url
                        article.save()
                        updated += 1
                        self.stdout.write(f"  ✅ Updated: {article.title[:50]}...")
                    else:
                        failed += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                # Silently continue
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Updated {updated} articles with images'))
        if failed > 0:
            self.stdout.write(self.style.WARNING(f'⚠️  Could not update {failed} articles'))

