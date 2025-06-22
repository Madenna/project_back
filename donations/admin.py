# donations/admin.py
from django.contrib import admin
from .models import DonationRequest, DonationConfirmation

@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'child', 'goal_amount', 'donated_amount', 'deadline', 'is_approved', 'is_active')
    list_filter = ('is_approved', 'is_active')
    list_editable = ('is_approved', 'is_active')
    search_fields = ('child__name', 'purpose')

@admin.register(DonationConfirmation)
class DonationConfirmationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'donation_request', 'amount', 'donated_at')
    search_fields = ('donor__username', 'donation_request__id')
