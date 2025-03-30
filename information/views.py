from rest_framework import permissions, generics
from django.shortcuts import get_object_or_404
from .models import InfoPost, InfoComment, InfoTag
from .serializers import InfoPostSerializer, InfoCommentSerializer, InfoTagSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView, Response

# class InformationItemViewSet(viewsets.ModelViewSet):
#     queryset = InformationItem.objects.all().order_by("-created_at")
#     serializer_class = InformationItemSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class InfoPostListView(generics.ListAPIView):
    serializer_class = InfoPostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = InfoPost.objects.all().order_by('-created_at')

        category_name = self.request.query_params.get('category')
        tag_name = self.request.query_params.get('tag')

        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)

        if tag_name:
            queryset = queryset.filter(tags__name__iexact=tag_name)

        return queryset
    
    @swagger_auto_schema(
        operation_description="Returns a list of Info Hub posts. Supports filtering by category and tag using query parameters.",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category name", type=openapi.TYPE_STRING),
            openapi.Parameter('tag', openapi.IN_QUERY, description="Filter by tag name", type=openapi.TYPE_STRING),
        ],
        responses={200: InfoPostSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class InfoCommentCreateView(generics.CreateAPIView):
    serializer_class = InfoCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=InfoCommentSerializer,
        operation_description="Create a new comment for a specific Info Hub post.",
        responses={201: InfoCommentSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(InfoPost, id=post_id)
        serializer.save(user=self.request.user, post=post)

class InfoCommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfoComment.objects.all()
    serializer_class = InfoCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return InfoComment.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Retrieve a specific comment by its ID.",
        responses={200: InfoCommentSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=InfoCommentSerializer,
        operation_description="Update an existing comment.",
        responses={200: InfoCommentSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=InfoCommentSerializer,
        operation_description="Partially update an existing comment.",
        responses={200: InfoCommentSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a comment by ID.",
        responses={204: "Comment deleted successfully."}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ToggleLikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Toggle like/unlike for a specific Info Hub post. Returns liked: true or false.",
        responses={
            200: openapi.Response(
                description="Success",
                examples={"application/json": {"liked": True}}
            ),
            404: "Post not found"
        }
    )

    def post(self, request, post_id):
        post = get_object_or_404(InfoPost, id=post_id)
        user = request.user
        if user in post.liked_by.all():
            post.liked_by.remove(user)
            return Response({"liked": False}, status=200)
        else:
            post.liked_by.add(user)
            return Response({"liked": True}, status=200)
        
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import upload_to_cloudinary

class InfoPostCreateView(generics.CreateAPIView):
    serializer_class = InfoPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=InfoPostSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'photo' in request.FILES:
            uploaded_file = request.FILES['photo']
            photo_url = upload_to_cloudinary(uploaded_file)
            data['photo'] = photo_url  # Store Cloudinary URL in DB

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
