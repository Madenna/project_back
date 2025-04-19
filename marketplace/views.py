from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import EquipmentItem, EquipmentCategory, AvailabilityType
from .serializers import EquipmentItemSerializer, EquipmentCategorySerializer, AvailabilityTypeSerializer


class EquipmentItemListCreateView(generics.ListCreateAPIView):
    serializer_class = EquipmentItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return EquipmentItem.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(operation_description="List all equipment items posted by the current user.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new equipment item.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class EquipmentItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EquipmentItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return EquipmentItem.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.owner != self.request.user:
            raise PermissionDenied("You can only edit your own items.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You can only delete your own items.")
        instance.delete()

    @swagger_auto_schema(operation_description="Retrieve a specific item.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update an equipment item.")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete an equipment item.")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class PublicEquipmentListView(generics.ListAPIView):
    queryset = EquipmentItem.objects.all().order_by('-created_at')
    serializer_class = EquipmentItemSerializer
    permission_classes = [permissions.AllowAny]


class EquipmentCategoryListView(generics.ListAPIView):
    queryset = EquipmentCategory.objects.all().order_by('name')
    serializer_class = EquipmentCategorySerializer
    permission_classes = [permissions.AllowAny]

class AvailabilityTypeListView(generics.ListAPIView):
    queryset = AvailabilityType.objects.all().order_by('name')
    serializer_class = AvailabilityTypeSerializer
    permission_classes = [permissions.AllowAny]

class ConditionListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        conditions = [
            {"value": condition.value, "label": condition.label}
            for condition in EquipmentItem.Condition
        ]
        return Response(conditions)
