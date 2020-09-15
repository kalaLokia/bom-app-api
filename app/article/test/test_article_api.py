from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Article

from article.serializers import ArticleSerializer, ArticleDetailSerializer

from . import samples


ARTICLE_URL = reverse('article:article-list')


def detail_url(article_id):
    """Returns the detail view of an article"""
    return reverse('article:article-detail', args=[article_id])


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
        samples.article(user=self.user)
        samples.article(user=self.user, artno='3780')

        res = self.client.get(ARTICLE_URL)

        articles = Article.objects.all().order_by('-id')
        serializer = ArticleSerializer(articles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_article_success(self):
        """Test that creating a article is successful"""
        payload = {'artno': '3780', 'brand': 'pride', 'style': 'covering'}
        self.client.post(ARTICLE_URL, payload)

        exists = Article.objects.filter(
            user=self.user,
            artno=payload['artno']
        ).exists()

        self.assertTrue(exists)

    def test_create_article_invalid(self):
        """Test creating an article with invalid payload"""
        payload = {'artno': '', 'brand': 'pride', 'style': 'sandal'}
        res = self.client.post(ARTICLE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_article_invalid(self):
        """Test that creating article with same artno is invalid"""
        samples.article(user=self.user, artno='3780')
        payload = {'artno': '3780', 'brand': 'stile', 'style': 'covering'}

        res = self.client.post(ARTICLE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_article_detail(self):
        """Test viewing article in detail"""
        article = samples.article(user=self.user)
        color = samples.color(user=self.user)
        samples.article_info(user=self.user,
                             article=article,
                             color=color)

        res = self.client.get(detail_url(article.id))

        serializer = ArticleDetailSerializer(article)

        self.assertEqual(res.data, serializer.data)
