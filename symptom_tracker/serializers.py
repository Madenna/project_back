from rest_framework import serializers
from .models import SymptomEntry

class SymptomEntrySerializer(serializers.ModelSerializer):
    child_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SymptomEntry
        fields = [
            'id', 'child', 'child_name', 'date', 'symptom_name', 'treatment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'child_name']

    def get_child_name(self, obj):
        return obj.child.full_name if obj.child else None

    def validate_date(self, value):
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['parent'] = request.user
        return super().create(validated_data)
