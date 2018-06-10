from django.contrib import admin
from bookstore.models import Book, Author, Logging, HttpRequest

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Logging)
admin.site.register(HttpRequest)
# Register your models here.
