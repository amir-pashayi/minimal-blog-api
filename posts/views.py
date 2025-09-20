from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from .serializers import PostSerializer, AuthorPostsSerializer
from .models import Post, PostLike, Category
from accounts.models import User, UserBlock
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view



class MyPostsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return (
            Post.objects.filter(user=self.request.user)
            .annotate(
                comments_count=Count("comment", filter=Q(comment__is_approved=True), distinct=True),
                likes_count=Count("postlike", filter=Q(postlike__value="like"), distinct=True),
            )
            .select_related("user")
        )



@extend_schema_view(
    get=extend_schema(
        summary="List published posts (public)",
        tags=["posts"],
        responses={200: PostSerializer(many=True)},
        examples=[
            OpenApiExample(
                "List posts",
                description="Supports pagination & may include search/ordering filters if enabled.",
                request_only=True,
                value=None,
            ),
        ],
    ),
    post=extend_schema(
        summary="Create a post (requires auth)",
        tags=["posts"],
        request=PostSerializer,
        responses={
            201: PostSerializer,
            400: OpenApiExample("Bad Request", value={"detail": "validation error"}, response_only=True),
        },
        examples=[
            OpenApiExample(
                "Create post body",
                request_only=True,
                value={
                    "title": "My first post",
                    "description": "<p>Hello world</p>",
                    "status": "draft",
                    "reading_time": 3,
                    "categories": [1, 2],
                    "image": "binary file"
                },
            ),
        ],
    ),
)
class PostListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.filter(status="published")
        qs = qs.annotate(
            comments_count=Count("comment", filter=Q(comment__is_approved=True), distinct=True),
            likes_count=Count("postlike", filter=Q(postlike__value="like"), distinct=True),
        ).select_related("user")
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Post.objects.annotate(
            comments_count=Count("comment", filter=Q(comment__is_approved=True), distinct=True),
            likes_count=Count("postlike", filter=Q(postlike__value="like"), distinct=True),
        ).select_related("user")


@extend_schema(
    summary="List published posts by author username (public)",
    description="Supports search (title/description) and ordering (created_at/updated_at/comments_count/likes_count).",
    tags=["posts"],
    responses={200: PostSerializer(many=True), 404: None},
    examples=[
        OpenApiExample(
            "Example request",
            request_only=True,
            value=None,
            description="GET /authors/<username>/posts/?search=django&ordering=-updated_at",
        ),
    ],
)
class AuthorPostsAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "created_at", "comments_count", "likes_count"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        username = self.kwargs["username"]
        get_object_or_404(User, username=username)
        return (
            Post.objects.filter(user__username=username, status="published")
            .annotate(
                comments_count=Count("comment", filter=Q(comment__is_approved=True), distinct=True),
                likes_count=Count("postlike", filter=Q(postlike__value="like"), distinct=True),
            )
            .select_related("user")
        )


@extend_schema(
    summary="Like/Dislike a post (requires auth)",
    tags=["posts"],
    request=OpenApiExample(
        "Like/Dislike body",
        value={"value": "like"},
        description="value must be 'like' or 'dislike'",
    ),
    responses={
        201: OpenApiExample("Created", value={"message": "Like added"}, response_only=True),
        200: OpenApiExample("Updated/Already", value={"message": "Already liked"}, response_only=True),
        400: OpenApiExample("Invalid", value={"error": "Invalid value"}, response_only=True),
        403: OpenApiExample("Blocked", value={"error": "You cannot interact with this user."}, response_only=True),
        404: None,
    },
)
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "like"

    def post(self, request, slug):
        value = request.data.get('value')
        if value not in ['like', 'dislike']:
            return Response({'error': 'Invalid value'}, status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(Post, slug=slug, status="published")

        if UserBlock.objects.filter(user=post.user, blocked_user=request.user).exists() or UserBlock.objects.filter(user=request.user, blocked_user=post.user).exists():
            return Response({"error": "You cannot interact with this user."}, status=403)

        existing_like = PostLike.objects.filter(post=post, user=request.user).first()
        if existing_like:
            if existing_like.value == value:
                return Response({'message': f'Already {value}d'}, status=status.HTTP_200_OK)
            else:
                existing_like.value = value
                existing_like.save()
                return Response({'message': f'Updated to {value}'}, status=status.HTTP_200_OK)
        else:
            PostLike.objects.create(post=post, user=request.user, value=value)
            return Response({'message': f'{value.capitalize()} added'}, status=status.HTTP_201_CREATED)



@extend_schema(
    summary="List posts by category slug (public)",
    description="Supports search (title/description) and ordering (created_at/updated_at/comments_count/likes_count).",
    tags=["posts"],
    responses={200: PostSerializer(many=True), 404: None},
    examples=[
        OpenApiExample(
            "Example request",
            request_only=True,
            value=None,
            description="GET /categories/<slug>/posts/?search=python&ordering=-updated_at",
        ),
    ],
)
class CategoryPostsAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "created_at", "comments_count", "likes_count"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        slug = self.kwargs["slug"]
        get_object_or_404(Category, slug=slug)
        return (
            Post.objects.filter(categories__slug=slug, status="published")
            .annotate(
                comments_count=Count("comments", filter=Q(comments__is_approved=True), distinct=True),
                likes_count=Count("postlike", filter=Q(postlike__value="like"), distinct=True),
            )
            .select_related("user")
            .prefetch_related("categories")
        )
