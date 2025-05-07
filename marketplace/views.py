from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .utils import upload_to_cloudinary
from drf_yasg import openapi
from .models import EquipmentItem, EquipmentCategory, AvailabilityType, ConditionType, EquipmentPhoto
from .serializers import EquipmentItemSerializer, EquipmentCategorySerializer, AvailabilityTypeSerializer, ConditionTypeSerializer, EquipmentPhotoSerializer

class EquipmentItemListCreateView(generics.ListCreateAPIView):
    serializer_class = EquipmentItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        print(f"Fetching items for user: {self.request.user}")
        return EquipmentItem.objects.filter(owner=self.request.user).prefetch_related('available_for').order_by('-created_at')

    def perform_create(self, serializer):
        item = serializer.save(owner=self.request.user)

        availability_data = serializer.validated_data.get('availability_ids', [])
        item.available_for.set(availability_data)

        for file_key in self.request.FILES:
            uploaded_file = self.request.FILES[file_key]
            photo_url = upload_to_cloudinary(uploaded_file)
            EquipmentPhoto.objects.create(item=item, image_url=photo_url)

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
    queryset = EquipmentItem.objects.all().prefetch_related('available_for').order_by('-created_at') 
    serializer_class = EquipmentItemSerializer
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(operation_description="Returns a list of all equipment items.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class PublicEquipmentDetailView(generics.RetrieveAPIView):
    queryset = EquipmentItem.objects.all()
    serializer_class = EquipmentItemSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Retrieve a specific equipment item by its ID.",
        responses={200: EquipmentItemSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class EquipmentCategoryListView(generics.ListAPIView):
    queryset = EquipmentCategory.objects.all().order_by('name')
    serializer_class = EquipmentCategorySerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve all available equipment categories.",
        responses={200: EquipmentCategorySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class AvailabilityTypeListView(generics.ListAPIView):
    queryset = AvailabilityType.objects.all().order_by('name')
    serializer_class = AvailabilityTypeSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve all available availability types.",
        responses={200: AvailabilityTypeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ConditionTypeListView(generics.ListAPIView):
    queryset = ConditionType.objects.all().order_by('name')
    serializer_class = ConditionTypeSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve all available condition types.",
        responses={200: ConditionTypeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

import logging
logger = logging.getLogger(__name__)  

class EquipmentPhotoUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            item_id = request.query_params.get('item_id')
            if not item_id:
                logger.warning("Item ID not provided in query params.")
                return Response({"error": "item_id is required in query parameters."}, status=status.HTTP_400_BAD_REQUEST)

            item = get_object_or_404(EquipmentItem, id=item_id, owner=request.user)

            photos = request.FILES.getlist('images')  # именно 'images'

            if not photos:
                logger.warning(f"No photos provided by user {request.user.email}.")
                return Response({"error": "No photos provided."}, status=status.HTTP_400_BAD_REQUEST)

            if len(photos) > 5:
                logger.warning(f"User {request.user.email} tried to upload {len(photos)} photos (limit is 5).")
                return Response({"error": "You can upload a maximum of 5 photos."}, status=status.HTTP_400_BAD_REQUEST)

            uploaded_photos = []

            for photo in photos:
                # Загрузка файла на Cloudinary
                try:
                    photo_url = upload_to_cloudinary(photo)
                    EquipmentPhoto.objects.create(item=item, image_url=photo_url)
                    uploaded_photos.append(photo_url)
                    logger.info(f"Photo uploaded for item {item.id} by {request.user.email}: {photo_url}")
                except Exception as e:
                    logger.error(f"Failed to upload photo: {str(e)}")
                    return Response({"error": "Failed to upload photo to cloud."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": "Photos uploaded successfully.",
                "photos": uploaded_photos
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception("Unexpected error while uploading photos.")
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)