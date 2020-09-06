from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Article

from article.serializers import ArticleSerializer


ARTICLE_URL = reverse('article:article-list')


def sample_article(user, **params):
    """Create and return a sample article"""
    defaults = {
        'artno': '3290',
        'brand': 'pride',
        'style': 'covering'
    }
    defaults.update(params)

    return Article.objects.create(user=user, **defaults)


class PublicArticleApiTests(TestCase):
    """test unauthenticated article api access"""

    def setUp(self):
        self.client = APIClient()

    def test_unauth_access(self):
        """Test that authentication is required"""
        res = self.client.get(ARTICLE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateArticleApiTests(TestCase):
    """test authenticated article api requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@kalalokia.xyz',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_articles(self):
        """Test retrieving a list of articles"""
        sample_article(user=self.user)
        sample_article(user=self.user, artno='3780')

        res = self.client.get(ARTICLE_URL)

        articles = Article.objects.all().order_by('-id')
        serializer = ArticleSerializer(articles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
