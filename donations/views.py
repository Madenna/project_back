# donations/views.py
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from .models import DonationRequest, DonationConfirmation
from .serializers import DonationRequestSerializer, DonationConfirmationSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

class DonationRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = DonationRequestSerializer

    def get_queryset(self):
        return DonationRequest.objects.filter(is_approved=True, is_active=True).order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        child = serializer.validated_data['child']
        if child.parent != self.request.user:
            raise PermissionDenied("You can only create donation requests for your own children.")
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Get list of approved donation requests",
        responses={200: DonationRequestSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create new donation request (must be authenticated)",
        request_body=DonationRequestSerializer,
        responses={201: openapi.Response("Created", DonationRequestSerializer),
                   400: "Validation Error"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class DonationRequestDetailView(generics.RetrieveAPIView):
    queryset = DonationRequest.objects.filter(is_approved=True, is_active=True)
    serializer_class = DonationRequestSerializer
    permission_classes = [permissions.AllowAny]

class DonationConfirmationCreateView(generics.CreateAPIView):
    serializer_class = DonationConfirmationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)
        
    @swagger_auto_schema(
        operation_description="Confirm donation by entering donation_request ID and amount",
        request_body=DonationConfirmationSerializer,
        responses={201: openapi.Response("Created", DonationConfirmationSerializer),
                   400: "Invalid data"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
