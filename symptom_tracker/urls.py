from django.urls import path
from .views import SymptomEntryListCreateView, SymptomEntryDetailView

urlpatterns = [
    path('entries/', SymptomEntryListCreateView.as_view(), name='symptom_entry_list_create'),
    path('entries/<uuid:id>/', SymptomEntryDetailView.as_view(), name='symptom_entry_detail'),
]
