"""
Viewpoint of api/material
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from core.models import Material

from bom import serializers


class MaterialViewSet(viewsets.ModelViewSet):
    """Manage materials in the databse"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Material.objects.all()
    serializer_class = serializers.MaterialSerializer

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

    def get_queryset(self):
        """
        Overriding get queryset method.
        For returning queryset w.r.t queryparams passed in url.
        """
        queryset = self.queryset

        itemcode = self.request.query_params.get('code')
        name = self.request.query_params.get('name')
        categories = self.request.query_params.get('category')
        subcategories = self.request.query_params.get('scategory')
        isactive = self.request.query_params.get('active')

        if itemcode:
            queryset = queryset.filter(code__icontains=itemcode)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if categories:
            category = self._params_to_list(categories)
            queryset = queryset.filter(category__in=category)
        if subcategories:
            subcategory = self._params_to_list(subcategories)
            queryset = queryset.filter(subcategory__in=subcategory)
        if isactive:
            active = self._params_to_boolean(isactive)
            queryset = queryset.filter(active=active)

        return queryset
