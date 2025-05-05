from django.urls import path
from .views import (
    DiscussionPostListCreateView, DiscussionPostDetailView, ReplyDeleteView, ListCommentView, ListReplyView, ToggleLikeReplyView,
    CommentCreateView, CategoryListView, CommentDeleteView, DiscussionPostDeleteView, ToggleLikeCommentView, ReplyCreateView
)

urlpatterns = [
    path('posts/', DiscussionPostListCreateView.as_view(), name='discussion_post_list'),
    path('posts/<uuid:id>/', DiscussionPostDetailView.as_view(), name='discussion_post_detail'),
    path('posts/<uuid:post_id>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('comments/<uuid:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('posts/<uuid:pk>/delete/', DiscussionPostDeleteView.as_view(), name='delete_post'),
    path('comments/<uuid:pk>/like/', ToggleLikeCommentView.as_view(), name='toggle_like_comment'),
    path('comments/replies/<uuid:reply_id>/like/', ToggleLikeReplyView.as_view(), name='toggle_like_reply'),
    path('comments/<uuid:comment_id>/replies/', ReplyCreateView.as_view(), name='create_reply'),
    path('comments/replies/<uuid:pk>/delete/', ReplyDeleteView.as_view(), name='delete_reply'),
    path('posts/<uuid:post_id>/comments/', ListCommentView.as_view(), name='list_comments'),
    path('comments/<uuid:comment_id>/replies/', ListReplyView.as_view(), name='list_replies'),
]