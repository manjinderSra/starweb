from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField( max_length=50)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField( max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField( max_length=50)
    slug = models.CharField( max_length=250)
    description = models.TextField()
    author = models.CharField( max_length=50)
    image = models.ImageField(upload_to='image')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

