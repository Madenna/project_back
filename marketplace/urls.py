from django.urls import path
from .views import (
    EquipmentItemListCreateView,
    EquipmentItemDetailView,
    PublicEquipmentListView,
    EquipmentCategoryListView,  
    AvailabilityTypeListView,
    ConditionTypeListView,
    EquipmentPhotoUploadView,
    PublicEquipmentDetailView,
)

urlpatterns = [
    path("my-items/", EquipmentItemListCreateView.as_view(), name="my_equipment_list_create"),
    path("my-items/<uuid:id>/", EquipmentItemDetailView.as_view(), name="my_equipment_detail"),
    path("public-items/", PublicEquipmentListView.as_view(), name="public_equipment_list"),
    path("categories/", EquipmentCategoryListView.as_view(), name="equipment_category_list"),  
    path("availability-types/", AvailabilityTypeListView.as_view(), name="availability_type_list"),
    path("conditions/", ConditionTypeListView.as_view(), name="condition_type_list"), 
    path("equipment-photos/", EquipmentPhotoUploadView.as_view(), name="upload_equipment_photo"),
    path("public-items/<uuid:id>/", PublicEquipmentDetailView.as_view(), name="public_equipment_detail"),
]
