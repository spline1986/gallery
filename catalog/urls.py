from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.PhotoListView.as_view(), name='index'),
    url(r'^tag/(?P<tag>.*)/$', views.PhotoListByTag.as_view(), name='by-tag'),
    url(r'^myphotos/$', views.PhotoListByUser.as_view(), name='by-user'),
    url(r'^upload/$', views.UploadPhoto.as_view(), name='upload-photo'),
    url(r'^register/$', views.SignUpView.as_view(), name='register'),
]
