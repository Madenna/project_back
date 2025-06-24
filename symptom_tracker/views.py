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
from rest_framework.permissions import IsAuthenticated
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from datetime import datetime, timedelta
from django.http import HttpResponse
from reportlab.lib import colors

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
    
from reportlab.lib.utils import simpleSplit
from komekai.utils import analyze_prompt
class SymptomAIAnalyzeView(APIView):
    permission_classes = [IsAuthenticated]

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

        # Validate child ownership
        child = get_object_or_404(Child, id=child_id, parent=request.user)

        # Fetch symptoms in date range
        symptoms = SymptomEntry.objects.filter(
            child=child,
            date__range=[date_from, date_to]
        ).order_by('date')

        if not symptoms.exists():
            return Response({'message': 'No symptoms found in this period.'}, status=200)

        # Build prompt from symptoms
        summary_lines = [
            f"- {s.date.strftime('%Y-%m-%d')}: {s.symptom_name}, action: {s.action_taken or 'none'}"
            for s in symptoms
        ]

        prompt = (
            f"I am tracking symptoms for my child {child.full_name}. "
            f"Here are the symptoms recorded from {date_from} to {date_to}:\n\n"
            + "\n".join(summary_lines) +
            "\n\nCan you analyze this and give advice or suggestion?"
        )

        try:
            ai_reply = analyze_prompt(prompt)
        except Exception as e:
            return Response({'error': 'AI request failed', 'details': str(e)}, status=500)

        return Response({"advice": ai_reply}, status=200)
    
def draw_footer(canvas, width):
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(width - 2 * cm, 1.5 * cm, "balasteps.com")
    canvas.setFillColor(colors.black) 

class ExportSymptomsPDFView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Export symptoms of a selected child to PDF based on a time period.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["child_id", "period"],
            properties={
                "child_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the child"),
                "period": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["3_months", "6_months", "1_year", "custom"],
                    description="Time period for export"
                ),
                "custom_start": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Start date (required if period is 'custom')"
                ),
                "custom_end": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="End date (required if period is 'custom')"
                ),
            }
        ),
        responses={
            200: openapi.Response(description="Returns PDF file with symptoms"),
            400: openapi.Response(description="Invalid period or input"),
            401: openapi.Response(description="Unauthorized")
        }
    )
    def post(self, request):
        child_id = request.data.get('child_id')
        period = request.data.get('period')  
        custom_start = request.data.get('custom_start') 
        custom_end = request.data.get('custom_end')     

        child = get_object_or_404(Child, id=child_id, parent=request.user)

        end_date = datetime.today().date()

        if period == '3_months':
            start_date = end_date - timedelta(days=90)
        elif period == '6_months':
            start_date = end_date - timedelta(days=180)
        elif period == '1_year':
            start_date = end_date - timedelta(days=365)
        elif period == 'custom' and custom_start and custom_end:
            start_date = datetime.strptime(custom_start, '%Y-%m-%d').date()
            end_date = datetime.strptime(custom_end, '%Y-%m-%d').date()
        else:
            return HttpResponse("Invalid period", status=400)

        symptoms = SymptomEntry.objects.filter(
            child=child,
            date__range=(start_date, end_date)
        ).order_by('date')

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 2 * cm

        p.setFont("Helvetica-Bold", 14)
        p.drawString(2 * cm, y, f"Symptom Report for {child.full_name}")
        y -= 1 * cm
        p.setFont("Helvetica", 12)
        p.drawString(2 * cm, y, f"Date of birth: {child.birthday.strftime('%Y-%m-%d')}")
        y -= 1 * cm

        p.setFont("Helvetica", 11)
        for symptom in symptoms:
            text = f"{symptom.date} — {symptom.symptom_name} — {symptom.action_taken or 'No action'}"
            if y < 2 * cm:  
                p.showPage()
                y = height - 2 * cm
                p.setFont("Helvetica", 11)
            max_width = width - 4 * cm  
            wrapped_lines = simpleSplit(text, "Helvetica", 11, max_width)

            for line in wrapped_lines:
                if y < 2 * cm:
                    draw_footer(p, width)
                    p.showPage()
                    y = height - 2 * cm
                    p.setFont("Helvetica", 11)
                p.drawString(2 * cm, y, line)
                y -= 0.6 * cm

        draw_footer(p, width)
        p.showPage()
        p.save()

        buffer.seek(0)
        filename = f"{child.full_name}_symptoms.pdf"
        return HttpResponse(buffer, content_type='application/pdf', headers={'Content-Disposition': f'attachment; filename="{filename}"'})
    