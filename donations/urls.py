# donations/urls.py
from django.urls import path
from .views import (
    DonationRequestListCreateView,
    DonationRequestDetailView,
    DonationConfirmationCreateView
)

urlpatterns = [
    path('donation/', DonationRequestListCreateView.as_view(), name='donation_list_create'),
    path('donation/<int:pk>/', DonationRequestDetailView.as_view(), name='donation_detail'),
    path('donation/confirm/', DonationConfirmationCreateView.as_view(), name='donation_confirm'),
]
