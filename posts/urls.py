from django.urls import path
from . import views

urlpatterns = [
    path("my-posts/", views.MyPostsListAPIView.as_view(), name="my-posts"),
    path("", views.PostListCreateAPIView.as_view(), name="post-list-create"),
    path("<slug:slug>/", views.PostDetailAPIView.as_view(), name="post-detail"),
    path("posts/<slug:slug>/like/", views.LikePostView.as_view(), name="post-like"),
    path('author/<str:username>/', views.AuthorPostsAPIView.as_view(), name='author-posts'),
    path("category/<slug:slug>/", views.CategoryPostsAPIView.as_view(), name="category-posts"),

]

