from django.urls import path
from .views import ContactMessageCreateView, ContactMessageHistoryView

urlpatterns = [
    path('', ContactMessageCreateView.as_view(), name='contact-us'),
    path('history/', ContactMessageHistoryView.as_view(), name='contact_history'),
]
