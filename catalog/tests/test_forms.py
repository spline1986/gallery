from django.test import TestCase
from catalog.forms import UploadPhotoForm, UserRegistrationForm


class UploadPhotoFormTest(TestCase):

    def test_upload_form_photo_field_label(self):
        form = UploadPhotoForm()
        self.assertTrue(form.fields['photo'].label == None or form.fields['photo'].label == 'Photo')

    def test_upload_form_tags_field_label(self):
        form = UploadPhotoForm()
        self.assertTrue(form.fields['tags'].label == None or form.fields['tags'].label == 'Tags')

    def test_upload_form_tags_field_help_text(self):
        form = UploadPhotoForm()
        self.assertEqual(form.fields['tags'].help_text, 'Введите теги через пробел')
