# donations/urls.py
from django.urls import path
from .views import (
    DonationRequestListCreateView,
    DonationRequestDetailView,
    DonationConfirmationCreateView
)

urlpatterns = [
    path('donations/', DonationRequestListCreateView.as_view(), name='donation_list_create'),
    path('donations/<int:pk>/', DonationRequestDetailView.as_view(), name='donation_detail'),
    path('donations/confirm/', DonationConfirmationCreateView.as_view(), name='donation_confirm'),
]
