from rest_framework import serializers
from .models import DiscussionPost, DiscussionCategory, Comment

class DiscussionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussionCategory
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Shows full_name of user

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']


class DiscussionPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    categories = DiscussionCategorySerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = DiscussionPost
        fields = ['id', 'user', 'title', 'content', 'created_at', 'categories', 'comments']

    def create(self, validated_data):
        request = self.context.get("request")
        categories_data = validated_data.pop('categories', [])
        post = DiscussionPost.objects.create(user=request.user, **validated_data)

        for cat_data in categories_data:
            category, _ = DiscussionCategory.objects.get_or_create(name=cat_data['name'])
            post.categories.add(category)

        return post
