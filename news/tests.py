from django.test import TestCase
from django.contrib.auth.models import User
from .models import News, Category, SavedArticle

class NewsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Technology')
        self.news = News.objects.create(
            title='Test News Article',
            link='https://example.com/test',
            description='This is a test article',
            source='Test Source',
            category=self.category
        )

    def test_news_creation(self):
        """Test that a news article can be created"""
        self.assertEqual(self.news.title, 'Test News Article')
        self.assertEqual(self.news.category.name, 'Technology')
        self.assertEqual(str(self.news), 'Test News Article')

    def test_news_unique_link(self):
        """Test that duplicate URLs are prevented"""
        with self.assertRaises(Exception):
            News.objects.create(
                title='Duplicate News',
                link='https://example.com/test',  # Same URL
                source='Another Source'
            )

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        """Test that a category can be created"""
        category = Category.objects.create(name='Sports')
        self.assertEqual(category.name, 'Sports')
        self.assertEqual(str(category), 'Sports')

class SavedArticleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.news = News.objects.create(
            title='Test Article',
            link='https://example.com/article',
            source='Test Source'
        )

    def test_save_article(self):
        """Test that a user can save an article"""
        saved = SavedArticle.objects.create(user=self.user, news=self.news)
        self.assertEqual(saved.user.username, 'testuser')
        self.assertEqual(saved.news.title, 'Test Article')

    def test_unique_save(self):
        """Test that a user cannot save the same article twice"""
        SavedArticle.objects.create(user=self.user, news=self.news)
        with self.assertRaises(Exception):
            SavedArticle.objects.create(user=self.user, news=self.news)

class HomeViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='World')
        News.objects.create(
            title='Test News 1',
            link='https://example.com/1',
            description='Description 1',
            source='Source 1',
            category=self.category
        )

    def test_home_page(self):
        """Test that home page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test News 1')

    def test_category_filter(self):
        """Test that category filtering works"""
        response = self.client.get(f'/?category={self.category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test News 1')
