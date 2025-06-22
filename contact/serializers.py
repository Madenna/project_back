# from rest_framework import serializers
# from .models import ContactMessage

# class ContactMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContactMessage
#         fields = ['id', 'method', 'contact_value', 'message', 'submitted_at']
# contact/serializers.py
from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'user', 'contact_method', 'contact_detail', 'message', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']
