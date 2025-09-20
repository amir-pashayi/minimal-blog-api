from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from django.conf import settings

urlpatterns = [
    path("my-posts/", views.MyPostsListAPIView.as_view(), name="my-posts"),
    path("author/<str:username>/", views.AuthorPostsAPIView.as_view(), name="author-posts"),
    path("category/<slug:slug>/", cache_page(settings.CACHE_TTL)(views.CategoryPostsAPIView.as_view()), name="category-posts"),
    path("<slug:slug>/like/", views.LikePostView.as_view(), name="post-like"),
    path("", cache_page(settings.CACHE_TTL)(views.PostListCreateAPIView.as_view()), name="post-list-create"),
    path("<slug:slug>/", views.PostDetailAPIView.as_view(), name="post-detail"),

]

