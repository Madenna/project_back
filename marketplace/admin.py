from django.contrib import admin
from .models import EquipmentItem, EquipmentCategory, AvailabilityType, EquipmentPhoto, ConditionType

@admin.register(AvailabilityType)
class AvailabilityTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(EquipmentPhoto)
class EquipmentPhotoAdmin(admin.ModelAdmin):
    list_display = ['item', 'image_url']

@admin.register(EquipmentItem)
class EquipmentItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'category', 'condition', 'location', 'created_at']
    raw_id_fields = ['owner', 'condition']
    filter_horizontal = ['available_for']

@admin.register(ConditionType)
class ConditionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']