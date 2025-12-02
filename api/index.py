"""
Vercel serverless function for Django WSGI application
This file must be in the api/ directory for Vercel to recognize it as a serverless function.
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Export the WSGI application - Vercel will use this
app = get_wsgi_application()

