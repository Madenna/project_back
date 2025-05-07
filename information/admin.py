from django.contrib import admin
from .models import (
    InfoTag, Specialist, TherapyCenter, News,
    SpecialistComment, SpecialistReply, TherapyCenterComment,
    TherapyCenterReply, NewsComment, NewsReply
)
from django.utils.html import format_html


# Customizing admin for SpecialistComment, SpecialistReply, etc.

class SpecialistCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialist', 'content', 'rating', 'created_at', 'updated_at']
    list_filter = ['specialist', 'created_at']
    search_fields = ['user__username', 'specialist__name']


class SpecialistReplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'parent', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'parent__content']

    def parent(self, obj):
        return obj.parent  # This will show the parent comment if it exists
    parent.short_description = 'Parent Comment'


class TherapyCenterCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'center', 'content', 'rating', 'created_at', 'updated_at']
    list_filter = ['center', 'created_at']
    search_fields = ['user__username', 'center__name']


class TherapyCenterReplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'parent', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'parent__content']

    def parent(self, obj):
        return obj.parent  # This will show the parent comment if it exists
    parent.short_description = 'Parent Comment'


class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'content', 'created_at', 'updated_at']
    list_filter = ['news', 'created_at']
    search_fields = ['user__username', 'news__title']


class NewsReplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'parent', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'parent__content']

    def parent(self, obj):
        return obj.parent  # This will show the parent comment if it exists
    parent.short_description = 'Parent Comment'


# Admin for other models
class InfoTagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class SpecialistAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'created_at', 'average_rating']
    search_fields = ['name', 'contact']
    list_filter = ['created_at']

class TherapyCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'created_at', 'average_rating']
    search_fields = ['name', 'address']
    list_filter = ['created_at']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'source']
    search_fields = ['title', 'content']
    list_filter = ['created_at']


# Register the models with their custom admin classes
admin.site.register(InfoTag, InfoTagAdmin)
admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(TherapyCenter, TherapyCenterAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(SpecialistComment, SpecialistCommentAdmin)
admin.site.register(SpecialistReply, SpecialistReplyAdmin)
admin.site.register(TherapyCenterComment, TherapyCenterCommentAdmin)
admin.site.register(TherapyCenterReply, TherapyCenterReplyAdmin)
admin.site.register(NewsComment, NewsCommentAdmin)
admin.site.register(NewsReply, NewsReplyAdmin)