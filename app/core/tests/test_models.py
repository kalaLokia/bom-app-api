from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@kalalokia.xyz', password='testpass'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_creating_user_success(self):
        """Test creating a user with email and password is successful"""

        email = 'test@kalalokia.xyz'
        password = 'test1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_with_valid_email(self):
        """Test creating a new user with a valid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    def test_new_user_normalized_email(self):
        """Test user email is normalized"""
        email = 'test@kalaLOKIA.xyz'
        user = get_user_model().objects.create_user(
            email=email,
            password='test1234'
        )

        self.assertEqual(user.email, email.lower())

    def test_creating_superuser_success(self):
        """
        Test creating a new super user with email and password is successful
        """
        email = 'test@kalalokia.xyz'
        password = 'test1234'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_color_str(self):
        """Test the color string representation"""
        color = models.Color.objects.create(
            user=sample_user(),
            name='black',
            code='bk'
        )

        self.assertEqual(str(color), color.name)

    def test_article_str(self):
        """Test the article string representation"""
        article = models.Article.objects.create(
            user=sample_user(),
            artno='3290',
            brand='pride',
            style='covering'
        )

        self.assertEqual(str(article), article.artno)

    def test_article_detail_str(self):
        """Test the article detail string representation"""
        user = sample_user()
        article = models.Article.objects.create(
            user=user,
            artno='3290'
        )
        color = models.Color.objects.create(
            user=user,
            name='black',
            code='bk'
        )
        article_detail = models.ArticleDetail.objects.create(
            user=user,
            article=article,
            color=color,
            category='g',
            price=290.00,
            active=True,
            artid='3290-bk-g'
        )

        self.assertEqual(str(article_detail), article_detail.artid)
