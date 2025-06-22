# donations/views.py
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import DonationRequest, DonationConfirmation
from .serializers import DonationRequestSerializer, DonationConfirmationSerializer

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


class DonationRequestDetailView(generics.RetrieveAPIView):
    queryset = DonationRequest.objects.filter(is_approved=True, is_active=True)
    serializer_class = DonationRequestSerializer
    permission_classes = [permissions.AllowAny]


class DonationConfirmationCreateView(generics.CreateAPIView):
    serializer_class = DonationConfirmationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)
