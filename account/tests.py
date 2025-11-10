from django.test import TestCase
from django.contrib.auth.models import User
from .models import Article

class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.article = Article.objects.create(
            title="Test Article",
            slug="test-article",
            description="Test Description",
            category="Test Category",
            author=self.user
        )

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(str(self.article.author), 'testuser')
