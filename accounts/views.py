from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, FollowSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Follow, User
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"


class UserRegisterView(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollow(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, username):
        ser_data = FollowSerializer(data=request.data)
        if ser_data.is_valid():
            to_user = get_object_or_404(User, username=username)
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