from django.urls import path
from .views import (
    DiscussionPostListCreateView, DiscussionPostDetailView,
    CommentCreateView, CategoryListView
)

urlpatterns = [
    path('posts/', DiscussionPostListCreateView.as_view(), name='discussion_post_list'),
    path('posts/<uuid:id>/', DiscussionPostDetailView.as_view(), name='discussion_post_detail'),
    path('posts/<uuid:post_id>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
]
