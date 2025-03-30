from rest_framework import generics, permissions
from .models import DiscussionPost, DiscussionCategory, Comment
from .serializers import DiscussionPostSerializer, CommentSerializer, DiscussionCategorySerializer

class DiscussionPostListCreateView(generics.ListCreateAPIView):
    queryset = DiscussionPost.objects.all().order_by('-created_at')
    serializer_class = DiscussionPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


class DiscussionPostDetailView(generics.RetrieveAPIView):
    queryset = DiscussionPost.objects.all()
    serializer_class = DiscussionPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = DiscussionPost.objects.get(id=post_id)
        serializer.save(user=self.request.user, post=post)


class CategoryListView(generics.ListAPIView):
    queryset = DiscussionCategory.objects.all()
    serializer_class = DiscussionCategorySerializer
