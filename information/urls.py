from django.urls import path
from .views import (
    # Specialists
    SpecialistListView,
    SpecialistDetailView,
    SpecialistCommentCreateView,

    # Therapy Centers
    TherapyCenterListView,
    TherapyCenterDetailView,
    TherapyCenterCommentCreateView,

    # News
    NewsListView,
    NewsDetailView,
    NewsCommentCreateView,
)

urlpatterns = [
    # --- Specialists ---
    path('specialists/', SpecialistListView.as_view(), name='specialist_list'),
    path('specialists/<uuid:id>/', SpecialistDetailView.as_view(), name='specialist_detail'),
    path('specialists/<uuid:specialist_id>/comment/', SpecialistCommentCreateView.as_view(), name='specialist_comment_create'),

    # --- Therapy Centers ---
    path('centers/', TherapyCenterListView.as_view(), name='center_list'),
    path('centers/<uuid:id>/', TherapyCenterDetailView.as_view(), name='center_detail'),
    path('centers/<uuid:center_id>/comment/', TherapyCenterCommentCreateView.as_view(), name='center_comment_create'),

    # --- News ---
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<uuid:id>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/<uuid:news_id>/comment/', NewsCommentCreateView.as_view(), name='news_comment_create'),
]
