from rest_framework import serializers

from core.models import Color, Article


class ColorSerializer(serializers.ModelSerializer):
    """Serializer for the color objects"""

    class Meta:
        model = Color
        fields = ('id', 'name', 'code')
        read_only_fields = ('id',)


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the article objects"""

    colors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Color.objects.all()
    )

    class Meta:
        model = Article
        fields = (
            'id', 'artno', 'brand', 'style', 'colors', 'category',
            'article_detail'
        )
        read_only_fields = ('id',)
