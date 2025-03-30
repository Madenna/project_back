from rest_framework import serializers
from .models import InfoPost, InfoComment, InfoTag, InfoCategory

class InfoTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoTag
        fields = ['id', 'name']
class InfoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoCategory
        fields = ['id', 'name']

class InfoCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = InfoComment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']

class InfoPostSerializer(serializers.ModelSerializer):
    photo = serializers.URLField(required=False, allow_null=True)
    category = InfoCategorySerializer()
    tags = InfoTagSerializer(many=True)
    comments = InfoCommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = InfoPost
        fields = ['id', 'title', 'content', 'category', 'tags', 'created_at', 'photo', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        return obj.liked_by.count()

# class InformationItemSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True)
#     comments = CommentSerializer(many=True, read_only=True)
#     average_rating = serializers.SerializerMethodField()

#     class Meta:
#         model = InformationItem
#         fields = ["id", "type", "title", "content", "image", "tags", "created_at", "comments", "average_rating"]

#     def get_average_rating(self, obj):
#         ratings = [comment.rating for comment in obj.comments.all()]
#         return round(sum(ratings) / len(ratings), 2) if ratings else None

#     def create(self, validated_data):
#         tags_data = validated_data.pop("tags", [])
#         item = InformationItem.objects.create(**validated_data)
#         for tag in tags_data:
#             tag_obj, _ = Tag.objects.get_or_create(name=tag["name"])
#             item.tags.add(tag_obj)
#         return item
