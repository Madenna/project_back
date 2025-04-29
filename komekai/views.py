from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import openai 

openai.api_key = settings.OPENAI_API_KEY  

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

        past_messages = [
            {"role": "user" if m.sender == "user" else "assistant", "content": m.content}
            for m in session.messages.all()
        ] + [{"role": "user", "content": user_msg}]

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  
                messages=[
                    {"role": "system", "content": "Please respond using Markdown format, including headings, bullet points, bold text, etc."},
                    {"role": "user", "content": user_msg}
                ] + past_messages  
            )

            reply = response['choices'][0]['message']['content']
            ChatMessage.objects.create(session=session, sender="assistant", content=reply)

            return Response({"reply": reply})
        except Exception as e:
            return Response({"error": f"Failed to get response from OpenAI: {str(e)}"}, status=500)

class ChatSessionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            session.delete()  
            return Response({"message": "Chat session deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Session not found or you do not have permission to delete it.'}, status=status.HTTP_404_NOT_FOUND)