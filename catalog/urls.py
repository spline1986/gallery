from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.PhotoListView.as_view(), name='index'),
    url(r'^tag/(?P<tag>.*)/$', views.PhotoListByTag.as_view(), name='by-tag'),
    url(r'^myphotos/$', views.PhotoListByUser.as_view(), name='by-user'),
    url(r'^upload/$', views.UploadPhoto.as_view(), name='upload-photo'),
    url(r'^photo/(?P<pk>\d+)/update/$', views.UpdatePhoto.as_view(), name='update-photo'),
    url(r'^photo/(?P<pk>\d+)/delete/$', views.DeletePhoto.as_view(), name='delete-photo'),
    url(r'^register/$', views.SignUpView.as_view(), name='register'),
]
