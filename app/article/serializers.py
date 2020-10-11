"""
Serializers for api/article
"""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import Color, Article, ArticleInfo, categorize


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

    def update(self, instance, validated_data):
        """
        Update a article, also updates the artid if exists.
        If artno number is new, artid in ArticleInfo will also be updated.
        """
        if str(instance) != validated_data['artno']:
            article_infos = instance.items.all()
            newartno = validated_data['artno']

            for i in article_infos:
                newartid = '-'.join([newartno] + str(i).split('-')[1:])
                i.artid = newartid
                i.save()

        article = super().update(instance, validated_data)
        return article


class ArticleInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the article_info objects.
    Validator here used is determines the uniqueness of artid field,
    which is assigned from "perform_create" method in views
    """

    class Meta:
        model = ArticleInfo
        fields = (
            'id', 'artid', 'article', 'color', 'category', 'mcategory',
            'price', 'active', 'basic', 'export'
        )
        read_only_fields = ('id', 'artid', 'mcategory')
        validators = [
            UniqueTogetherValidator(
                queryset=ArticleInfo.objects.all(),
                fields=['article', 'color', 'category']
            )
        ]

    def update(self, instance, validated_data):
        """
        Update ArticleInfo with updated artid
        """
        artno = validated_data['article'].artno
        color = validated_data['color'].code
        category = validated_data['category']
        validated_data['artid'] = '-'.join([artno, color, category])
        validated_data['mcategory'] = categorize(value=category)

        article_info = super().update(instance, validated_data)
        return article_info


class ArticleInfoDetailSerializer(ArticleInfoSerializer):
    """Serialize detailed view of article info"""
    article = serializers.StringRelatedField(read_only=True)
    color = serializers.StringRelatedField(read_only=True)


class ArticleDetailSerializer(ArticleSerializer):
    """Serialize detailed view of article"""
    items = ArticleInfoDetailSerializer(many=True)
