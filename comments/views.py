from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.throttling import ScopedRateThrottle
from .models import Comment
from posts.models import Post

class CommentView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "comment-create"

    def get_queryset(self):
        post_slug = self.kwargs.get('post_slug')
        post = get_object_or_404(Post, slug=post_slug)
        comments = Comment.objects.select_related('user').filter(post=post, is_approved=True)
        return comments

    def perform_create(self, serializer):
        post_slug = self.kwargs.get('post_slug')
        post = get_object_or_404(Post, slug=post_slug)
        serializer.save(user=self.request.user, post=post, is_approved=False)