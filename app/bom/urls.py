"""
Url routing for the app: "bom"
main url: host/api/bom
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bom import views


router = DefaultRouter()
router.register('materials', views.MaterialViewSet)

app_name = 'bom'

urlpatterns = [
    path('', include(router.urls))
]
