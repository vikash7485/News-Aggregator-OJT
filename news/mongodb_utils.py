"""
MongoDB utility functions for News Aggregator
Note: Currently using SQLite for Django ORM. MongoDB connection is available for future use.
"""
from django.conf import settings
from decouple import config
import pymongo
from urllib.parse import quote_plus

def get_mongodb_connection():
    """
    Get MongoDB connection
    Returns: pymongo.MongoClient or None
    """
    try:
        mongodb_url = config('MONGODB_URL', default=None)
        if not mongodb_url:
            return None
        
        # Parse and connect
        client = pymongo.MongoClient(mongodb_url)
        # Test connection
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None

def get_mongodb_database(db_name='news_aggregator'):
    """
    Get MongoDB database
    Returns: pymongo.database.Database or None
    """
    client = get_mongodb_connection()
    if client is not None:
        return client[db_name]
    return None

