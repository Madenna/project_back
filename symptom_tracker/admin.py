from django.contrib import admin
from .models import SymptomEntry

@admin.register(SymptomEntry)
class SymptomEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'child', 'symptom_name', 'date', 'created_at')
    list_filter = ('child', 'date', 'created_at')
    search_fields = ('symptom_name', 'actions_taken', 'notes', 'child__full_name')
    ordering = ('-date',)
