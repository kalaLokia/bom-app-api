"""
Url routing for the app: "material"
main url: host/api/material
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from material import views


router = DefaultRouter()
router.register('materials', views.MaterialViewSet)

app_name = 'material'

urlpatterns = [
    path('', include(router.urls))
]
