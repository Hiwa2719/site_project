from django.urls import path
import views

app_name = 'blog'


urlpatterns = [
    path('', views.PostListView().as_view(), name='index'),
]
