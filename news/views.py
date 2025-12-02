from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import News, Category, SavedArticle

from django.db.models import Q

from django.utils.dateparse import parse_datetime

def home(request):
    # Auto-fetch articles if database is empty (only on first request)
    if News.objects.count() == 0 and not hasattr(request, '_fetch_triggered'):
        # Trigger fetch in background using threading
        import threading
        from django.core.management import call_command
        
        def fetch_in_background():
            try:
                call_command('fetch_feeds', verbosity=0)
            except Exception:
                pass  # Silently fail in background
        
        thread = threading.Thread(target=fetch_in_background, daemon=True)
        thread.start()
        request._fetch_triggered = True
    
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    
    # Start with all news from local DB
    news_list = News.objects.all()
    
    # Apply category filter if provided
    if category_id:
        news_list = news_list.filter(category_id=category_id)
    
    # Handle search query - search local database only
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(source__icontains=search_query)
        )

    # Order by publication date (newest first)
    news_list = news_list.order_by('-pub_date')

    paginator = Paginator(news_list, 20) # 20 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Ensure default categories exist (create if they don't)
    default_categories = ['Technology', 'Sports', 'World']
    for cat_name in default_categories:
        Category.objects.get_or_create(name=cat_name)
    
    # Only show Technology, Sports, and World categories
    categories = Category.objects.filter(name__in=default_categories).order_by('name')
    
    # Check which articles are saved by the user
    saved_news_ids = []
    if request.user.is_authenticated:
        saved_news_ids = list(SavedArticle.objects.filter(user=request.user).values_list('news_id', flat=True))

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'saved_news_ids': saved_news_ids,
        'selected_category': int(category_id) if category_id else None
    }
    return render(request, 'news/home.html', context)

@login_required
def saved_articles(request):
    saved_list = SavedArticle.objects.filter(user=request.user).select_related('news').order_by('-saved_date')
    
    paginator = Paginator(saved_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/saved.html', {'page_obj': page_obj})

@login_required
def toggle_save(request, news_id):
    news = get_object_or_404(News, id=news_id)
    saved_article, created = SavedArticle.objects.get_or_create(user=request.user, news=news)
    
    if not created:
        # If already exists, delete it (toggle off)
        saved_article.delete()
        messages.success(request, 'Article removed from saved list.')
    else:
        messages.success(request, 'Article saved.')
    
    # Redirect back to where the user came from
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('home')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
