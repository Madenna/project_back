from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
import uuid

class InfoTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Specialist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField()
    photo = models.URLField(blank=True, null=True)  # Cloudinary URL
    tags = models.ManyToManyField(InfoTag, blank=True, related_name="specialists")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        ratings = self.specialist_comments.filter(rating__isnull=False)
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 2)
        return None

class TherapyCenter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    photo = models.URLField(blank=True, null=True)  # Cloudinary URL
    tags = models.ManyToManyField(InfoTag, blank=True, related_name="therapy_centers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        ratings = self.center_comments.filter(rating__isnull=False)
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 2)
        return None

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    photo = models.URLField(blank=True, null=True)  # Cloudinary URL
    tags = models.ManyToManyField(InfoTag, blank=True, related_name="news")
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.title

class SpecialistComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name="specialist_comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="specialist_comments")
    content = models.TextField()
    rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_specialist_comments', blank=True)

    def __str__(self):
        return f"Specialist Comment by {self.user.full_name} on {self.specialist.name}"
    
class SpecialistReply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(SpecialistComment, on_delete=models.CASCADE, related_name="specialist_replies")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='specialist_replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_specialist_replies", blank=True)

    def __str__(self):
        return f"Reply by {self.user.full_name} on specialist comment {self.comment.id}"

    class Meta:
        ordering = ['created_at']

class TherapyCenterComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    center = models.ForeignKey(TherapyCenter, on_delete=models.CASCADE, related_name="center_comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="center_comments")
    content = models.TextField()
    rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_center_comments', blank=True)

    def __str__(self):
        return f"Center Comment by {self.user.full_name} on {self.center.name}"

class TherapyCenterReply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(TherapyCenterComment, on_delete=models.CASCADE, related_name="center_replies")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='center_replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_center_replies", blank=True)

    def __str__(self):
        return f"Reply by {self.user.full_name} on therapy center comment {self.comment.id}"

    class Meta:
        ordering = ['created_at']

class NewsComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="news_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_news_comments', blank=True)

    def __str__(self):
        return f"News Comment by {self.user.full_name} on {self.news.title}"

class NewsReply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(NewsComment, on_delete=models.CASCADE, related_name="news_replies")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='news_replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_news_replies", blank=True)

    def __str__(self):
        return f"Reply by {self.user.full_name} on news comment {self.comment.id}"

    class Meta:
        ordering = ['created_at']