from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import Color, Article, ArticleDetail


class ColorSerializer(serializers.ModelSerializer):
    """Serializer for the color objects"""

    class Meta:
        model = Color
        fields = ('id', 'name', 'code')
        read_only_fields = ('id',)


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the article objects"""

    details = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = ('id', 'artno', 'brand', 'style', 'details')
        read_only_fields = ('id',)


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the detailed article objects.
    Validator here used is determines the uniqueness of artid field,
    which is assigned from "perform_create" method in views
    """

    class Meta:
        model = ArticleDetail
        fields = (
                 'id', 'article', 'color', 'category',
                 'price', 'active', 'basic', 'export'
        )
        read_only_fields = ('id',)
        validators = [
            UniqueTogetherValidator(
                queryset=ArticleDetail.objects.all(),
                fields=['article', 'color', 'category']
            )
        ]
