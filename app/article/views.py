"""
Viewpoint of the api/article
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from core.models import Color, Article, ArticleInfo, categorize

from article import serializers


# TODO make staff only access for writting

class ColorViewSet(viewsets.ModelViewSet):
    """Manage colors in the database"""
    authentication_classes = (TokenAuthentication,)
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
        return [string.strip().lower() for string in qs.split(',')]

    def get_queryset(self):
        """Overriding get queryset to order by id"""
        queryset = self.queryset

        brands = self.request.query_params.get('brand')
        styles = self.request.query_params.get('style')
        colors = self.request.query_params.get('color')
        cateogories = self.request.query_params.get('category')

        if brands:
            brand_names = self._params_to_list(brands)
            queryset = queryset.filter(brand__in=brand_names)
        if styles:
            style_names = self._params_to_list(styles)
            queryset = queryset.filter(style__in=style_names)
        if colors:
            color_codes = self._params_to_list(colors)
            queryset = queryset.filter(items__color__code__in=color_codes)
        if cateogories:
            mcategory = self._params_to_list(cateogories)
            queryset = queryset.filter(items__mcategory__in=mcategory)

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

    def _params_to_list(self, qs):
        """
        Convert comma seperated string to a list of strings.
        Also make sure no trailing, leading spaces ;-)
        """
        return [string.strip().lower() for string in qs.split(',')]

    def _params_to_boolean(self, qs):
        """
        Returns True or False for valid data, or raises 404
        """
        value = qs.strip().lower()

        if value in ['true', 't', '1', 'one']:
            return True
        elif value in ['false', 'f', '0', 'none', 'zero']:
            return False
        else:
            raise Http404("Something went wrong")
        # return False

    def get_queryset(self):
        """
        Overriding get queryset method.
        For returning queryset w.r.t queryparams passed in the url
        """
        queryset = self.queryset

        articlenos = self.request.query_params.get('artno')
        brands = self.request.query_params.get('brand')
        styles = self.request.query_params.get('style')
        colors = self.request.query_params.get('color')
        categories = self.request.query_params.get('category')
        isactive = self.request.query_params.get('active')
        isexport = self.request.query_params.get('export')

        if articlenos:
            artnos = self._params_to_list(articlenos)
            queryset = queryset.filter(article__artno__in=artnos)
        if brands:
            brand = self._params_to_list(brands)
            queryset = queryset.filter(article__brand__in=brand)
        if styles:
            style = self._params_to_list(styles)
            queryset = queryset.filter(article__style__in=style)
        if colors:
            color = self._params_to_list(colors)
            if len(color[0]) == 2:
                queryset = queryset.filter(color__code__in=color)
            else:
                queryset = queryset.filter(color__name__in=color)
        if categories:
            category = self._params_to_list(categories)
            queryset = queryset.filter(category__in=category)

        if isactive:
            active = self._params_to_boolean(isactive)
            queryset = queryset.filter(active=active)
        if isexport:
            export = self._params_to_boolean(isexport)
            queryset = queryset.filter(export=export)

        return queryset

    def perform_create(self, serializer):
        """
        Overriding perform_create #creates a model object,
        to set values for "created user", "arid" in the model.
        """

        artno = serializer.validated_data.get('article').artno
        color = serializer.validated_data.get('color').code
        catgry = serializer.validated_data.get('category')
        artid = f"{artno}-{color}-{catgry}"

        serializer.save(
            user=self.request.user,
            artid=artid,
            mcategory=categorize(value=catgry)
        )

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ArticleInfoDetailSerializer

        return self.serializer_class
