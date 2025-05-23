from rest_framework import serializers
from .models import DiscussionPost, DiscussionCategory, Comment, Reply
from django.utils.timezone import localtime

class DiscussionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussionCategory
        fields = ['id', 'name']

class ReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)  

    class Meta:
        model = Reply
        fields = ['id', 'user', 'content', 'created_at', 'likes_count', 'parent']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return rep

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies = ReplySerializer(many=True, read_only=True)  # Replies for comment

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'likes_count', 'replies']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return rep
    
    def get_replies(self, obj):
        return ReplySerializer(obj.replies.all(), many=True).data
    
class DiscussionPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=DiscussionCategory.objects.all()
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = DiscussionPost
        fields = ['id', 'user', 'title', 'content', 'created_at', 'category', 'comments']

    def create(self, validated_data):
        request = self.context.get("request")
        return DiscussionPost.objects.create(user=request.user, **validated_data)

