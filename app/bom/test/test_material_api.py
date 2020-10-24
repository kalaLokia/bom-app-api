"""
All Material model related tests are here.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Material

from bom.serializers import MaterialSerializer


MATERIAL_URL = reverse('bom:material-list')


def detail_url(material_id):
    """Returns the detailed view of a material"""
    return reverse('bom:material-detail', args=[material_id])


def sample_material(**params):
    """Create and return a sample material"""
    defaults = {
        'code': '5-co07-0002',
        'name': 'M40 Black',
        'category': 'component',
        'active': True,
    }
    defaults.update(params)

    return Material.objects.create(**defaults)


class PublicMaterialApiTests(TestCase):
    """Test unauthenticated material api access"""

    def setUp(self):
        self.client = APIClient()

    def test_unauth_access(self):
        """Test that authentication is required"""
        res = self.client.get(MATERIAL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMaterialApiTests(TestCase):
    """
    Test authenticated material requests
        * Retrieving list of material objects.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@kalalokia.xyz',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_materials(self):
        """Test retrieving a list of materials"""
        sample_material()
        sample_material(
            code='5-nl02-0002', name='Kashmirblack', category='rexin'
        )

        res = self.client.get(MATERIAL_URL)
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_material_success(self):
        """Test that creating a material is successful"""

        payload = {
            'code': '5-c09-0001',
            'name': 'pvc pipe 7mm',
            'category': 'component',
            'uom': 'meter'
        }
        self.client.post(MATERIAL_URL, payload)

        exists = Material.objects.filter(
            code=payload['code'],
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_material_duplicate_fail(self):
        """Test that creating material with same code is invalid"""
        sample_material()
        payload = {'code': '5-co07-0002', 'name': 'm40 black'}

        res = self.client.post(MATERIAL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_material_detail(self):
        """Test viewing material in detail #by id"""

        material = sample_material()
        res = self.client.get(detail_url(material.id))
        serializer = MaterialSerializer(material)

        self.assertEqual(res.data, serializer.data)


class FilterMaterialApiTest(TestCase):
    """
    Test filtering on Material model:
        * code       - contains
        * name       - contains
        * category   -
        * scategory  -
        * active     - boolean
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@kalalokia.xyz',
            'testpass'
        )
        self.client.force_authenticate(self.user)

        material1 = sample_material()
        material2 = sample_material(
            code='5-co07-0083',
            name='brown b9223',
            category='component',
            subcategory='thread',
            active=True
        )
        material3 = sample_material(
            code='5-co07-0006',
            name='m40 red',
            category='component',
            subcategory='thread',
            active=False
        )
        material4 = sample_material(
            code='5-co05-0432',
            name='n blue red tape',
            category='component',
            subcategory='tape',
            active=False
        )
        material5 = sample_material(
            code='5-nl02-0190',
            name='a 0069 rj1 1.45mm',
            category='rexin',
            subcategory='non pasted',
            active=True
        )
        self.serializer1 = MaterialSerializer(material1)
        self.serializer2 = MaterialSerializer(material2)
        self.serializer3 = MaterialSerializer(material3)
        self.serializer4 = MaterialSerializer(material4)
        self.serializer5 = MaterialSerializer(material5)

    def test_filter_code(self):
        """Test filter material by item code"""
        res = self.client.get(
            MATERIAL_URL,
            {'code': '5-co07'}
        )

        self.assertIn(self.serializer1.data, res.data)
        self.assertIn(self.serializer2.data, res.data)
        self.assertIn(self.serializer3.data, res.data)
        self.assertNotIn(self.serializer4.data, res.data)
        self.assertNotIn(self.serializer5.data, res.data)

    def test_filter_name(self):
        """Test filter material by name"""
        res = self.client.get(
            MATERIAL_URL,
            {'name': 'red'}
        )
        self.assertNotIn(self.serializer1.data, res.data)
        self.assertNotIn(self.serializer2.data, res.data)
        self.assertIn(self.serializer3.data, res.data)
        self.assertIn(self.serializer4.data, res.data)
        self.assertNotIn(self.serializer5.data, res.data)

    def test_filter_category(self):
        """Test filter material by category"""
        res = self.client.get(
            MATERIAL_URL,
            {'category': 'component'}
        )
        self.assertIn(self.serializer1.data, res.data)
        self.assertIn(self.serializer2.data, res.data)
        self.assertIn(self.serializer3.data, res.data)
        self.assertIn(self.serializer4.data, res.data)
        self.assertNotIn(self.serializer5.data, res.data)

    def test_filter_subcategory(self):
        """Test filter material by subcategory"""
        res = self.client.get(
            MATERIAL_URL,
            {'scategory': 'non pasted, tape'}
        )
        self.assertNotIn(self.serializer1.data, res.data)
        self.assertNotIn(self.serializer2.data, res.data)
        self.assertNotIn(self.serializer3.data, res.data)
        self.assertIn(self.serializer4.data, res.data)
        self.assertIn(self.serializer5.data, res.data)

    def test_filter_active(self):
        """Test filter material by active or not"""
        res = self.client.get(
            MATERIAL_URL,
            {'active': 'true'}
        )
        self.assertIn(self.serializer1.data, res.data)
        self.assertIn(self.serializer2.data, res.data)
        self.assertNotIn(self.serializer3.data, res.data)
        self.assertNotIn(self.serializer4.data, res.data)
        self.assertIn(self.serializer5.data, res.data)

    def test_filter_invalid_boolean(self):
        """Test invalid boolean value in queryparams fails"""

        res1 = self.client.get(
            MATERIAL_URL,
            {'active': 'false or true'}
        )
        res2 = self.client.get(
            MATERIAL_URL,
            {'active': '1 '}
        )
        res3 = self.client.get(
            MATERIAL_URL,
            {'active': 'tape'}
        )
        res4 = self.client.get(
            MATERIAL_URL,
            {'active': 'none'}
        )

        self.assertEqual(res1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res3.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res4.status_code, status.HTTP_200_OK)
