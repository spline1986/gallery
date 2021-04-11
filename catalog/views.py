from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import UserRegistrationForm
from .models import Photo, User


class PhotoListView(generic.ListView):
    model = Photo
    paginate_by = 20
    ordering = ['-id']


class PhotoListByTag(generic.ListView):
    model = Photo
    template_name ='catalog/photo_by_tag.html'
    paginate_by = 20

    def get_queryset(self):
        return Photo.objects.filter(tags__icontains=self.kwargs['tag']).order_by('-id')


class PhotoListByUser(LoginRequiredMixin, generic.ListView):
    model = Photo
    template_name ='catalog/photo_by_user.html'
    paginate_by = 20

    def get_queryset(self):
        return Photo.objects.filter(author__exact=self.request.user).order_by('-id')


class UploadPhoto(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['photo', 'tags']
    success_url = '/'

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.author = User.objects.get(username=self.request.user)
        photo.save()
        return HttpResponseRedirect(self.success_url)


class UpdatePhoto(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['tags']
    template_name ='catalog/update_photo.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object.author, request.user)
        if self.object.author != request.user:
            return HttpResponseForbidden('Невозможно редактировать чужие изображения')
        return super().dispatch(request, *args, **kwargs)


class DeletePhoto(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseForbidden('Невозможно удалять чужие изображения')


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegistrationForm
    success_message = "Ваша учётная запись создана"
