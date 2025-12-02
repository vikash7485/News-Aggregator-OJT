"""
Django signals to sync data to MongoDB
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import News, Category, SavedArticle
from .mongodb_utils import get_mongodb_database
from django.contrib.auth.models import User
from datetime import datetime

@receiver(post_save, sender=News)
def sync_news_to_mongodb(sender, instance, created, **kwargs):
    """Sync News model to MongoDB"""
    try:
        db = get_mongodb_database()
        if db is None:
            return
        
        collection = db['news']
        news_doc = {
            '_id': instance.id,
            'title': instance.title,
            'link': instance.link,
            'image': instance.image or '',
            'description': instance.description or '',
            'content': instance.content or '',
            'author': instance.author or '',
            'pub_date': instance.pub_date.isoformat() if instance.pub_date else None,
            'source': instance.source,
            'category': instance.category.name if instance.category else None,
            'category_id': instance.category.id if instance.category else None,
            'guid': instance.guid or '',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        collection.replace_one({'_id': instance.id}, news_doc, upsert=True)
    except Exception as e:
        print(f"Error syncing News to MongoDB: {e}")

@receiver(post_save, sender=Category)
def sync_category_to_mongodb(sender, instance, created, **kwargs):
    """Sync Category model to MongoDB"""
    try:
        db = get_mongodb_database()
        if db is None:
            return
        
        collection = db['categories']
        category_doc = {
            '_id': instance.id,
            'name': instance.name,
            'created_at': datetime.now().isoformat()
        }
        collection.replace_one({'_id': instance.id}, category_doc, upsert=True)
    except Exception as e:
        print(f"Error syncing Category to MongoDB: {e}")

@receiver(post_save, sender=SavedArticle)
def sync_saved_article_to_mongodb(sender, instance, created, **kwargs):
    """Sync SavedArticle model to MongoDB"""
    try:
        db = get_mongodb_database()
        if db is None:
            return
        
        collection = db['saved_articles']
        saved_doc = {
            '_id': f"{instance.user.id}_{instance.news.id}",
            'user_id': instance.user.id,
            'username': instance.user.username,
            'news_id': instance.news.id,
            'news_title': instance.news.title,
            'news_link': instance.news.link,
            'saved_date': instance.saved_date.isoformat() if instance.saved_date else None,
            'created_at': datetime.now().isoformat()
        }
        collection.replace_one({'_id': f"{instance.user.id}_{instance.news.id}"}, saved_doc, upsert=True)
    except Exception as e:
        print(f"Error syncing SavedArticle to MongoDB: {e}")

@receiver(post_delete, sender=SavedArticle)
def delete_saved_article_from_mongodb(sender, instance, **kwargs):
    """Delete SavedArticle from MongoDB when deleted from SQLite"""
    try:
        db = get_mongodb_database()
        if db is None:
            return
        
        collection = db['saved_articles']
        collection.delete_one({'_id': f"{instance.user.id}_{instance.news.id}"})
    except Exception as e:
        print(f"Error deleting SavedArticle from MongoDB: {e}")

@receiver(post_save, sender=User)
def sync_user_to_mongodb(sender, instance, created, **kwargs):
    """Sync User model to MongoDB"""
    try:
        db = get_mongodb_database()
        if db is None:
            return
        
        collection = db['users']
        user_doc = {
            '_id': instance.id,
            'username': instance.username,
            'email': instance.email or '',
            'date_joined': instance.date_joined.isoformat() if instance.date_joined else None,
            'is_active': instance.is_active,
            'created_at': datetime.now().isoformat()
        }
        collection.replace_one({'_id': instance.id}, user_doc, upsert=True)
    except Exception as e:
        print(f"Error syncing User to MongoDB: {e}")

