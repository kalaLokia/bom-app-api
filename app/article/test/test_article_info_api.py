from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import ArticleInfo

from article.serializers import ArticleInfoSerializer, \
                                ArticleInfoDetailSerializer

from . import samples


ARTICLE_INFO_URL = reverse('article:articleinfo-list')


def detail_url(articleinfo_id):
    """Return the detail url for article info"""
    return reverse('article:articleinfo-detail', args=[articleinfo_id])


class PublicArticleinfoApiTests(TestCase):
    """Test unauthenticated article-info api access"""

    def setUp(self):
        self.client = APIClient()

    def test_unauth_access(self):
        """Test that authentication is required"""
        res = self.client.get(ARTICLE_INFO_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateArticleinfoApiTests(TestCase):
    """Test authenticated article-info api requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@kalalokia.xyz',
            'testpass'
        )
        self.client.force_authenticate(self.user)

        self.article_1 = samples.article(user=self.user)
        self.article_2 = samples.article(user=self.user, artno='3780')
        self.color_1 = samples.color(user=self.user)
        self.color_2 = samples.color(user=self.user, code='br', name='brown')

    def test_retrieve_articleinfos(self):
        """Test retrieving a list of articles"""

        samples.article_info(user=self.user,
                             article=self.article_1,
                             color=self.color_1)
        samples.article_info(user=self.user,
                             article=self.article_2,
                             color=self.color_1)
        samples.article_info(user=self.user,
                             article=self.article_2,
                             color=self.color_2)

        res = self.client.get(ARTICLE_INFO_URL)

        articles = ArticleInfo.objects.all()
        serializer = ArticleInfoSerializer(articles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 3)

    def test_create_articleinfo_success(self):
        """Test that creating article info is successful"""
        payload = {
            'article': self.article_1.id,
            'color': self.color_1.id,
            'category': 'g',
        }

        res = self.client.post(ARTICLE_INFO_URL, payload)

        exists = ArticleInfo.objects.filter(
            user=self.user,
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_articleinfo_invalid_foreign_key(self):
        """
        The that creating article info with invalid foreign key.
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
        res1 = self.client.post(ARTICLE_INFO_URL, payload1)

        res2 = self.client.post(ARTICLE_INFO_URL, payload2)
        res3 = self.client.post(ARTICLE_INFO_URL, payload3)

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_articleinfo_invalid(self):
        """
        Test creating article info with invalid payload fails.
        #1: without category field
        """
        payload1 = {
            'article': self.article_1.id,
            'color': self.color_1.id,
        }

        res1 = self.client.post(ARTICLE_INFO_URL, payload1)

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_articleinfo_fails(self):
        """Test that creating article info with duplicate artid fails"""
        samples.article_info(user=self.user,
                             article=self.article_1,
                             color=self.color_1)
        payload = {
            'article': self.article_1.id,
            'color': self.color_1.id,
            'category': 'g'
        }

        res = self.client.post(ARTICLE_INFO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_articleinfo_detail(self):
        """Test viewing a article info in detail"""
        articleinfo = samples.article_info(user=self.user,
                                           article=self.article_1,
                                           color=self.color_1)

        url = detail_url(articleinfo.id)
        res = self.client.get(url)

        serializer = ArticleInfoDetailSerializer(articleinfo)

        self.assertEqual(res.data, serializer.data)
