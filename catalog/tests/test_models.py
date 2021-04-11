from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from catalog.models import Photo

class PhotoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username = 'tester',
            email = 'tester@example.com',
            password = 'secret'
        )
        Photo.objects.create(
            author = user,
            tags = 'test image',
            photo = SimpleUploadedFile(
                name = 'test_image.jpg',
                content = open('catalog/tests/test_image.jpg', 'rb').read(),
                content_type = 'image/jpeg'
            )
        )

    def test_tags_label(self):
        photo = Photo.objects.get(id=1)
        field_label = photo._meta.get_field('tags').verbose_name
        self.assertEquals(field_label, 'tags')

    def test_tags_max_length(self):
        photo = Photo.objects.get(id=1)
        max_length = photo._meta.get_field('tags').max_length
        self.assertEquals(max_length, 200)

    def test_photo_as_str(self):
        photo = Photo.objects.get(id=1)
        string = str(photo)
        self.assertEquals(string, 'tester (test image)')

    def test_tags_as_list(self):
        photo = Photo.objects.get(id=1)
        tags = photo.tags_as_list()
        self.assertEquals(tags, ['test', 'image'])
