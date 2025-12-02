from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class News(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField(unique=True, max_length=500) # Prevent duplicates by URL
    image = models.URLField(blank=True, null=True, max_length=500)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    guid = models.CharField(max_length=255, blank=True, null=True) # Optional extra deduplication

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-pub_date']

class SavedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'news') # Prevent saving same article twice

    def __str__(self):
        return f"{self.user.username} - {self.news.title}"
