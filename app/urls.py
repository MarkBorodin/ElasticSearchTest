from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from search import urls as search_urls
from search.views import ArticleView, ArticleDocumentView, CategoryView, CategoryDocumentView


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^search/', include(search_urls)),
]

# urlpatterns += router.urls
