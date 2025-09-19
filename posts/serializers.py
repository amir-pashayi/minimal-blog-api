from rest_framework import serializers
from .models import Post
from accounts.models import User, Follow


class PostSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Post.objects.create(**validated_data)


class AuthorSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('full_name', 'age', 'bio', 'email')

    def get_followers_count(self, obj):
        return Follow.objects.filter(to_user=obj).count()

class AuthorPostsSerializer(serializers.Serializer):
    posts = PostSerializer(many=True)
    author = AuthorSerializer()