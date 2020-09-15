from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import Color, Article, ArticleInfo


class ColorSerializer(serializers.ModelSerializer):
    """Serializer for the color objects"""

    class Meta:
        model = Color
        fields = ('id', 'name', 'code')
        read_only_fields = ('id',)


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the article objects"""

    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = ('id', 'artno', 'brand', 'style', 'items')
        read_only_fields = ('id', 'items')


class ArticleInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the article_info objects.
    Validator here used is determines the uniqueness of artid field,
    which is assigned from "perform_create" method in views
    """

    class Meta:
        model = ArticleInfo
        fields = (
                 'id', 'artid', 'article', 'color', 'category',
                 'price', 'active', 'basic', 'export'
        )
        read_only_fields = ('id', 'artid')
        validators = [
            UniqueTogetherValidator(
                queryset=ArticleInfo.objects.all(),
                fields=['article', 'color', 'category']
            )
        ]


class ArticleInfoDetailSerializer(ArticleInfoSerializer):
    """Serialize detailed view of article info"""
    article = serializers.StringRelatedField(read_only=True)
    color = serializers.StringRelatedField(read_only=True)


class ArticleDetailSerializer(ArticleSerializer):
    """Serialize detailed view of article"""
    items = ArticleInfoDetailSerializer(many=True)
