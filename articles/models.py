from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return self.title


class Article(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
