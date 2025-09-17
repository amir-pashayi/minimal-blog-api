from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from .serializers import PostSerializer, AuthorPostsSerializer
from .models import Post
from accounts.models import User


class PostListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.annotate(
            comments_count=Count('comment', filter=Q(comment__is_approved=True))
        ).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class AuthorPostsAPIView(APIView):
    permission_classes = [AllowAny]
    filter_backends = (SearchFilter, OrderingFilter)
    filterset_fields = ['updated_at']
    search_fields = ['title', 'excerpt']

    def get(self, request, username):
        try:
            author = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('User Does Not Exists', status=status.HTTP_400_BAD_REQUEST)

        posts = Post.objects.filter(user__username=username, status='published').annotate(
            comments_count=Count('comment', filter=Q(comment__is_approved=True)))

        for backend in self.filter_backends:
            posts = backend().filter_queryset(request, posts, self)

        paginator = PageNumberPagination()
        paginated_posts = paginator.paginate_queryset(posts, request, view=self)

        data = {
            'posts': paginated_posts,
            'author': author
        }
        ser_data = AuthorPostsSerializer(instance=data)
        return Response(ser_data.data, status=status.HTTP_200_OK)