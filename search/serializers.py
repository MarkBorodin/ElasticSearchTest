from django.contrib.postgres.fields import IntegerRangeField
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from search.documents import ArticleDocument, CategoryDocument
from articles.models import Article, Category


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'category', 'content', 'id')


class ArticleDocumentSerializer(DocumentSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        document = ArticleDocument
        fields = ('title', 'category', 'content', 'popularity_counter', 'id')

    def get_id(self, obj):
        return obj.meta.id


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class CategoryDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CategoryDocument
        fields = ('title',)
