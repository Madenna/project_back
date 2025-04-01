from django.contrib import admin
from .models import DiscussionCategory, DiscussionPost, Comment

@admin.register(DiscussionCategory)
class DiscussionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(DiscussionPost)
class DiscussionPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at', 'parent']
    list_filter = ['created_at']
    search_fields = ['content', 'user__full_name', 'post__title']
    raw_id_fields = ['post', 'user', 'parent']
