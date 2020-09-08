from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import ArticleDetail, Article, Color

from article.serializers import ArticleDetailSerializer


ARTICLE_DETAIL_URL = reverse('article:articledetail-list')


def sample_article(user, **params):
    """Creates a sample article"""
    defaults = {
        'artno': '3290',
        'brand': 'pride',
        'style': 'covering'
    }
    defaults.update(params)

    return Article.objects.create(user=user, **defaults)


def sample_color(user, **params):
    """Creates a sample color"""
    defaults = {
        'code': 'bk',
        'name': 'black'
    }
    defaults.update(params)

    return Color.objects.create(user=user, **defaults)


def sample_article_detail(user, article, color, **params):
    """
    Creates a sample article detail, also accepts models
    "article", "color" in params.
    """

    defaults = {
        'article': article,
        'color': color,
        'category': 'g',
        'price': 270.00
    }
    defaults.update(params)
    artid = "{}-{}-{}".format(defaults['article'].artno,
                              defaults['color'].code, defaults['category'])
    defaults.update({'artid': artid})

    return ArticleDetail.objects.create(user=user, **defaults)


class PublicArticleDetailApiTests(TestCase):
    """Test unauthenticated article-detail api access"""

    def setUp(self):
        self.client = APIClient()

    def test_unauth_access(self):
        """Test that authentication is required"""
        res = self.client.get(ARTICLE_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateArticleDetailApiTests(TestCase):
    """Test authenticated article-detail api requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@kalalokia.xyz',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_articles(self):
        """Test retrieving a list of articles"""
        article_1 = sample_article(user=self.user)
        article_2 = sample_article(user=self.user, artno='3780')
        color_1 = sample_color(user=self.user)
        color_2 = sample_color(user=self.user, code='br', name='brown')

        sample_article_detail(user=self.user,
                              article=article_1,
                              color=color_1)
        sample_article_detail(user=self.user,
                              article=article_2,
                              color=color_1)
        sample_article_detail(user=self.user,
                              article=article_2,
                              color=color_2)

        res = self.client.get(ARTICLE_DETAIL_URL)

        articles = ArticleDetail.objects.all()
        serializer = ArticleDetailSerializer(articles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 3)
