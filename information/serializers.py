from rest_framework import serializers
from .models import (
    Specialist, TherapyCenter, News,
    SpecialistComment, TherapyCenterComment, NewsComment,
    InfoTag, NewsReply, SpecialistReply, TherapyCenterReply
)
from django.utils.timezone import localtime

class InfoTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoTag
        fields = ['id', 'name']

class SpecialistReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=SpecialistComment.objects.all(), required=False)  

    class Meta:
        model = SpecialistReply
        fields = ['id', 'user', 'content', 'created_at', 'parent']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return rep
    
class SpecialistCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = SpecialistReplySerializer(many=True, read_only=True)

    class Meta:
        model = SpecialistComment
        fields = [
            'id', 'user', 'content', 'rating',
            'created_at', 'updated_at', 'replies'
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return rep
    
    def get_replies(self, obj):
        return SpecialistReplySerializer(obj.replies.all(), many=True).data
    
class TherapyCenterReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=TherapyCenterComment.objects.all(), required=False)  

    class Meta:
        model = TherapyCenterReply
        fields = ['id', 'user', 'content', 'created_at', 'parent']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return rep
    
class TherapyCenterCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = TherapyCenterReplySerializer(many=True, read_only=True)

    class Meta:
        model = TherapyCenterComment
        fields = [
            'id', 'user', 'content', 'rating',
            'created_at', 'updated_at', 'replies'
        ]
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return rep
    
    def get_replies(self, obj):
        return TherapyCenterReplySerializer(obj.replies.all(), many=True).data
    
class NewsReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=NewsComment.objects.all(), required=False)  

    class Meta:
        model = NewsReply
        fields = ['id', 'user', 'content', 'created_at', 'parent']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return rep

class NewsCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = NewsReplySerializer(many=True, read_only=True)

    class Meta:
        model = NewsComment
        fields = [
            'id', 'user', 'content',
            'created_at', 'updated_at', 'replies'
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return rep
    
    def get_replies(self, obj):
        return NewsReplySerializer(obj.replies.all(), many=True).data

class SpecialistSerializer(serializers.ModelSerializer):
    tags = InfoTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=InfoTag.objects.all(), many=True, write_only=True, source='tags'
    )
    comments = SpecialistCommentSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = [
            'id', 'name', 'contact', 'description', 'photo',
            'tags', 'tag_ids',
            'created_at', 'comments', 'average_rating'
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()

class TherapyCenterSerializer(serializers.ModelSerializer):
    tags = InfoTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=InfoTag.objects.all(), many=True, write_only=True, source='tags'
    )
    comments = TherapyCenterCommentSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = TherapyCenter
        fields = [
            'id', 'name', 'description', 'address', 'photo',
            'tags', 'tag_ids',
            'created_at', 'comments', 'average_rating'
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()

class NewsSerializer(serializers.ModelSerializer):
    tags = InfoTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=InfoTag.objects.all(), many=True, write_only=True, source='tags'
    )
    comments = NewsCommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'photo',
            'tags', 'tag_ids',
            'created_at', 'comments', 'source'
        ]
