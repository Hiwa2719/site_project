from django.views.generic import ListView
from django.utils import timezone
from .models import Post, Comment


class PostListView(ListView):
    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
