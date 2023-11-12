from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl_drf.compat import KeywordField
from elasticsearch_dsl import analyzer

from articles.models import Article, Category


@registry.register_document
class ArticleDocument(Document):
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    content = fields.TextField(
        attr='content',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    category = fields.ObjectField(
        attr='category',
        properties={
            'id': fields.IntegerField(),
            'title': fields.KeywordField(
                attr='title',
                fields={
                    'raw': fields.TextField(),
                },
            )
        }
    )

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 1
    }

    class Index:
        name = 'articles'

    class Django:
        model = Article
        related_models = [Category]

    def get_queryset(self):
        return super(ArticleDocument, self).get_queryset().select_related(
            'category'
        )


@registry.register_document
class CategoryDocument(Document):
    title = fields.TextField(
        attr='title',
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    class Index:
        name = 'categories'

    class Django:
        model = Category
        related_models = [Article]
