from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.throttling import ScopedRateThrottle
from .models import Comment, CommentReport
from posts.models import Post
from accounts.models import UserBlock
from rest_framework.exceptions import PermissionDenied
from . serializers import CommentReportSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(
    summary="Create comment",
    tags=["comments"],
    examples=[
        OpenApiExample(
            "Create comment",
            request_only=True,
            value={"content": "Nice post!"},
        ),
        OpenApiExample(
            "Created",
            response_only=True,
            value={"id": 123, "content": "Nice post!", "is_approved": False},
        ),
    ],
)
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
        blocked = UserBlock.objects.filter(user=post.user, blocked_user=self.request.user).exists() or UserBlock.objects.filter(user=self.request.user, blocked_user=post.user).exists()
        if blocked:
            raise PermissionDenied("You cannot interact with this user.")
        serializer.save(user=self.request.user, post=post, is_approved=False)


class ReportCommentView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "report"

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        ser_data = CommentReportSerializer(data=request.data)
        if ser_data.is_valid():
            obj, created = CommentReport.objects.get_or_create(
                comment=comment,
                reporter=request.user,
                defaults={"reason": ser_data.validated_data["reason"]},
            )
            if not created:
                obj.reason = ser_data.validated_data["reason"]
                obj.save(update_fields=["reason"])
                return Response({"message": "Report updated"}, status=status.HTTP_200_OK)
            return Response({"message": "Report submitted"}, status=status.HTTP_201_CREATED)