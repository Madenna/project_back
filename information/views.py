from rest_framework import permissions, generics
from django.shortcuts import get_object_or_404
from .models import (
    Specialist, TherapyCenter, News,
    SpecialistComment, TherapyCenterComment, NewsComment, SpecialistReply, NewsReply, TherapyCenterReply
)
from .serializers import (
    SpecialistSerializer, TherapyCenterSerializer, NewsSerializer,
    SpecialistCommentSerializer, TherapyCenterCommentSerializer, NewsCommentSerializer, SpecialistReplySerializer, NewsReplySerializer, TherapyCenterReplySerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView, Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import upload_to_cloudinary  

class SpecialistListView(generics.ListAPIView):
    queryset = Specialist.objects.all().order_by('-created_at')
    serializer_class = SpecialistSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Returns a list of specialists.",
        responses={200: SpecialistSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SpecialistDetailView(generics.RetrieveAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a specialist by ID.",
        responses={200: SpecialistSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SpecialistCommentCreateView(generics.CreateAPIView):
    serializer_class = SpecialistCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=SpecialistCommentSerializer,
        operation_description="Create a comment for a specialist (with optional rating).",
        responses={201: SpecialistCommentSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        specialist_id = self.kwargs.get('specialist_id')
        specialist = get_object_or_404(Specialist, id=specialist_id)
        
        # If it's a reply, find the parent comment
        parent_id = self.request.data.get('parent_id')
        parent = None
        
        # If parent_id exists, we are creating a reply and not a new comment
        if parent_id:
            parent = get_object_or_404(SpecialistComment, id=parent_id)
            # Ensure parent is not itself a reply (just in case)
            if parent.parent:
                raise PermissionDenied("Replies can't be created for replies.")
        
        # Create the comment or reply
        serializer.save(user=self.request.user, specialist=specialist, parent=parent)

class SpecialistCommentDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SpecialistComment.objects.all()

    @swagger_auto_schema(operation_description="Delete a specialist comment (only by its author)")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You can delete only your own comments.")
        return obj

class SpecialistListCommentView(generics.ListAPIView):
    serializer_class = SpecialistCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve comments for a specific specialist")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        specialist_id = self.kwargs.get('specialist_id')
        specialist = get_object_or_404(Specialist, id=specialist_id)
        return SpecialistComment.objects.filter(specialist=specialist).order_by('created_at')

class SpecialistListReplyView(generics.ListAPIView):
    serializer_class = SpecialistReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve replies for a specific specialist")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(SpecialistComment, id=comment_id)
        return SpecialistReply.objects.filter(comment=comment).order_by('created_at')

class SpecialistReplyCreateView(generics.CreateAPIView):
    serializer_class = SpecialistReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(SpecialistComment, id=comment_id)
        serializer.save(user=self.request.user, parent=comment)
    
class SpecialistReplyDeleteView(generics.DestroyAPIView):
    queryset = SpecialistReply.objects.all()
    serializer_class = SpecialistReplySerializer

    def delete(self, request, *args, **kwargs):
        reply = self.get_object()

        # Check if the logged-in user is the author of the reply
        if reply.user != request.user:
            raise PermissionDenied("You can delete only your own replies.")

        return super().delete(request, *args, **kwargs)
    
class TherapyCenterListView(generics.ListAPIView):
    queryset = TherapyCenter.objects.all().order_by('-created_at')
    serializer_class = TherapyCenterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Returns a list of therapy centers.",
        responses={200: TherapyCenterSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class TherapyCenterDetailView(generics.RetrieveAPIView):
    queryset = TherapyCenter.objects.all()
    serializer_class = TherapyCenterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a therapy center by ID.",
        responses={200: TherapyCenterSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class TherapyCenterCommentCreateView(generics.CreateAPIView):
    serializer_class = TherapyCenterCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=TherapyCenterCommentSerializer,
        operation_description="Create a comment for a therapy center (with optional rating).",
        responses={201: TherapyCenterCommentSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        center_id = self.kwargs.get('center_id')
        center = get_object_or_404(TherapyCenter, id=center_id)
        
        # If it's a reply, find the parent comment
        parent_id = self.request.data.get('parent_id')
        parent = None
        
        # If parent_id exists, we are creating a reply and not a new comment
        if parent_id:
            parent = get_object_or_404(TherapyCenterComment, id=parent_id)
            # Ensure parent is not itself a reply (just in case)
            if parent.parent:
                raise PermissionDenied("Replies can't be created for replies.")
        
        # Create the comment or reply
        serializer.save(user=self.request.user, center=center, parent=parent)

class TherapyCenterCommentDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TherapyCenterComment.objects.all()

    @swagger_auto_schema(operation_description="Delete a therapy center comment (only by its author)")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You can delete only your own comments.")
        return obj

class TherapyCenterListCommentView(generics.ListAPIView):
    serializer_class = TherapyCenterCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve comments for a specific therapy center")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        center_id = self.kwargs.get('center_id')
        center = get_object_or_404(TherapyCenter, id=center_id)
        return TherapyCenterComment.objects.filter(center=center).order_by('created_at')

class TherapyCenterListReplyView(generics.ListAPIView):
    serializer_class = TherapyCenterReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve replies for a specific therapy center")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(TherapyCenterComment, id=comment_id)
        return TherapyCenterReply.objects.filter(comment=comment).order_by('created_at')

class TherapyCenterReplyCreateView(generics.CreateAPIView):
    serializer_class = TherapyCenterReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(TherapyCenterComment, id=comment_id)
        serializer.save(user=self.request.user, parent=comment)
    
class TherapyCenterReplyDeleteView(generics.DestroyAPIView):
    queryset = TherapyCenterReply.objects.all()
    serializer_class = TherapyCenterReplySerializer

    def delete(self, request, *args, **kwargs):
        reply = self.get_object()

        # Check if the logged-in user is the author of the reply
        if reply.user != request.user:
            raise PermissionDenied("You can delete only your own replies.")

        return super().delete(request, *args, **kwargs)

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Returns a list of news articles.",
        responses={200: NewsSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a news article by ID.",
        responses={200: NewsSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class NewsCommentCreateView(generics.CreateAPIView):
    serializer_class = NewsCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=NewsCommentSerializer,
        operation_description="Create a comment for a news article.",
        responses={201: NewsCommentSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        news_id = self.kwargs.get('specialist_id')
        news = get_object_or_404(News, id=news_id)
        
        # If it's a reply, find the parent comment
        parent_id = self.request.data.get('parent_id')
        parent = None
        
        # If parent_id exists, we are creating a reply and not a new comment
        if parent_id:
            parent = get_object_or_404(NewsComment, id=parent_id)
            # Ensure parent is not itself a reply (just in case)
            if parent.parent:
                raise PermissionDenied("Replies can't be created for replies.")
        
        # Create the comment or reply
        serializer.save(user=self.request.user, news=news, parent=parent)

class NewsCommentDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NewsComment.objects.all()

    @swagger_auto_schema(operation_description="Delete a comment (only by its author)")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You can delete only your own comments.")
        return obj
    
class NewsListCommentView(generics.ListAPIView):
    serializer_class = NewsCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve comments for a specific news")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        news_id = self.kwargs.get('news_id')
        news = get_object_or_404(News, id=news_id)
        return SpecialistComment.objects.filter(news=news).order_by('created_at')

class NewsListReplyView(generics.ListAPIView):
    serializer_class = NewsReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve replies for a specific news")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(NewsComment, id=comment_id)
        return NewsReply.objects.filter(comment=comment).order_by('created_at')

class NewsReplyCreateView(generics.CreateAPIView):
    serializer_class = NewsReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment_id = self.kwargs.get('news_id')
        comment = get_object_or_404(NewsComment, id=comment_id)
        serializer.save(user=self.request.user, parent=comment)
    
class NewsReplyDeleteView(generics.DestroyAPIView):
    queryset = NewsReply.objects.all()
    serializer_class = NewsReplySerializer

    def delete(self, request, *args, **kwargs):
        reply = self.get_object()

        # Check if the logged-in user is the author of the reply
        if reply.user != request.user:
            raise PermissionDenied("You can delete only your own replies.")

        return super().delete(request, *args, **kwargs)