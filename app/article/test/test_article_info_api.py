"""
All ArticleInfo model related tests are here.
"""

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
    """Test authenticated normal user article-info api requests."""

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

    def test_user_create_articleinfo_unsuccess(self):
        """Test that creating article info is unsuccessful by normal user"""
        payload = {
            'article': self.article_1.id,
            'color': self.color_1.id,
            'category': 'g',
        }

        res = self.client.post(ARTICLE_INFO_URL, payload)

        exists = ArticleInfo.objects.filter(
            user=self.user,
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(exists)

    def test_view_articleinfo_detail(self):
        """Test viewing a article info in detail"""
        articleinfo = samples.article_info(user=self.user,
                                           article=self.article_1,
                                           color=self.color_1)

        url = detail_url(articleinfo.id)
        res = self.client.get(url)

        serializer = ArticleInfoDetailSerializer(articleinfo)

        self.assertEqual(res.data, serializer.data)


class ProtectedArticleinfoApiTests(TestCase):
    """Test authenticated admin/staff user article-info api requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='staff@kalalokia.xyz',
            password='staffpass',
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.article_1 = samples.article(user=self.user)
        self.article_2 = samples.article(user=self.user, artno='3780')
        self.color_1 = samples.color(user=self.user)
        self.color_2 = samples.color(user=self.user, code='br', name='brown')

    def test_staff_create_articleinfo_success(self):
        """Test that creating article info is successful by admin/staff"""
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
        #1: model expecting id field from foreign model.
        #2: foreign models are mandatory fields.
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


class FilterArticleInfoApiTests(TestCase):
    """
    Test filtering on ArticleInfo model by:
        * art no   - (artno) [foreign field]
        * brand    - [foreign field]
        * color    - (code|name) [foreign field]
        * style    - [foreign field]
        * category
        * active
        * export
        * TODO: price
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@kalalokia.xyz',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        # Initiating colors to db
        color1 = samples.color(user=self.user)
        color2 = samples.color(user=self.user, name='brown', code='br')
        color3 = samples.color(user=self.user, name='grey', code='gy')
        color4 = samples.color(user=self.user, name='blue', code='bl')
        # Initiating articles to db
        art1 = samples.article(user=self.user)
        art2 = samples.article(
            user=self.user,
            brand='pride',
            artno='8436',
            style='sandal'
        )
        art3 = samples.article(
            user=self.user,
            brand='debongo',
            artno='d4303',
            style='v-strap'
        )
        art4 = samples.article(
            user=self.user,
            artno='k6012',
            brand='kapers',
            style='sandal'
        )
        # Initiating ArticleInfo objects to db
        article1 = samples.article_info(
            user=self.user, article=art1, color=color1, category='g',
            active=True, export=False, price=270
        )
        article2 = samples.article_info(
            user=self.user, article=art1, color=color2, category='g',
            active=False, export=True, price=270
        )
        article3 = samples.article_info(
            user=self.user, article=art2, color=color4, category='l',
            active=False, export=False, price=239
        )
        article4 = samples.article_info(
            user=self.user, article=art3, color=color3, category='x',
            active=True, export=True, price=329
        )
        article5 = samples.article_info(
            user=self.user, article=art4, color=color4, category='k',
            active=False, export=False, price=309
        )
        article6 = samples.article_info(
            user=self.user, article=art4, color=color4, category='b',
            active=False, export=False, price=309
        )
        # Initializing serializers for the articles
        self.serializer1 = ArticleInfoSerializer(article1)
        self.serializer2 = ArticleInfoSerializer(article2)
        self.serializer3 = ArticleInfoSerializer(article3)
        self.serializer4 = ArticleInfoSerializer(article4)
        self.serializer5 = ArticleInfoSerializer(article5)
        self.serializer6 = ArticleInfoSerializer(article6)

    def test_filter_artno(self):
        """Test filter article by art number"""

        res = self.client.get(
            ARTICLE_INFO_URL,
            {'artno': 'k6012, d4303'}
        )

        self.assertNotIn(self.serializer1.data, res.data)
        self.assertNotIn(self.serializer2.data, res.data)
        self.assertNotIn(self.serializer3.data, res.data)
        self.assertIn(self.serializer4.data, res.data)
        self.assertIn(self.serializer5.data, res.data)
        self.assertIn(self.serializer6.data, res.data)

    def test_filter_brand(self):
        """Test filter article by brand name"""

        res = self.client.get(
            ARTICLE_INFO_URL,
            {'brand': 'pride,  debongo'}
        )

        self.assertIn(self.serializer1.data, res.data)
        self.assertIn(self.serializer2.data, res.data)
        self.assertIn(self.serializer3.data, res.data)
        self.assertIn(self.serializer4.data, res.data)
        self.assertNotIn(self.serializer5.data, res.data)
        self.assertNotIn(self.serializer6.data, res.data)

    def test_filter_style(self):
        """Test filter article by style"""

        res = self.client.get(
            ARTICLE_INFO_URL,
            {'style': 'sandal'}
        )

        self.assertNotIn(self.serializer1.data, res.data)
        self.assertNotIn(self.serializer2.data, res.data)
        self.assertIn(self.serializer3.data, res.data)
        self.assertNotIn(self.serializer4.data, res.data)
        self.assertIn(self.serializer5.data, res.data)
        self.assertIn(self.serializer6.data, res.data)

    def test_filter_color(self):
        """Test filter article by their color"""

        res = self.client.get(
            ARTICLE_INFO_URL,
            {'color': 'blue'}
        )

        self.assertNotIn(self.serializer1.data, res.data)
        self.assertNotIn(self.serializer2.data, res.data)
        self.assertIn(self.serializer3.data, res.data)
        self.assertNotIn(self.serializer4.data, res.data)
        self.assertIn(self.serializer5.data, res.data)
        self.assertIn(self.serializer6.data, res.data)

    def test_filter_category(self):
        """Test filter article by category"""

        res = self.client.get(
            ARTICLE_INFO_URL,
            {'category': 'g, x '}
        )

        self.assertIn(self.serializer1.data, res.data)
        self.assertIn(self.serializer2.data, res.data)
        self.assertNotIn(self.serializer3.data, res.data)
        self.assertIn(self.serializer4.data, res.data)
        self.assertNotIn(self.serializer5.data, res.data)
        self.assertNotIn(self.serializer6.data, res.data)

    def test_filter_isactive(self):
        """Test filter active articles"""

        res = self.client.get(
            ARTICLE_INFO_URL,
            {'active': 'true'}
        )

        self.assertIn(self.serializer1.data, res.data)
        self.assertNotIn(self.serializer2.data, res.data)
        self.assertNotIn(self.serializer3.data, res.data)
        self.assertIn(self.serializer4.data, res.data)
        self.assertNotIn(self.serializer5.data, res.data)
        self.assertNotIn(self.serializer6.data, res.data)

    def test_filter_isexport(self):
        """
        Test filter no export articles.
        Given false here is for checking string boolean conversion #views97
        """

        res = self.client.get(
            ARTICLE_INFO_URL,
            {'export': 'False'}
        )

        self.assertIn(self.serializer1.data, res.data)
        self.assertNotIn(self.serializer2.data, res.data)
        self.assertIn(self.serializer3.data, res.data)
        self.assertNotIn(self.serializer4.data, res.data)
        self.assertIn(self.serializer5.data, res.data)
        self.assertIn(self.serializer6.data, res.data)

    def test_filter_invalid_boolean(self):
        """
        Test invalid boolean queryparams fails
        """

        res1 = self.client.get(
            ARTICLE_INFO_URL,
            {'export': 'false and true'}
        )
        res2 = self.client.get(
            ARTICLE_INFO_URL,
            {'export': 'false '}
        )
        res3 = self.client.get(
            ARTICLE_INFO_URL,
            {'active': '3780, pride'}
        )
        res4 = self.client.get(
            ARTICLE_INFO_URL,
            {'active': 'none'}
        )

        self.assertEqual(res1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res3.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res4.status_code, status.HTTP_200_OK)
