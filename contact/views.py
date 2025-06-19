from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import ContactMessageSerializer

class ContactMessageCreateView(APIView):
    @swagger_auto_schema(
        request_body=ContactMessageSerializer,
        responses={
            201: openapi.Response('Created', ContactMessageSerializer),
            400: 'Validation Error'
        },
        operation_description="Submit a contact message with either email or phone and a message body."
    )
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your message has been sent successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

