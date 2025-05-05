from django.contrib import admin
from .models import DiscussionCategory, DiscussionPost, Comment, Reply

@admin.register(DiscussionCategory)
class DiscussionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(DiscussionPost)
class DiscussionPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__full_name', 'post__title']
    raw_id_fields = ['post', 'user']
    ordering = ['created_at']

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'parent', 'created_at']  
    list_filter = ['created_at']
    search_fields = ['content', 'user__full_name', 'parent__content']  
    raw_id_fields = ['parent', 'user']  
    ordering = ['created_at']

    def get_parent(self, obj):
        return obj.parent if obj.parent else None
    get_parent.short_description = 'Parent Comment'  
