from django.contrib import admin
from .models import (
    InfoTag, Specialist, TherapyCenter, News,
    SpecialistComment, SpecialistReply, TherapyCenterComment, TherapyCenterReply, NewsComment, NewsReply
)

# InfoTag Admin
@admin.register(InfoTag)
class InfoTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Specialist Admin
@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'created_at', 'average_rating')  
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'tags')
    ordering = ('-created_at',)

# TherapyCenter Admin
@admin.register(TherapyCenter)
class TherapyCenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'created_at', 'average_rating')  
    search_fields = ('name', 'description', 'address')
    list_filter = ('created_at', 'tags')
    ordering = ('-created_at',)

# News Admin
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'source')
    search_fields = ('title', 'content', 'source')
    list_filter = ('created_at', 'tags')
    ordering = ('-created_at',)

# SpecialistComment Admin
@admin.register(SpecialistComment)
class SpecialistCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'specialist', 'user', 'content', 'created_at', 'rating', 'parent')  
    search_fields = ('content', 'user__username')
    list_filter = ('created_at', 'specialist', 'rating')
    ordering = ('-created_at',)

# SpecialistReply Admin
@admin.register(SpecialistReply)
class SpecialistReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_content', 'user', 'content', 'created_at')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at', 'parent__specialist')
    ordering = ('-created_at',)

    def comment_content(self, obj):
        return obj.parent.content 

# TherapyCenterComment Admin
@admin.register(TherapyCenterComment)
class TherapyCenterCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'center', 'user', 'content', 'created_at', 'rating', 'parent')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at', 'center', 'rating')
    ordering = ('-created_at',)

# TherapyCenterReply Admin
@admin.register(TherapyCenterReply)
class TherapyCenterReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_content', 'user', 'content', 'created_at')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at', 'parent__center')
    ordering = ('-created_at',)

    def comment_content(self, obj):
        return obj.parent.content  

# NewsComment Admin
@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'user', 'content', 'created_at', 'parent')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at', 'news')
    ordering = ('-created_at',)

# NewsReply Admin
@admin.register(NewsReply)
class NewsReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_content', 'user', 'content', 'created_at')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at', 'parent__news')
    ordering = ('-created_at',)

    def comment_content(self, obj):
        return obj.parent.content  
