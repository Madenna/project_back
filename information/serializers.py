from rest_framework import serializers
from .models import InformationItem, Comment, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Comment
        fields = ["id", "user", "user_name", "content", "rating", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

class InformationItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = InformationItem
        fields = ["id", "type", "title", "content", "image", "tags", "created_at", "comments", "average_rating"]

    def get_average_rating(self, obj):
        ratings = [comment.rating for comment in obj.comments.all()]
        return round(sum(ratings) / len(ratings), 2) if ratings else None

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        item = InformationItem.objects.create(**validated_data)
        for tag in tags_data:
            tag_obj, _ = Tag.objects.get_or_create(name=tag["name"])
            item.tags.add(tag_obj)
        return item
