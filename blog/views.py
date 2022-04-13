from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(ListView):
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now())


class PostDetailView(DetailView):
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return get_object_or_404(Post.objects.filter(published_date__lte=timezone.now()), pk=self.kwargs.get('pk'))


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
