from rest_framework import serializers

from core.models import Color, Article, ArticleDetail


class ColorSerializer(serializers.ModelSerializer):
    """Serializer for the color objects"""

    class Meta:
        model = Color
        fields = ('id', 'name', 'code')
        read_only_fields = ('id',)


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Serializer for the detailed article objects"""

    class Meta:
        model = ArticleDetail
        fields = (
                 'id', 'article', 'color', 'category',
                 'price', 'active', 'artid', 'basic', 'export'
        )
        read_only_fields = ('id',)


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the article objects"""

    details = ArticleDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('id', 'artno', 'brand', 'style', 'details')
        read_only_fields = ('id',)
