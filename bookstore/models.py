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
    thumbnail = models.ImageField(blank=True, upload_to='thumbnail/')

    __original_image = None

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def __str__(self):
        return self.title

    def create_thumbnail(self):
        from PIL import Image
        from io import BytesIO
        from stars_task.settings import THUMB_SIZE
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os
        import random, string

        thumb_extension = os.path.splitext(self.image.name)[1].lower()
        if thumb_extension in ['.jpg', '.jpeg']:
            PIL_TYPE = 'JPEG'
        elif thumb_extension == '.gif':
            PIL_TYPE = 'GIF'
        elif thumb_extension == '.png':
            PIL_TYPE = 'PNG'

        img = Image.open(BytesIO(self.image.read()))
        img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        tmp_handle = BytesIO()
        img.save(tmp_handle, PIL_TYPE)
        tmp_handle.seek(0)
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], tmp_handle.read())
        thumb_name = '%s_thumbnail%s' % (os.path.splitext(suf.name)[0], thumb_extension)
        thumb_path = '{}/{}'.format('thumbnail', thumb_name)
        if default_storage.exists(thumb_path):
            random_choice = lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)])
            random_str = random_choice(4)
            thumb_name = '%s_thumbnail_%s%s' % (os.path.splitext(suf.name)[0], random_str, thumb_extension)
        self.thumbnail.save(
            thumb_name,
            # '%s_thumbnail%s' % (os.path.splitext(suf.name)[0], thumb_extension),
            suf, save=False
        )
        self.image = self.thumbnail

    def save(self, *args, **kwargs):
        # Make thumbnail only if photo field was changed
        if self.image != self.__original_image:
            self.create_thumbnail()
        super(Book, self).save()
        pass


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
