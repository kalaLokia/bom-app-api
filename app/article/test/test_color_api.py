"""
All Color model related tests are here.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Color

from article.serializers import ColorSerializer


COLOR_URL = reverse('article:color-list')


class PublicColorTests(TestCase):
    """Test the publically available colors api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving colos"""
        res = self.client.get(COLOR_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateColorTests(TestCase):
    """Test the authorized user color api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@kalalokia.xyz',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieving_colors(self):
        """Test retrieving colors"""
        Color.objects.create(user=self.user, name='black', code='bk')
        Color.objects.create(user=self.user, name='brown', code='br')

        res = self.client.get(COLOR_URL)

        colors = Color.objects.all().order_by('-name')
        serializer = ColorSerializer(colors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_color_success(self):
        """Test that creating a color is successful"""
        payload = {'name': 'brown', 'code': 'br'}
        self.client.post(COLOR_URL, payload)

        exists = Color.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_color_invalid(self):
        """Test creating a color with invalid payload"""
        payload = {'name': '', 'code': ''}
        res = self.client.post(COLOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
