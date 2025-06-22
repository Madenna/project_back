# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from .serializers import ContactMessageSerializer
# from rest_framework import permissions

# class ContactMessageCreateView(APIView):
#     permission_classes = [permissions.AllowAny]
#     @swagger_auto_schema(
#         request_body=ContactMessageSerializer,
#         responses={
#             201: openapi.Response('Created', ContactMessageSerializer),
#             400: 'Validation Error'
#         },
#         operation_description="Submit a contact message with either email or phone and a message body."
#     )
#     def post(self, request):
#         serializer = ContactMessageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Your message has been sent successfully.'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .serializers import ContactMessageSerializer
from .models import ContactMessage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ContactMessageCreateView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        operation_description="Send a claim or suggestion (for all users, auth optional)",
        request_body=ContactMessageSerializer,
        responses={
            201: openapi.Response("Message created successfully"),
            400: "Validation error"
        }
    )
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user if request.user.is_authenticated else None)
            return Response({'message': 'Your message has been sent successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ContactMessageHistoryView(generics.ListAPIView):
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get current user's contact message history (requires authentication)",
        responses={200: ContactMessageSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return ContactMessage.objects.filter(user=self.request.user).order_by('-created_at')
