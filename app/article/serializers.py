from rest_framework import serializers

from core.models import Color, Article, ArticleDetail


class ColorSerializer(serializers.ModelSerializer):
    """Serializer for the color objects"""

    class Meta:
        model = Color
        fields = ('id', 'name', 'code')
        read_only_fields = ('id',)


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the detailed article objects.
    artid field is hidden from view
    """

    class Meta:
        model = ArticleDetail
        fields = (
                 'id', 'artid', 'article', 'color', 'category',
                 'price', 'active', 'basic', 'export'
        )
        read_only_fields = ('id',)

        # artid = serializers.SerializerMethodField('get_article_id')

        # def get_article_id(self, obj):
        #     """Getting article id from provided fields"""
        #     artno = obj.article.artno
        #     color = obj.color.code
        #     category = obj.category
        #     return f"{artno}-{color}-{category}"


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the article objects"""

    details = ArticleDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('id', 'artno', 'brand', 'style', 'details')
        read_only_fields = ('id',)
