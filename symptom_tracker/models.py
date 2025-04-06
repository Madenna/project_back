from django.db import models
from django.conf import settings
import uuid

class SymptomEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child = models.ForeignKey("userauth.Child", on_delete=models.CASCADE, related_name="symptom_entries")
    symptom_name = models.CharField(max_length=255)
    action_taken = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symptom_name} for {self.child.full_name} on {self.date}"
