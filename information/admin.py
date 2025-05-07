from django.contrib import admin
from .models import (
    Specialist, TherapyCenter, News,
    SpecialistComment, TherapyCenterComment, NewsComment,
    SpecialistReply, TherapyCenterReply, NewsReply
)

# Specialist Admin
@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

# TherapyCenter Admin
@admin.register(TherapyCenter)
class TherapyCenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name', 'address')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

# News Admin
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

# SpecialistComment Admin
@admin.register(SpecialistComment)
class SpecialistCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'specialist', 'user', 'content', 'created_at', 'parent')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at', 'specialist')
    ordering = ('-created_at',)

# TherapyCenterComment Admin
@admin.register(TherapyCenterComment)
class TherapyCenterCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'therapy_center', 'user', 'content', 'created_at', 'parent')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at', 'therapy_center')
    ordering = ('-created_at',)

# NewsComment Admin
@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'user', 'content', 'created_at', 'parent')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at', 'news')
    ordering = ('-created_at',)

# SpecialistReply Admin
@admin.register(SpecialistReply)
class SpecialistReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at', 'comment')
    ordering = ('-created_at',)

# TherapyCenterReply Admin
@admin.register(TherapyCenterReply)
class TherapyCenterReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at', 'comment')
    ordering = ('-created_at',)

# NewsReply Admin
@admin.register(NewsReply)
class NewsReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at', 'comment')
    ordering = ('-created_at',)
