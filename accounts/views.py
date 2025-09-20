from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, FollowSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Follow, User, Profile, UserBlock
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view



@extend_schema(
    summary="Login (JWT)",
    description="Obtain access/refresh tokens with phone and password.",
    examples=[
        OpenApiExample(
            "Login request",
            request_only=True,
            value={"phone": "09120000000", "password": "Passw0rd!"},
        ),
        OpenApiExample(
            "Login response",
            response_only=True,
            value={"access": "<jwt>", "refresh": "<jwt>"},
        ),
    ],
    tags=["auth"],
)
class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"



@extend_schema(
    summary="Register a new user",
    description="Create a new user account using phone, username, password and other optional fields.",
    tags=["auth"],
    request=OpenApiExample(
        "Register body",
        value={
            "phone": "09120000000",
            "username": "alice",
            "full_name": "Alice Example",
            "password": "Passw0rd!",
            "age": 25,
            "gender": "female",
            "email": "alice@example.com"
        },
    ),
    responses={
        201: OpenApiExample(
            "User created",
            value={
                "phone": "09120000000",
                "username": "alice",
                "full_name": "Alice Example",
                "age": 25,
                "gender": "female",
                "email": "alice@example.com",
                "bio": None,
            },
            response_only=True,
        ),
        400: OpenApiExample(
            "Validation error",
            value={"phone": ["شماره موبایل نامعتبر است."]},
            response_only=True,
        ),
    },
)
class UserRegisterView(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema_view(
    post=extend_schema(
        summary="Follow a user",
        tags=["social"],
        request=OpenApiExample(
            "Follow body (optional data)",
            value={},
        ),
        responses={
            201: OpenApiExample("Followed", value={"from_user": 1, "to_user": 2}, response_only=True),
            403: OpenApiExample("Blocked", value={"error": "Interaction not allowed"}, response_only=True),
            404: None,
        },
    ),
    delete=extend_schema(
        summary="Unfollow a user",
        tags=["social"],
        responses={
            204: OpenApiExample("Unfollowed", value={"message": "Unfollowed successfully"}, response_only=True),
            400: OpenApiExample("Not following", value={"error": "Not following this user"}, response_only=True),
            404: None,
        },
    ),
)
class UserFollow(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, username):

        ser_data = FollowSerializer(data=request.data)
        if ser_data.is_valid():
            to_user = get_object_or_404(User, username=username)

            if UserBlock.objects.filter(user=to_user, blocked_user=request.user).exists() or UserBlock.objects.filter(user=request.user, blocked_user=to_user).exists():
                return Response({"error": "Interaction not allowed"}, status=403)

            ser_data.save(from_user=request.user, to_user=to_user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        to_user = get_object_or_404(User, username=username)
        follow = Follow.objects.filter(from_user=request.user, to_user=to_user).first()
        if not follow:
            return Response({'error': 'Not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)


class MyProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class ProfileView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    lookup_field = "user__username"
    lookup_url_kwarg = "username"

    def get_object(self):
        username = self.kwargs[self.lookup_url_kwarg]
        return get_object_or_404(Profile, user__username=username)


@extend_schema_view(
    post=extend_schema(
        summary="Block a user",
        tags=["moderation"],
        responses={
            201: OpenApiExample("Blocked", value={"message": "Blocked bob"}, response_only=True),
            400: OpenApiExample("Invalid", value={"error": "Cannot block yourself"}, response_only=True),
            404: None,
        },
    ),
    delete=extend_schema(
        summary="Unblock a user",
        tags=["moderation"],
        responses={
            200: OpenApiExample("Unblocked", value={"message": "Unblocked bob"}, response_only=True),
            404: None,
        },
    ),
)

class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        if target == request.user:
            return Response({"error": "Cannot block yourself"}, status=status.HTTP_400_BAD_REQUEST)
        UserBlock.objects.get_or_create(user=request.user, blocked_user=target)
        return Response({"message": f"Blocked {username}"}, status=status.HTTP_201_CREATED)

    def delete(self, request, username):
        target = get_object_or_404(User, username=username)
        UserBlock.objects.filter(user=request.user, blocked_user=target).delete()
        return Response({"message": f"Unblocked {username}"}, status=status.HTTP_200_OK)