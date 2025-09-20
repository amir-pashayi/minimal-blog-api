from rest_framework import serializers
from .models import User, Follow, Profile
import re

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('id', )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_phone(self, value):
        if not re.match(r'^09\d{9}$', value):
            raise serializers.ValidationError("شماره موبایل نامعتبر است.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["bio", "avatar", "location", "website"]