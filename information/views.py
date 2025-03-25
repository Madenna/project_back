from rest_framework import viewsets, permissions
from .models import InformationItem, Comment, Tag
from .serializers import InformationItemSerializer, CommentSerializer, TagSerializer

class InformationItemViewSet(viewsets.ModelViewSet):
    queryset = InformationItem.objects.all().order_by("-created_at")
    serializer_class = InformationItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(info__id=self.kwargs["info_id"])

    def perform_create(self, serializer):
        info_id = self.kwargs["info_id"]
        serializer.save(user=self.request.user, info_id=info_id)
