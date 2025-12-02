from django.contrib import admin
from .models import Category, News, SavedArticle

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'pub_date', 'category')
    list_filter = ('source', 'category', 'pub_date')
    search_fields = ('title', 'description')

@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'saved_date')
