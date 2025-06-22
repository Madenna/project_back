from django.db import models
from django.contrib.auth import get_user_model
# class ContactMessage(models.Model):
#     CONTACT_METHODS = [
#         ('email', 'Email'),
#         ('phone', 'Phone'),
#     ]

#     method = models.CharField(max_length=10, choices=CONTACT_METHODS)
#     contact_value = models.CharField(max_length=255)
#     message = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.method} - {self.contact_value}"
    
User = get_user_model()

class ContactMessage(models.Model):
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]

    STATUS_CHOICES = [
        ('in_process', 'In Process'),
        ('solved', 'Solved'),
        ('declined', 'Declined'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_messages')
    contact_method = models.CharField(max_length=10, choices=CONTACT_METHOD_CHOICES)
    contact_detail = models.CharField(max_length=255)
    message = models.TextField(max_length=2000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_process')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.contact_method} | {self.contact_detail}'
