from rest_framework import generics, permissions, status
from .models import DiscussionPost, DiscussionCategory, Comment
from .serializers import DiscussionPostSerializer, CommentSerializer, DiscussionCategorySerializer

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView, Response
from rest_framework.exceptions import PermissionDenied


class DiscussionPostListCreateView(generics.ListCreateAPIView):
    queryset = DiscussionPost.objects.all().order_by('-created_at')
    serializer_class = DiscussionPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=DiscussionPostSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer_context(self):
        return {"request": self.request}


class DiscussionPostDetailView(generics.RetrieveAPIView):
    queryset = DiscussionPost.objects.all()
    serializer_class = DiscussionPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(DiscussionPost, id=post_id)
        parent_id = self.request.data.get('parent_id')
        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
        serializer.save(user=self.request.user, post=post, parent=parent)

class CategoryListView(generics.ListAPIView):
    queryset = DiscussionCategory.objects.all()
    serializer_class = DiscussionCategorySerializer

    @swagger_auto_schema(operation_description="List all discussion categories")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    @swagger_auto_schema(operation_description="Delete a comment (only by its author)")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You can delete only your own comments.")
        return obj


class DiscussionPostDeleteView(generics.DestroyAPIView):
    queryset = DiscussionPost.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Delete a post (only by its author)")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        post = super().get_object()
        if post.user != self.request.user:
            raise PermissionDenied("You can delete only your own posts.")
        return post


class ToggleLikeCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Toggle like on a comment",
        responses={200: openapi.Response("Like toggled", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'liked': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'likes_count': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))}
    )
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True
        return Response({"liked": liked, "likes_count": comment.likes.count()}, status=status.HTTP_200_OK)
