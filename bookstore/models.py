from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
# Create your models here.
now = timezone.now()


class Author(models.Model):
    fullname = models.CharField(max_length=40)

    def __str__(self):
        return self.fullname


class Book(models.Model):
    title = models.CharField(max_length=40)
    ISBN = models.CharField(max_length=13)
    publish_date = models.DateField(default=now)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.ManyToManyField(Author, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        if self.image:
            default_storage.delete(self.image.name)

class HttpRequest(models.Model):
    request_path = models.CharField(max_length=50)
    request_method = models.CharField(max_length=5)
    request_info = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)



class Logging(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    operation = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=20, blank=True)
