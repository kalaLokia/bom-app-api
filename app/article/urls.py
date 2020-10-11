"""
Url routing for the app: "article".
main url: host/api/article/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from article import views


router = DefaultRouter()
router.register('colors', views.ColorViewSet)
router.register('list', views.ArticleViewSet)
router.register('articles', views.ArticleInfoViewSet)

app_name = 'article'

urlpatterns = [
    path('', include(router.urls))
]
