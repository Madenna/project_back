from django.urls import path
from .views import (
    ChatSessionListCreateView,
    ChatMessageView,
    ChatSessionDeleteView, 
)

urlpatterns = [
    path('api/komekai/sessions/', ChatSessionListCreateView.as_view(), name='chat_sessions_list_create'),
    path('api/komekai/sessions/<uuid:session_id>/message/', ChatMessageView.as_view(), name='chat_message'),
    path('api/komekai/sessions/<uuid:session_id>/delete/', ChatSessionDeleteView.as_view(), name='chat_session_delete'),  
]
