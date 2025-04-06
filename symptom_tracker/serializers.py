from rest_framework import serializers
from .models import SymptomEntry

class SymptomEntrySerializer(serializers.ModelSerializer):
    child_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SymptomEntry
        fields = [
            'id', 'child', 'child_name', 'date', 'symptom_name', 'action_taken', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'child_name']

    def get_child_name(self, obj):
        return obj.child.full_name if obj.child else None

    def validate_date(self, value):
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value

    def validate_child(self, child):
        request = self.context.get('request')
        if request and request.user != child.parent:
            raise serializers.ValidationError("You can only assign symptoms to your own children.")
        return child

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        from django.utils.timezone import localtime
        rep['created_at'] = localtime(instance.created_at).strftime('%Y-%m-%d %H:%M:%S')
        rep['updated_at'] = localtime(instance.updated_at).strftime('%Y-%m-%d %H:%M:%S')
        return rep
