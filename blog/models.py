from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.author} --> {self.title}'

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'pk': self.pk})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def unpublish(self):
        self.published_date = None
        self.save()
