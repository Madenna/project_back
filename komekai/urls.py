from django.urls import path
from .views import ChatSessionListCreateView, ChatMessageView

urlpatterns = [
    path('sessions/', ChatSessionListCreateView.as_view()),
    path('sessions/<uuid:session_id>/message/', ChatMessageView.as_view()),
]