from django.urls import path
from .views import (
    InfoPostListView, InfoCommentCreateView, InfoCommentUpdateDeleteView,
    ToggleLikePostView
)

urlpatterns = [
    path('infohub/', InfoPostListView.as_view(), name='infohub_list'),
    path('infohub/<uuid:post_id>/comment/', InfoCommentCreateView.as_view(), name='infohub_comment'),
    path('infohub/comment/<uuid:id>/', InfoCommentUpdateDeleteView.as_view(), name='comment_update_delete'),
    path('infohub/<uuid:post_id>/like/', ToggleLikePostView.as_view(), name='toggle_like'),
]