from django.conf import settings
import firebase_admin
from firebase_admin import auth

def send_otp_firebase(phone_number):
    try:
        return f"Firebase OTP must be sent from the frontend for {phone_number}." # returns message instructing frontend to handle OTP requests
    except Exception as e:
        return str(e)

