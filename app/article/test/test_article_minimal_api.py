"""
Public minimal article api access tests
"""

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import ArticleInfo

from article.serializers import ArticlePublicSerializer

from . import samples


ARTICLE_PUBLIC_URL = reverse('article:article-minimal-list')


class PublicArticleinfoApiTests(TestCase):
    """Test public article-minimal api access"""

    def setUp(self):
        self.client = APIClient()
        self.sample_user = get_user_model().objects.create_user(
            'test@kalalokia.xyz',
            'testpass'
        )

    def test_public_access(self):
        """Test that authentication is not required"""
        res = self.client.get(ARTICLE_PUBLIC_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_minimal_article_data(self):
        """
        Test only minimal data is provided for public:
            "Article, Color, Category, Price, Active"
        """
        samples.article_info(
            user=self.sample_user,
            article=samples.article(user=self.sample_user),
            color=samples.color(user=self.sample_user)
        )
        articles = ArticleInfo.objects.all()
        data = ['article', 'color', 'mcategory', 'price', 'active']

        res = self.client.get(ARTICLE_PUBLIC_URL)

        serializer = ArticlePublicSerializer(articles, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(list(serializer.data[0].keys()), data)
