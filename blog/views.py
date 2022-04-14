from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView

from .models import Post, Comment


class PostListView(ListView):
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now())


class PostDetailView(LoginRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = 'title', 'text'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class UserEditCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        author = self.model.objects.get(pk=pk).author
        if self.request.user != author:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(UserEditCheckMixin, UpdateView):
    model = Post
    fields = 'title', 'text'


class PostDeleteView(UserEditCheckMixin, DeleteView):
    model = Post


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = 'text',
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = Post.objects.get(pk=self.kwargs.get('pk'))
        self.object.approved = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs.get('pk')})


class CommentDeleteView(UserEditCheckMixin, DeleteView):
    model = Comment
