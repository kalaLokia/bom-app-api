"""
Viewpoint of the api/article
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Color, Article, ArticleInfo

from article import serializers


class ColorViewSet(viewsets.ModelViewSet):
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

    def _params_to_list(self, qs):
        """
        Convert comma seperated string to a list of strings.
        Also make sure no trailing, leading spaces ;-)
        """
        return [string.strip() for string in qs.split(',')]

    def get_queryset(self):
        """Overriding get queryset to order by id"""
        brands = self.request.query_params.get('brand')
        queryset = self.queryset
        if brands:
            brand_names = self._params_to_list(brands)
            queryset = queryset.filter(brand__in=brand_names)

        return queryset.order_by('-id')

    def perform_create(self, serializer):
        """Create a new article"""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer"""
        if self.action == 'retrieve':
            return serializers.ArticleDetailSerializer

        return self.serializer_class


class ArticleInfoViewSet(viewsets.ModelViewSet):
    """Manage article info in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ArticleInfo.objects.all()
    serializer_class = serializers.ArticleInfoSerializer

    def perform_create(self, serializer):
        """
        Create a new article in detail.
        assigns "created user", "arid" in the model where artid is unique
        """

        artno = serializer.validated_data.get('article').artno
        color = serializer.validated_data.get('color').code
        catgry = serializer.validated_data.get('category')
        artid = "-".join([artno, color, catgry])

        serializer.save(
            user=self.request.user,
            artid=artid
        )

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ArticleInfoDetailSerializer

        return self.serializer_class
