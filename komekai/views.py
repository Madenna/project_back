from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from openai import OpenAI

# Function to initialize OpenAI client
def get_openai_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY)

class ChatSessionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ChatSessionSerializer(many=True)})
    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
        return Response(ChatSessionSerializer(sessions, many=True).data)

    @swagger_auto_schema(responses={201: ChatSessionSerializer})
    def post(self, request):
        session = ChatSession.objects.create(user=request.user)
        return Response(ChatSessionSerializer(session).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Delete a chat session by ID.",
        responses={204: "Chat session deleted successfully."}
    )
    def delete(self, request, session_id):
        """
        Deletes a chat session by ID.
        Only the user who created the session can delete it.
        """
        try:
            # Check if the session exists and belongs to the current user
            session = ChatSession.objects.get(id=session_id, user=request.user)
            session.delete()  # Delete the session
            return Response({"message": "Chat session deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Session not found or you do not have permission to delete it.'}, status=404)

class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['message'],
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'reply': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )}
    )
    def post(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Session not found'}, status=404)

        user_msg = request.data.get("message")
        if not user_msg:
            return Response({'error': 'Message is required'}, status=400)

        ChatMessage.objects.create(session=session, sender="user", content=user_msg)

        # Gather history of past messages
        past_messages = [
            {"role": "user" if m.sender == "user" else "assistant", "content": m.content}
            for m in session.messages.all()
        ] + [{"role": "user", "content": user_msg}]

        # Get the OpenAI client
        client = get_openai_client()

        # Send request to OpenAI with Markdown response request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Please respond using Markdown format, including headings, bullet points, bold text, etc."},
                {"role": "user", "content": user_msg}
            ] + past_messages
        )

        # Correct way to access the response content
        reply = response.choices[0].message["content"]
        ChatMessage.objects.create(session=session, sender="assistant", content=reply)

        return Response({"reply": reply})
