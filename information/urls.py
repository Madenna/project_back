from django.urls import path
from .views import (
    InfoPostListView,
    InfoPostCreateView,
    InfoPostDetailView,
    InfoCommentCreateView,
    InfoCommentUpdateDeleteView,
    ToggleLikeCommentView,
)

urlpatterns = [
    path('infohub/', InfoPostListView.as_view(), name='infohub_list'),
    path('infohub/create/', InfoPostCreateView.as_view(), name='infohub_create'),  
    path('infohub/<uuid:id>/', InfoPostDetailView.as_view(), name='infohub_detail'),
    path('infohub/<uuid:post_id>/comment/', InfoCommentCreateView.as_view(), name='infohub_comment'),
    path('infohub/comment/<uuid:id>/', InfoCommentUpdateDeleteView.as_view(), name='comment_update_delete'),
    path('infohub/comment/<uuid:comment_id>/like/', ToggleLikeCommentView.as_view(), name='toggle_like_comment'),
]
