import openai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer

openai.api_key = settings.OPENAI_API_KEY


class ChatSessionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
        return Response(ChatSessionSerializer(sessions, many=True).data)

    def post(self, request):
        session = ChatSession.objects.create(user=request.user)
        return Response(ChatSessionSerializer(session).data, status=status.HTTP_201_CREATED)


class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Session not found'}, status=404)

        user_msg = request.data.get("message")
        if not user_msg:
            return Response({'error': 'Message is required'}, status=400)

        ChatMessage.objects.create(session=session, sender="user", content=user_msg)

        # Get all past messages
        past_messages = [
            {"role": "user" if m.sender == "user" else "assistant", "content": m.content}
            for m in session.messages.all()
        ] + [{"role": "user", "content": user_msg}]

        # Get assistant response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты — заботливый ассистент платформы BalaSteps, помогаешь родителям особенных детей."}
            ] + past_messages
        )

        reply = response.choices[0].message["content"]
        ChatMessage.objects.create(session=session, sender="assistant", content=reply)

        return Response({"reply": reply})