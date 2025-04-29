from rest_framework import permissions, generics
from django.shortcuts import get_object_or_404
from .models import (
    Specialist, TherapyCenter, News,
    SpecialistComment, TherapyCenterComment, NewsComment
)
from .serializers import (
    SpecialistSerializer, TherapyCenterSerializer, NewsSerializer,
    SpecialistCommentSerializer, TherapyCenterCommentSerializer, NewsCommentSerializer
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
    lookup_field = 'id'

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
        parent_id = self.request.data.get('parent_id')
        specialist = get_object_or_404(Specialist, id=specialist_id)
        parent = SpecialistComment.objects.filter(id=parent_id).first() if parent_id else None
        serializer.save(user=self.request.user, specialist=specialist, parent=parent)

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
    lookup_field = 'id'

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
        parent_id = self.request.data.get('parent_id')
        center = get_object_or_404(TherapyCenter, id=center_id)
        parent = TherapyCenterComment.objects.filter(id=parent_id).first() if parent_id else None
        serializer.save(user=self.request.user, center=center, parent=parent)

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
    lookup_field = 'id'

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
        news_id = self.kwargs.get('news_id')
        parent_id = self.request.data.get('parent_id')
        news = get_object_or_404(News, id=news_id)
        parent = NewsComment.objects.filter(id=parent_id).first() if parent_id else None
        serializer.save(user=self.request.user, news=news, parent=parent)
