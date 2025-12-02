"""
Management command to sync existing data to MongoDB
"""
from django.core.management.base import BaseCommand
from news.models import News, Category, SavedArticle
from news.mongodb_utils import get_mongodb_database
from django.contrib.auth.models import User
from datetime import datetime

class Command(BaseCommand):
    help = 'Sync all existing data from SQLite to MongoDB'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting MongoDB sync...")
        
        db = get_mongodb_database()
        if db is None:
            self.stdout.write(self.style.ERROR('❌ Could not connect to MongoDB. Check MONGODB_URL in .env'))
            return
        
        # Sync Categories
        self.stdout.write("Syncing Categories...")
        categories_collection = db['categories']
        for category in Category.objects.all():
            category_doc = {
                '_id': category.id,
                'name': category.name,
                'created_at': datetime.now().isoformat()
            }
            categories_collection.replace_one({'_id': category.id}, category_doc, upsert=True)
        self.stdout.write(self.style.SUCCESS(f'✅ Synced {Category.objects.count()} categories'))

        # Sync News
        self.stdout.write("Syncing News articles...")
        news_collection = db['news']
        count = 0
        for news in News.objects.all():
            news_doc = {
                '_id': news.id,
                'title': news.title,
                'link': news.link,
                'image': news.image or '',
                'description': news.description or '',
                'content': news.content or '',
                'author': news.author or '',
                'pub_date': news.pub_date.isoformat() if news.pub_date else None,
                'source': news.source,
                'category': news.category.name if news.category else None,
                'category_id': news.category.id if news.category else None,
                'guid': news.guid or '',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            news_collection.replace_one({'_id': news.id}, news_doc, upsert=True)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'✅ Synced {count} news articles'))

        # Sync Users
        self.stdout.write("Syncing Users...")
        users_collection = db['users']
        for user in User.objects.all():
            user_doc = {
                '_id': user.id,
                'username': user.username,
                'email': user.email or '',
                'date_joined': user.date_joined.isoformat() if user.date_joined else None,
                'is_active': user.is_active,
                'created_at': datetime.now().isoformat()
            }
            users_collection.replace_one({'_id': user.id}, user_doc, upsert=True)
        self.stdout.write(self.style.SUCCESS(f'✅ Synced {User.objects.count()} users'))

        # Sync Saved Articles
        self.stdout.write("Syncing Saved Articles...")
        saved_collection = db['saved_articles']
        count = 0
        for saved in SavedArticle.objects.all():
            saved_doc = {
                '_id': f"{saved.user.id}_{saved.news.id}",
                'user_id': saved.user.id,
                'username': saved.user.username,
                'news_id': saved.news.id,
                'news_title': saved.news.title,
                'news_link': saved.news.link,
                'saved_date': saved.saved_date.isoformat() if saved.saved_date else None,
                'created_at': datetime.now().isoformat()
            }
            saved_collection.replace_one({'_id': f"{saved.user.id}_{saved.news.id}"}, saved_doc, upsert=True)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'✅ Synced {count} saved articles'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Successfully synced all data to MongoDB!'))
        self.stdout.write('You can now see the data in MongoDB Compass:')
        self.stdout.write('  - Database: news_aggregator')
        self.stdout.write('  - Collections: categories, news, users, saved_articles')

