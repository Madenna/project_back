from rest_framework import generics, permissions
from .models import SymptomEntry
from .serializers import SymptomEntrySerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import PermissionDenied

class SymptomEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = SymptomEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SymptomEntry.objects.filter(child__parent=self.request.user)

    def perform_create(self, serializer):
        child = serializer.validated_data['child']
        if child.parent != self.request.user:
            raise PermissionDenied("You can only add symptoms for your own child.")
        serializer.save()

    @swagger_auto_schema(
        operation_description="List all symptom entries for the current parent user.",
        responses={200: SymptomEntrySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=SymptomEntrySerializer,
        operation_description="Create a new symptom entry for a selected child.",
        responses={201: SymptomEntrySerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SymptomEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SymptomEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return SymptomEntry.objects.filter(child__parent=self.request.user)

    @swagger_auto_schema(
        operation_description="Retrieve a specific symptom entry.",
        responses={200: SymptomEntrySerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=SymptomEntrySerializer,
        operation_description="Update an existing symptom entry.",
        responses={200: SymptomEntrySerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific symptom entry.",
        responses={204: "Deleted successfully."}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
