from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


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
        return super().form_valid(form)


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
