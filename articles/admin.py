from django.contrib import admin

from articles.models import Article, Category

admin.site.register([Article, Category])
