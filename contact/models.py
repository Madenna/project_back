from django.db import models

class ContactMessage(models.Model):
    CONTACT_METHODS = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]

    method = models.CharField(max_length=10, choices=CONTACT_METHODS)
    contact_value = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} - {self.contact_value}"
