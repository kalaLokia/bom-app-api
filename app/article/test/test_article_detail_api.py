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

        self.article_1 = sample_article(user=self.user)
        self.article_2 = sample_article(user=self.user, artno='3780')
        self.color_1 = sample_color(user=self.user)
        self.color_2 = sample_color(user=self.user, code='br', name='brown')

    def test_retrieve_articles(self):
        """Test retrieving a list of articles"""

        sample_article_detail(user=self.user,
                              article=self.article_1,
                              color=self.color_1)
        sample_article_detail(user=self.user,
                              article=self.article_2,
                              color=self.color_1)
        sample_article_detail(user=self.user,
                              article=self.article_2,
                              color=self.color_2)

        res = self.client.get(ARTICLE_DETAIL_URL)

        articles = ArticleDetail.objects.all()
        serializer = ArticleDetailSerializer(articles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 3)

    def test_create_article_success(self):
        """Test that creating article detail is successful"""
        payload = {
            'article': self.article_1.id,
            'color': self.color_1.id,
            'category': 'g',
            'artid': '3290-bk-g'
        }

        res = self.client.post(ARTICLE_DETAIL_URL, payload)

        exists = ArticleDetail.objects.filter(
            user=self.user,
            artid=payload['artid']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_article_invalid_foreign_key(self):
        """
        The that creating article detail with invalid foreign key.
        #1: model expecting id field from foreign model
        #2: foreign models are mandatory fields
        """
        payload1 = {
            'article': self.article_1,
            'color': self.color_1,
            'category': 'g',
            'artid': '3290-bk-g'
        }
        payload2 = {
            'article': self.article_1.id,
            'category': 'g',
            'artid': '3290-bk-g'
        }
        payload3 = {
            'color': self.color_1.id,
            'category': 'g',
            'artid': '3290-bk-g'
        }
        res1 = self.client.post(ARTICLE_DETAIL_URL, payload1)

        res2 = self.client.post(ARTICLE_DETAIL_URL, payload2)
        res3 = self.client.post(ARTICLE_DETAIL_URL, payload3)

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_invalid(self):
        """
        Test creating article detail with invalid payload fails.
        #1: without category field
        #2: without artid 
        """
        payload1 = {
            'article': self.article_1.id,
            'color': self.color_1.id,
            'artid': '3290-bk-g'
        }
        payload2 = {
            'article': self.article_1.id,
            'color': self.color_1.id,
            'category': 'g'
        }

        res1 = self.client.post(ARTICLE_DETAIL_URL, payload1)
        res2 = self.client.post(ARTICLE_DETAIL_URL, payload2)

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
