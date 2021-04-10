from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Photo


class UploadPhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['photo', 'tags']


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
