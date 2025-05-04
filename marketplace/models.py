from django.db import models
from django.conf import settings
import uuid

class EquipmentCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class AvailabilityType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)  # sale, donation, exchange

    def __str__(self):
        return self.name
    
class ConditionType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)  # 'New', 'Gently Used', etc.
    def __str__(self):
        return self.name

class EquipmentItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='equipment_items'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        EquipmentCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='items'
    )
    condition = models.ForeignKey(
        ConditionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment_items'
    )
    available_for = models.ManyToManyField(
        AvailabilityType,
        related_name='items',
        blank=True
    )
    location = models.CharField(max_length=100)
    contact_method = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class EquipmentPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(
        EquipmentItem,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image_url = models.URLField()  # Cloudinary image URLs

    def __str__(self):
        return f"Photo for {self.item.name}"
