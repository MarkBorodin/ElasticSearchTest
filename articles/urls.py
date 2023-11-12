from django.urls import path, include, re_path
from search.views import ArticleDocumentView, ArticleView

app_name = 'articles'


urlpatterns = [
    path('articles/', ArticleView.as_view(), name='articles'),
]


