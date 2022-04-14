from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('comment/', include([
        path('create/<int:pk>/', views.CommentCreateView.as_view(), name='comment_create'),
        path('delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
    ])),
    path('post/', include([
        path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
        path('create/', views.PostCreateView.as_view(), name='post_create'),
        path('update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
        path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
        path('mine/', views.MyPosts.as_view(), name='my_posts'),
    ])),
    path('about/', views.AboutView.as_view(), name='about'),
]
