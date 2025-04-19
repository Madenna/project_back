from rest_framework import serializers
from .models import EquipmentCategory, EquipmentItem, AvailabilityType, EquipmentPhoto, ConditionType

class EquipmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory
        fields = ['id', 'name']


class AvailabilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityType
        fields = ['id', 'name']


class EquipmentPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentPhoto
        fields = ['id', 'image_url']


class EquipmentItemSerializer(serializers.ModelSerializer):
    category = EquipmentCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=EquipmentCategory.objects.all(), source='category', write_only=True
    )
    availability = AvailabilityTypeSerializer(many=True, read_only=True)
    availability_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AvailabilityType.objects.all(),
        source='availability',
        write_only=True
    )
    photos = EquipmentPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = EquipmentItem
        fields = [
            'id', 'name', 'description', 'category', 'category_id', 'condition',
            'availability', 'availability_ids', 'location', 'contact_method',
            'price', 'created_at', 'updated_at', 'photos'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'photos']
    
class ConditionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionType
        fields = ['id', 'key', 'label']