# komekai/admin.py
from django.contrib import admin
from .models import ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'content', 'timestamp')
    can_delete = True  
    show_change_link = False

class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'user__username')
    inlines = [ChatMessageInline]
    readonly_fields = ('created_at',)
    actions = ['delete_sessions']  

    def delete_sessions(self, request, queryset):
        """
        Custom delete action for selected chat sessions.
        """
        count, _ = queryset.delete()  
        self.message_user(request, f'{count} session(s) were deleted successfully.')

    delete_sessions.short_description = "Delete selected chat sessions"

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content_short', 'session', 'timestamp')
    list_filter = ('sender', 'timestamp')
    search_fields = ('content',)

    def content_short(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_short.short_description = 'Content'

admin.site.register(ChatSession, ChatSessionAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
