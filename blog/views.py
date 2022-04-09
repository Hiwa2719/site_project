from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import get_object_or_404


class PostListView(ListView):
    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')


class PostDetailView(DetailView):
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return get_object_or_404(Post.objects.filter(published_date__lte=timezone.now()), pk=self.kwargs.get('pk'))


class PostCreateView(CreateView):
    model = Post


class AboutView(TemplateView):
    pass
