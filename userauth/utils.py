from django.conf import settings
import random
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email, otp_code):
    subject = "Balasteps: Your Verification Code"
    message = f"Your Balasteps OTP code is: {otp_code}. It is valid for 10 minutes."
    sender_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, sender_email, [email])
        print(f"Sent OTP: {otp_code} to {email}")
    except Exception as e:
        print(f"Email sending failed: {e}")

def generate_otp():
    return str(random.randint(100000, 999999))

import cloudinary.uploader
import logging
logger = logging.getLogger(__name__)
from rest_framework import serializers

def upload_to_cloudinary(file):
    try:
        result = cloudinary.uploader.upload(file)
        return result['secure_url']
    except Exception as e:
        logger.error(f"Cloudinary upload failed: {e}")
        raise serializers.ValidationError("Upload failed. Please try again.")
