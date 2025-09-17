from rest_framework import serializers
from .models import Post
from accounts.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Post.objects.create(**validated_data)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'age', 'bio', 'email')


class AuthorPostsSerializer(serializers.Serializer):
    posts = PostSerializer(many=True)
    author = AuthorSerializer()