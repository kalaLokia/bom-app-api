from rest_framework import serializers

from core.models import Color


class ColorSerializer(serializers.ModelSerializer):
    """Serializer for the color objects"""

    class Meta:
        model = Color
        fields = ('id', 'name', 'code')
        read_only_fields = ('id',)
