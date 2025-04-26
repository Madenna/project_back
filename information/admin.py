from django.contrib import admin
from .models import (
    InfoTag, 
    Specialist, TherapyCenter, News,
    SpecialistComment, TherapyCenterComment, NewsComment
)

@admin.register(InfoTag)
class InfoTagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'display_average_rating']
    search_fields = ['name', 'description']
    filter_horizontal = ['tags']

    def display_average_rating(self, obj):
        return obj.average_rating()
    display_average_rating.short_description = 'Average Rating'

@admin.register(SpecialistComment)
class SpecialistCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialist', 'rating', 'created_at', 'parent']
    list_filter = ['created_at', 'rating']
    search_fields = ['content', 'user__full_name', 'specialist__name']
    raw_id_fields = ['specialist', 'user', 'parent']

@admin.register(TherapyCenter)
class TherapyCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'created_at', 'display_average_rating']
    search_fields = ['name', 'description', 'address']
    filter_horizontal = ['tags']

    def display_average_rating(self, obj):
        return obj.average_rating()
    display_average_rating.short_description = 'Average Rating'

@admin.register(TherapyCenterComment)
class TherapyCenterCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'center', 'rating', 'created_at', 'parent']
    list_filter = ['created_at', 'rating']
    search_fields = ['content', 'user__full_name', 'center__name']
    raw_id_fields = ['center', 'user', 'parent']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'content']
    filter_horizontal = ['tags']

@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'created_at', 'parent']
    list_filter = ['created_at']
    search_fields = ['content', 'user__full_name', 'news__title']
    raw_id_fields = ['news', 'user', 'parent']
