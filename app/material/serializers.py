"""
Serializer for api/material
"""
from rest_framework import serializers

from core.models import Material


class MaterialSerializer(serializers.ModelSerializer):
    """Serializer for the Material model"""

    class Meta:
        model = Material
        fields = (
            'id', 'code', 'name', 'category', 'subcategory',
            'uom', 'purchaseuom', 'cf', 'price', 'active'
        )
        read_only_fields = ('id',)
