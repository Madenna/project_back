from django.urls import path
from .views import SymptomEntryListCreateView, SymptomEntryDetailView, SymptomAIAnalyzeView, ExportSymptomsPDFView

urlpatterns = [
    path('entries/', SymptomEntryListCreateView.as_view(), name='symptom_entry_list_create'),
    path('entries/<uuid:id>/', SymptomEntryDetailView.as_view(), name='symptom_entry_detail'),
    path('ai-analyze/', SymptomAIAnalyzeView.as_view(), name='symptom_ai_analyze'),
    path('export-pdf/', ExportSymptomsPDFView.as_view(), name='export_symptoms_pdf'),
]
