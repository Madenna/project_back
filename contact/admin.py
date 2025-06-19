from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'method', 'contact_value', 'message', 'submitted_at')
    list_filter = ('method', 'submitted_at')
    search_fields = ('contact_value', 'message')
    readonly_fields = ('method', 'contact_value', 'message', 'submitted_at')
    ordering = ('submitted_at',)