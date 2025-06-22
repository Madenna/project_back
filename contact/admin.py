from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_method', 'contact_detail', 'message', 'created_at')
    list_filter = ('contact_method', 'created_at')
    search_fields = ('contact_detail', 'message')
    readonly_fields = ('contact_method', 'contact_detail', 'message', 'created_at')
    ordering = ('created_at',)