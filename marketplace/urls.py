from django.urls import path
from .views import (
    EquipmentItemListCreateView,
    EquipmentItemDetailView,
    PublicEquipmentListView,
    EquipmentCategoryListView,  
)

urlpatterns = [
    path("my-items/", EquipmentItemListCreateView.as_view(), name="my_equipment_list_create"),
    path("my-items/<uuid:id>/", EquipmentItemDetailView.as_view(), name="my_equipment_detail"),
    path("public-items/", PublicEquipmentListView.as_view(), name="public_equipment_list"),
    path("categories/", EquipmentCategoryListView.as_view(), name="equipment_category_list"),  
]
