from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('my-posts/', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('author/<str:username>/', views.AuthorPostsAPIView.as_view(), name='author-posts')

]

