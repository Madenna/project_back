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

class ConditionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionType
        fields = ['id', 'name']

class EquipmentItemSerializer(serializers.ModelSerializer):
    category = EquipmentCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=EquipmentCategory.objects.all(), source='category', write_only=True
    )
    availability = AvailabilityTypeSerializer(many=True, read_only=True)
    availability_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AvailabilityType.objects.all(),
        #source='availability',
        write_only=True
    )
    condition = ConditionTypeSerializer(read_only=True)
    condition_id = serializers.PrimaryKeyRelatedField(
        queryset=ConditionType.objects.all(), source='condition', write_only=True
    )
    photos = EquipmentPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = EquipmentItem
        fields = [
            'id', 'name', 'description', 'price', 'location', 'contact_method',
            'category', 'category_id',
            'condition', 'condition_id',
            'availability', 'availability_ids',
            'created_at', 'updated_at', 'photos'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'photos']

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        condition_id = validated_data.pop('condition_id')
        availability_ids = validated_data.pop('availability_ids', [])

        item = EquipmentItem.objects.create(
            category_id=category_id,
            condition_id=condition_id,
            **validated_data
        )
        item.availability.set(availability_ids)
        return item

    def update(self, instance, validated_data):
        availability_data = validated_data.pop('availability_ids', None)
        instance = super().update(instance, validated_data)
        if availability_data is not None:
            instance.available_for.set(availability_data)
        return instance
    
class EquipmentPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentPhoto
        fields = ['id', 'image_url']
        ref_name = "MarketplaceEquipmentPhoto" 
