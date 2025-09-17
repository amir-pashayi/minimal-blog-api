from rest_framework import serializers
from .models import Comment


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True, read_only=True)
    comment_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'post',
            'content',
            'created_at',
            'replies',
            'level',
            'parent',
            'comment_author',
        ]
        read_only_fields = ['id', 'created_at', 'replies', 'level', 'is_approved']

    def get_comment_author(self, obj):
        return obj.user.full_name or obj.user.username