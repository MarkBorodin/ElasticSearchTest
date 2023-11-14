import json

from django.http import HttpResponse, JsonResponse
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION, SUGGESTER_PHRASE, SUGGESTER_TERM, \
    LOOKUP_FILTER_TERMS, LOOKUP_FILTER_PREFIX, LOOKUP_FILTER_WILDCARD, LOOKUP_QUERY_EXCLUDE
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, FilteringFilterBackend, \
    SuggesterFilterBackend, OrderingFilterBackend, DefaultOrderingFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from elasticsearch import Elasticsearch
from rest_framework import generics

from search.documents import ArticleDocument, CategoryDocument
from articles.models import Article, Category
from search.serializers import ArticleSerializer, ArticleDocumentSerializer, CategorySerializer, \
    CategoryDocumentSerializer


from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    SUGGESTER_COMPLETION,
    LOOKUP_QUERY_CONTAINS
)


class ArticleView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDocumentView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleDocumentSerializer
    ordering = ('id',)
    lookup_field = 'id'

    filter_backends = [
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend   # This should be the last backend
    ]

    search_fields = (
        'title',
        'content',
    )

    filter_fields = {
        # 'category': 'category.id',
        'id': {
            'field': 'id',
            # Note, that we limit the lookups of id field in this example,
            # to `range`, `in`, `gt`, `gte`, `lt` and `lte` filters.
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'title': 'title.raw',
        'content': 'content.raw',
        'category': {
            'field': 'category.title',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }

    suggester_fields = {

        'title_term_or_phrase': {   # VERY IMPORTANT! THIS KEY WILL BE IN THE URL ADDRESS: .../search/articles/suggest/?title_term_or_phrase__phrase=...
            'field': 'title',
            'suggesters': [
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,

            ],
            'default_suggester': SUGGESTER_TERM,
            'options': {
                'size': 10,  # Number of suggestions to retrieve.
                'skip_duplicates': True,  # Whether duplicate suggestions should be filtered out.
            },
        },
        'title_completion': {   # VERY IMPORTANT! THIS KEY WILL BE IN THE URL ADDRESS: .../search/articles/suggest/?title_completion__completion=...
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'default_suggester': SUGGESTER_COMPLETION,
            'options': {
                'size': 10,  # Number of suggestions to retrieve.
                'skip_duplicates': True,  # Whether duplicate suggestions should be filtered out.
            },
        },

        'content_term_or_phrase': {   # VERY IMPORTANT! THIS KEY WILL BE IN THE URL ADDRESS: .../search/articles/suggest/?content_term_or_phrase__phrase=...
            'field': 'content',
            'suggesters': [
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,
            ],
            'default_suggester': SUGGESTER_TERM,
            'options': {
                'size': 10,  # Number of suggestions to retrieve.
                'skip_duplicates': True,  # Whether duplicate suggestions should be filtered out.
            },
        },
        'content_completion': {   # VERY IMPORTANT! THIS KEY WILL BE IN THE URL ADDRESS: .../search/articles/suggest/?content_completion__completion=...
            'field': 'content.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'default_suggester': SUGGESTER_COMPLETION,
            'options': {
                'size': 10,  # Number of suggestions to retrieve.
                'skip_duplicates': True,  # Whether duplicate suggestions should be filtered out.
            },
        },
    }


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDocumentView(DocumentViewSet):
    document = CategoryDocument
    serializer_class = CategoryDocumentSerializer

    filter_backends = [
        SearchFilterBackend,
        SuggesterFilterBackend
    ]

    search_fields = (
        'title',
        'content',
        'category_title'
    )

    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }
