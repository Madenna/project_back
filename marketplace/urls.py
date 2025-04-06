from django.urls import path
from .views import (
    EquipmentItemListCreateView,
    EquipmentItemDetailView,
    EquipmentItemListView  # for public browsing with filters
)

urlpatterns = [
    path("my-items/", EquipmentItemListCreateView.as_view(), name="my_equipment_list_create"),
    path("my-items/<uuid:id>/", EquipmentItemDetailView.as_view(), name="my_equipment_detail"),
    path("public-items/", EquipmentItemListView.as_view(), name="public_equipment_list"),
]
