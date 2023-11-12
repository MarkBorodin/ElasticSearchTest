from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter
from articles.views import *
from search.views import ArticleDocumentView, ArticleView

app_name = 'search'


router = ExtendedDefaultRouter()
router.register(r'articles', ArticleDocumentView, basename='article')


urlpatterns = [
    re_path(r'^', include(router.urls)),
]
