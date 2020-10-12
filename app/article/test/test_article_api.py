"""
All Article model related tests are here.
"""
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
    """Returns the detailed view of an article"""
    return reverse('article:article-detail', args=[article_id])


class PublicArticleApiTests(TestCase):
    """Test unauthenticated article api access"""

    def setUp(self):
        self.client = APIClient()

    def test_unauth_access(self):
        """Test that authentication is required"""
        res = self.client.get(ARTICLE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateArticleApiTests(TestCase):
    """
    Test authenticated article api requests.
        * Retrieving list of article objects.
        * Creating a object is successful.
            * Fails with invalid data.
            * Fails with duplicated data (on unique fields).
        * Getting detailed view of a object.
    """

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
        samples.article_info(
            user=self.user, article=article, color=color
        )

        res = self.client.get(detail_url(article.id))
        serializer = ArticleDetailSerializer(article)

        self.assertEqual(res.data, serializer.data)


class FilterArticleApiTests(TestCase):
    """
    Test filtering on Article model by:
        * brand
        * style
        * color    (code) [related field]
        * category (main category) [related field[]
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@kalalokia.xyz',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_filter_brand(self):
        """Test filter article by brand"""
        article1 = samples.article(user=self.user, brand='pride')
        article2 = samples.article(
            user=self.user, artno='6359', brand='stile'
        )
        article3 = samples.article(
            user=self.user, artno='d4303', brand='debongo'
        )
        article4 = samples.article(
            user=self.user, artno='8493', brand='pride'
        )
        article5 = samples.article(
            user=self.user, artno='k6012', brand='')

        res = self.client.get(
            ARTICLE_URL,
            {'brand': f'{article2.brand}, {article1.brand}'}
        )

        serializer1 = ArticleSerializer(article1)
        serializer2 = ArticleSerializer(article2)
        serializer3 = ArticleSerializer(article3)
        serializer4 = ArticleSerializer(article4)
        serializer5 = ArticleSerializer(article5)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
        self.assertIn(serializer4.data, res.data)
        self.assertNotIn(serializer5.data, res.data)

    def test_filter_style(self):
        """Test filter article by style"""
        article1 = samples.article(user=self.user, style='covering')
        article2 = samples.article(
            user=self.user, artno='3510', style='sandal'
        )
        article3 = samples.article(
            user=self.user, artno='d4303', style='v-strap'
        )
        article4 = samples.article(
            user=self.user, artno='8493', style='covering'
        )
        article5 = samples.article(
            user=self.user, artno='k6012', style='')

        res = self.client.get(
            ARTICLE_URL,
            {'style': f'{article2.style}, {article1.style}'}
        )

        serializer1 = ArticleSerializer(article1)
        serializer2 = ArticleSerializer(article2)
        serializer3 = ArticleSerializer(article3)
        serializer4 = ArticleSerializer(article4)
        serializer5 = ArticleSerializer(article5)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
        self.assertIn(serializer4.data, res.data)
        self.assertNotIn(serializer5.data, res.data)

    def test_filter_color(self):
        """Test filter article if the color is available"""

        article1 = samples.article(user=self.user)
        article2 = samples.article(
            user=self.user, artno="d4303", brand="debongo"
        )
        article3 = samples.article(
            user=self.user, artno="d4109", brand="debongo"
        )
        color1 = samples.color(user=self.user)
        color2 = samples.color(user=self.user, name="grey", code="gy")
        color3 = samples.color(user=self.user, name="orange", code="or")

        samples.article_info(
            user=self.user, article=article1, color=color1
        )
        samples.article_info(
            user=self.user, article=article2, color=color1
        )
        samples.article_info(
            user=self.user, article=article2, color=color2
        )
        samples.article_info(
            user=self.user, article=article3, color=color3
        )

        res = self.client.get(ARTICLE_URL, {'color': f'{color1.code}'})

        serializer1 = ArticleSerializer(article1)
        serializer2 = ArticleSerializer(article2)
        serializer3 = ArticleSerializer(article3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_category(self):
        """Test filter article by main category"""

        article1 = samples.article(user=self.user)
        article2 = samples.article(user=self.user, artno="d4303")
        article3 = samples.article(user=self.user, artno="k6012")
        article4 = samples.article(user=self.user, artno="3844")
        color = samples.color(user=self.user)

        samples.article_info(
            user=self.user, article=article1,
            color=color, category='g'
        )
        samples.article_info(
            user=self.user, article=article2,
            color=color, category='g'
        )
        samples.article_info(
            user=self.user, article=article2,
            color=color, category='x'
        )
        samples.article_info(
            user=self.user, article=article3,
            color=color, category='k'
        )
        samples.article_info(
            user=self.user, article=article4,
            color=color, category='r'
        )

        res = self.client.get(ARTICLE_URL, {'category': 'kids, giants'})

        serializer1 = ArticleSerializer(article1)
        serializer2 = ArticleSerializer(article2)
        serializer3 = ArticleSerializer(article3)
        serializer4 = ArticleSerializer(article4)

        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertIn(serializer3.data, res.data)
        self.assertIn(serializer4.data, res.data)
