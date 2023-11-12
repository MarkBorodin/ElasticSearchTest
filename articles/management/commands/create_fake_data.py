from django.core.management.base import BaseCommand
from faker import Faker

from articles.models import Category, Article


class Command(BaseCommand):
    help = 'Populate the database with fake data'
    genres = [
        'Fiction',
        'Mystery',
        'Romance',
        'Science Fiction',
        'Fantasy',
        'Biography',
        'History',
        'Self-Help',
        'Thriller',
        'Drama',
    ]

    def handle(self, *args, **kwargs):
        fake = Faker()

        for category_title in self.genres:
            Category.objects.get_or_create(title=category_title)

        for _ in range(150):
            category = Category.objects.order_by('?').first()
            try:
                title = fake.sentence()
                content = fake.paragraph()
            except UnicodeDecodeError:
                title = 'Title with invalid characters'
                content = 'Content with invalid characters'
            Article.objects.create(
                title=title,
                content=content,
                category=category
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data.'))
