# donations/serializers.py
from rest_framework import serializers
from .models import DonationRequest, DonationConfirmation

class DonationRequestSerializer(serializers.ModelSerializer):
    remaining = serializers.SerializerMethodField()
    child_info = serializers.SerializerMethodField()

    class Meta:
        model = DonationRequest
        fields = [
            'id', 'user', 'child', 'child_info', 'purpose',
            'goal_amount', 'donated_amount', 'remaining',
            'kaspi_code', 'kaspi_qr', 'deadline',
            'is_approved', 'is_active', 'created_at'
        ]
        read_only_fields = ['user', 'donated_amount', 'kaspi_code', 'kaspi_qr', 'is_approved', 'created_at']

    def get_remaining(self, obj):
        return obj.remaining_amount()

    def get_child_info(self, obj):
        return {
            'id': obj.child.id,
            'name': obj.child.name,
            'photo': obj.child.photo.url if obj.child.photo else None,
        }


class DonationConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationConfirmation
        fields = ['id', 'donor', 'donation_request', 'amount', 'comment', 'donated_at']
        read_only_fields = ['donor', 'donated_at']
