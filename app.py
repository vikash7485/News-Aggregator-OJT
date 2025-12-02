"""
WSGI entry point for Render deployment.
This file allows Render to use 'gunicorn app:app' command.
"""
import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()

