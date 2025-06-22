from rest_framework import generics, permissions
from .models import SymptomEntry
from .serializers import SymptomEntrySerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import PermissionDenied
import requests
from userauth.models import Child

class SymptomEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = SymptomEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure the query only returns entries for the logged-in user's children
        return SymptomEntry.objects.filter(child__parent=self.request.user)

    def perform_create(self, serializer):
        # Ensure the user can only create symptom entries for their own children
        child = serializer.validated_data['child']
        if child.parent != self.request.user:
            raise PermissionDenied("You can only add symptoms for your own child.")
        serializer.save()

    @swagger_auto_schema(
        operation_description="List all symptom entries for the current parent user.",
        responses={200: SymptomEntrySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=SymptomEntrySerializer,
        operation_description="Create a new symptom entry for a selected child.",
        responses={201: SymptomEntrySerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SymptomEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SymptomEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return SymptomEntry.objects.filter(child__parent=self.request.user)

    @swagger_auto_schema(
        operation_description="Retrieve a specific symptom entry.",
        responses={200: SymptomEntrySerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=SymptomEntrySerializer,
        operation_description="Update an existing symptom entry.",
        responses={200: SymptomEntrySerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific symptom entry.",
        responses={204: "Deleted successfully."}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class SymptomAIAnalyzeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Analyze symptoms for selected child using AI assistant Komekai",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['child_id', 'date_from', 'date_to'],
            properties={
                'child_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the child"),
                'date_from': openapi.Schema(type=openapi.TYPE_STRING, format='date', description="Start date"),
                'date_to': openapi.Schema(type=openapi.TYPE_STRING, format='date', description="End date"),
            }
        ),
        responses={
            200: openapi.Response(description="AI-generated health advice"),
            400: "Validation error",
            500: "Server or AI error"
        }
    )
    def post(self, request):
        child_id = request.data.get('child_id')
        date_from = request.data.get('date_from')
        date_to = request.data.get('date_to')

        if not all([child_id, date_from, date_to]):
            return Response({'error': 'child_id, date_from, and date_to are required.'}, status=400)

        child = get_object_or_404(Child, id=child_id, parent=request.user)
        symptoms = SymptomEntry.objects.filter(
            child=child,
            date__range=[date_from, date_to]
        ).order_by('date')

        if not symptoms.exists():
            return Response({'message': 'No symptoms found in this period.'}, status=200)

        summary_lines = []
        for s in symptoms:
            summary_lines.append(f"- {s.date}: {s.symptom_name}, action: {s.action_taken or 'none'}")

        prompt = (
            f"I am tracking symptoms for my child {child.name}. "
            f"Here are the symptoms recorded from {date_from} to {date_to}:\n\n"
            + "\n".join(summary_lines) +
            "\n\nCan you analyze this and give advice or suggestion?"
        )

        session_resp = requests.post(
            "https://project-back-81mh.onrender.com/komekai/sessions/",
            headers={"Authorization": f"Bearer {request.auth}"},
        )
        if session_resp.status_code not in [200, 201]:
            return Response({'error': 'Failed to create Komekai session'}, status=500)
        
        session_id = session_resp.json().get("id")

        message_resp = requests.post(
            f"http://localhost:8000/api/komekai/sessions/{session_id}/message/",
            json={"message": prompt},
            headers={"Authorization": f"Bearer {request.auth}"},
        )

        if message_resp.status_code != 200:
            return Response({'error': 'AI response failed'}, status=500)

        ai_reply = message_resp.json().get("reply")
        return Response({"advice": ai_reply}, status=200)