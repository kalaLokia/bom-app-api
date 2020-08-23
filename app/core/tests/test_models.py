from django.test import TestCase
from django.contrib.auth import get_user_model


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
