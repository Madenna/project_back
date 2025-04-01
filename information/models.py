from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
import uuid

class InfoTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class InfoCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class InfoPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    photo = models.URLField(blank=True, null=True)  # Using Cloudinary 
    category = models.ForeignKey(InfoCategory, on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField(InfoTag, blank=True, related_name="info_posts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class InfoComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(InfoPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="info_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_info_comments', blank=True)

    def __str__(self):
        return f"Comment by {self.user.full_name} on {self.post.title}"
