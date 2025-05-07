from django.urls import path
from .views import (
    # Specialists
    SpecialistListView,
    SpecialistDetailView,
    SpecialistCommentCreateView,
    SpecialistCommentDeleteView,
    SpecialistReplyDeleteView,
    SpecialistReplyCreateView,
    SpecialistListReplyView,
    SpecialistListCommentView,

    # Therapy Centers
    TherapyCenterListView,
    TherapyCenterDetailView,
    TherapyCenterCommentCreateView,
    TherapyCenterCommentDeleteView,
    TherapyCenterReplyDeleteView,
    TherapyCenterReplyCreateView,
    TherapyCenterListReplyView,
    TherapyCenterListCommentView,

    # News
    NewsListView,
    NewsDetailView,
    NewsCommentCreateView,
    NewsCommentDeleteView,
    NewsReplyDeleteView,
    NewsReplyCreateView,
    NewsListReplyView,
    NewsListCommentView,
)
urlpatterns = [
    # Specialist Views
    path('specialists/', SpecialistListView.as_view(), name='specialist_list'),
    path('specialists/<uuid:pk>/', SpecialistDetailView.as_view(), name='specialist_detail'),
    path('specialists/<uuid:specialist_pk>/comments/', SpecialistCommentCreateView.as_view(), name='create_specialist_comment'),
    path('specialists/comments/<uuid:pk>/delete/', SpecialistCommentDeleteView.as_view(), name='delete_specialist_comment'),
    path('specialists/<uuid:specialist_pk>/comments/', SpecialistListCommentView.as_view(), name='list_specialist_comments'),
    path('specialists/comments/<uuid:comment_pk>/replies/', SpecialistListReplyView.as_view(), name='list_specialist_replies'),
    path('specialists/comments/<uuid:comment_pk>/replies/create/', SpecialistReplyCreateView.as_view(), name='create_specialist_reply'),
    path('specialists/comments/replies/<uuid:pk>/delete/', SpecialistReplyDeleteView.as_view(), name='delete_specialist_reply'),

    # Therapy Center Views
    path('therapy-centers/', TherapyCenterListView.as_view(), name='therapy_center_list'),
    path('therapy-centers/<uuid:pk>/', TherapyCenterDetailView.as_view(), name='therapy_center_detail'),
    path('therapy-centers/<uuid:center_pk>/comments/', TherapyCenterCommentCreateView.as_view(), name='create_therapy_center_comment'),
    path('therapy-centers/comments/<uuid:pk>/delete/', TherapyCenterCommentDeleteView.as_view(), name='delete_therapy_center_comment'),
    path('therapy-centers/<uuid:center_pk>/comments/', TherapyCenterListCommentView.as_view(), name='list_therapy_center_comments'),
    path('therapy-centers/comments/<uuid:comment_pk>/replies/', TherapyCenterListReplyView.as_view(), name='list_therapy_center_replies'),
    path('therapy-centers/comments/<uuid:comment_pk>/replies/create/', TherapyCenterReplyCreateView.as_view(), name='create_therapy_center_reply'),
    path('therapy-centers/comments/replies/<uuid:pk>/delete/', TherapyCenterReplyDeleteView.as_view(), name='delete_therapy_center_reply'),

    # News Views
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<uuid:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/<uuid:news_pk>/comments/', NewsCommentCreateView.as_view(), name='create_news_comment'),
    path('news/comments/<uuid:pk>/delete/', NewsCommentDeleteView.as_view(), name='delete_news_comment'),
    path('news/<uuid:news_pk>/comments/', NewsListCommentView.as_view(), name='list_news_comments'),
    path('news/comments/<uuid:comment_pk>/replies/', NewsListReplyView.as_view(), name='list_news_replies'),
    path('news/comments/<uuid:comment_pk>/replies/create/', NewsReplyCreateView.as_view(), name='create_news_reply'),
    path('news/comments/replies/<uuid:pk>/delete/', NewsReplyDeleteView.as_view(), name='delete_news_reply'),
]

# urlpatterns = [
#     # --- Specialists ---
#     path('specialists/', SpecialistListView.as_view(), name='specialist_list'),
#     path('specialists/<uuid:id>/', SpecialistDetailView.as_view(), name='specialist_detail'),
#     path('specialists/<uuid:specialist_id>/comment/', SpecialistCommentCreateView.as_view(), name='specialist_comment_create'),

#     # --- Therapy Centers ---
#     path('centers/', TherapyCenterListView.as_view(), name='center_list'),
#     path('centers/<uuid:id>/', TherapyCenterDetailView.as_view(), name='center_detail'),
#     path('centers/<uuid:center_id>/comment/', TherapyCenterCommentCreateView.as_view(), name='center_comment_create'),

#     # --- News ---
#     path('news/', NewsListView.as_view(), name='news_list'),
#     path('news/<uuid:id>/', NewsDetailView.as_view(), name='news_detail'),
#     path('news/<uuid:news_id>/comment/', NewsCommentCreateView.as_view(), name='news_comment_create'),


#     path('comments/<uuid:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
#     path('posts/<uuid:pk>/delete/', DiscussionPostDeleteView.as_view(), name='delete_post'),
#     path('comments/<uuid:pk>/like/', ToggleLikeCommentView.as_view(), name='toggle_like_comment'),
#     path('comments/replies/<uuid:reply_id>/like/', ToggleLikeReplyView.as_view(), name='toggle_like_reply'),
#     path('comments/<uuid:comment_id>/replies/', ReplyCreateView.as_view(), name='create_reply'),
#     path('replies/<uuid:pk>/delete/', ReplyDeleteView.as_view(), name='delete_reply'),
#     path('posts/<uuid:post_id>/comments/', ListCommentView.as_view(), name='list_comments'),
#     path('comments/<uuid:comment_id>/replies/', ListReplyView.as_view(), name='list_replies'),
# ]
