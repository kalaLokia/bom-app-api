from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Color, Article

from article import serializers


class ColorViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    """Manage colors in the database"""
    authentication_classes = (TokenAuthentication,)
    # TODO make staff only access
    permission_classes = (IsAuthenticated,)
    queryset = Color.objects.all()
    serializer_class = serializers.ColorSerializer

    def get_queryset(self):
        """Overriding get queryset to order by name"""
        return self.queryset.order_by('-name')

    def perform_create(self, serializer):
        """Create a new color"""
        serializer.save(user=self.request.user)


class ArticleViewSet(viewsets.ModelViewSet):
    """Manage articles in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer

    def get_queryset(self):
        """Overriding get queryset to order by id"""
        return self.queryset.order_by('-id')
