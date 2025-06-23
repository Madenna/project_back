# donations/models.py
import random
import string
from io import BytesIO
from datetime import date
from django.db import models
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from cloudinary.uploader import upload
from cloudinary.models import CloudinaryField
import qrcode
from decimal import Decimal

User = get_user_model()
from userauth.models import Child

def generate_unique_kaspi_code():
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        if not DonationRequest.objects.filter(kaspi_code=code).exists():
            return code

class DonationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation_requests')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='donations')
    purpose = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    donated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kaspi_code = models.CharField(max_length=6, unique=True, blank=True)
    kaspi_qr = CloudinaryField('kaspi_qr', blank=True, null=True)
    deadline = models.DateField()
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.kaspi_code:
            self.kaspi_code = generate_unique_kaspi_code()

        if not self.kaspi_qr and self.kaspi_code:
            qr = qrcode.make(f"https://kaspi.kz/pay/{self.kaspi_code}")
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)
            result = upload(buffer, folder="kaspi_qr", public_id=f"kaspi_{self.kaspi_code}")
            self.kaspi_qr = result["public_id"]

        super().save(*args, **kwargs)

    def remaining_amount(self):
        return max(self.goal_amount - self.donated_amount, Decimal('0'))

    def is_expired(self):
        return date.today() > self.deadline

    def __str__(self):
        return f"{self.child.name} — {self.purpose}"

class DonationConfirmation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    donation_request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)
    donated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.donation_request.donated_amount += self.amount
        self.donation_request.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Donation {self.amount}₸ to {self.donation_request.id}"
    
class DonationPhoto(models.Model):
    donation_request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='photos')
    image = CloudinaryField('donation_photo')

    def __str__(self):
        return f"Photo for request {self.donation_request.id}"