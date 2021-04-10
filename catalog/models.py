from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from io import BytesIO
from .settings import THUMB_SIZE
import os.path


class Photo(models.Model):

    photo = models.ImageField(upload_to="static/%Y/%m/%d/")
    thumbnail = models.ImageField(upload_to="static/%Y/%m/%d/", editable=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.CharField(max_length=200, help_text="Введите теги через пробел")

    def __str__(self):
        return "{} ({})".format(self.author, self.tags)

    def save(self, *args, **kwargs):
        self.tags = self.tags.lower()
        if not self.make_thumbnail():
            raise Exception("Невозможно создать миниатюру")
        super(Photo, self).save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.photo)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + "_thumb" + thumb_extension

        if thumb_extension in [".jpg", ".jpeg"]:
            FTYPE = "JPEG"
        elif thumb_extension == ".gif":
            FTYPE = "GIF"
        elif thumb_extension == ".png":
            FTYPE = "PNG"
        else:
            return False

        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def tags_as_list(self):
        return self.tags.split(' ')
