from django.contrib import admin
from .models import InfoTag, InfoCategory, InfoPost, InfoComment

@admin.register(InfoTag)
class InfoTagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(InfoCategory)
class InfoCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(InfoPost)
class InfoPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'tags']
    search_fields = ['title', 'content']
    filter_horizontal = ['tags']

@admin.register(InfoComment)
class InfoCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at', 'parent']
    list_filter = ['created_at']
    search_fields = ['content', 'user__full_name', 'post__title']
    raw_id_fields = ['post', 'user', 'parent']
