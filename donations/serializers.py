from rest_framework import serializers
from .models import DonationRequest, DonationConfirmation, DonationPhoto

class DonationPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationPhoto
        fields = ['id', 'image']

class DonationRequestSerializer(serializers.ModelSerializer):
    remaining = serializers.SerializerMethodField()
    photos = DonationPhotoSerializer(many=True, required=False)

    class Meta:
        model = DonationRequest
        fields = [
            'id', 'user', 'child', 'purpose',
            'goal_amount', 'donated_amount', 'remaining',
            'kaspi_code', 'kaspi_qr', 'deadline',
            'is_approved', 'is_active', 'created_at', 'photos'
        ]
        read_only_fields = ['user', 'donated_amount', 'kaspi_code', 'kaspi_qr', 'is_approved', 'created_at']

    def get_remaining(self, obj):
        return obj.remaining_amount()

    def validate_photos(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("You can upload up to 10 photos.")
        return value
    
    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        donation = DonationRequest.objects.create(**validated_data)
        for photo_data in photos_data:
            DonationPhoto.objects.create(donation_request=donation, **photo_data)
        return donation

class DonationConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationConfirmation
        fields = ['id', 'donor', 'donation_request', 'amount', 'comment', 'donated_at']
        read_only_fields = ['donor', 'donated_at']
