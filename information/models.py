from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
import uuid

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class InformationItem(models.Model):
    POST_TYPES = (
        ("news", "News"),
        ("specialist", "Specialist"),
        ("center", "Therapy Center"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=POST_TYPES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = CloudinaryField("image", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.type})"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    info = models.ForeignKey(InformationItem, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # 1–5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.full_name} on {self.info.title}"
