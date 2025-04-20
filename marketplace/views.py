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
        return EquipmentItem.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        item = serializer.save(owner=self.request.user)

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
    queryset = EquipmentItem.objects.all().order_by('-created_at')
    serializer_class = EquipmentItemSerializer
    permission_classes = [permissions.AllowAny]

class PublicEquipmentDetailView(generics.RetrieveAPIView):
    queryset = EquipmentItem.objects.all()
    serializer_class = EquipmentItemSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

class EquipmentCategoryListView(generics.ListAPIView):
    queryset = EquipmentCategory.objects.all().order_by('name')
    serializer_class = EquipmentCategorySerializer
    permission_classes = [permissions.AllowAny]

class AvailabilityTypeListView(generics.ListAPIView):
    queryset = AvailabilityType.objects.all().order_by('name')
    serializer_class = AvailabilityTypeSerializer
    permission_classes = [permissions.AllowAny]

class ConditionTypeListView(generics.ListAPIView):
    queryset = ConditionType.objects.all().order_by('name')
    serializer_class = ConditionTypeSerializer
    permission_classes = [permissions.AllowAny]

class EquipmentPhotoUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'item_id', openapi.IN_FORM, description="Equipment Item ID", type=openapi.TYPE_STRING, required=True
            ),
        ],
        operation_description="Upload multiple photos for an equipment item (max 5).",
        responses={201: EquipmentPhotoSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        try:
            item_id = request.data.get('item_id')
            if not item_id:
                return Response({"error": "item_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            item = get_object_or_404(EquipmentItem, id=item_id)

            # Проверка владельца
            if item.owner != request.user:
                return Response({"error": "You can only upload photos for your own items."}, status=status.HTTP_403_FORBIDDEN)

            files = request.FILES.getlist('photos')
            if not files:
                return Response({"error": "No photos provided."}, status=status.HTTP_400_BAD_REQUEST)

            if len(files) > 5:
                return Response({"error": "Maximum 5 photos allowed."}, status=status.HTTP_400_BAD_REQUEST)

            photo_instances = []

            for file in files:
                # Проверка типа файла
                if not file.content_type.startswith('image/'):
                    return Response({"error": f"Invalid file type: {file.content_type}. Only images are allowed."},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Заливаем на Cloudinary
                photo_url = upload_to_cloudinary(file)

                # Создаем запись в БД
                photo = EquipmentPhoto.objects.create(item=item, image_url=photo_url)
                photo_instances.append(photo)

            serializer = EquipmentPhotoSerializer(photo_instances, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)