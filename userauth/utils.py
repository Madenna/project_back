from django.conf import settings
import firebase_admin
from firebase_admin import auth
import requests
import random
from .models import User, OTPVerification
import json
import urllib.parse
from django.core.mail import send_mail

# def create_firebase_id_token(phone_number):
#     try:
#         # Check if user exists on Firebase
#         try:
#             user = auth.get_user_by_phone_number(f"{phone_number}")
#         except firebase_admin.auth.UserNotFoundError:
#             # Create a new user if not found
#             user = auth.create_user(phone_number=f"{phone_number}")

#         # Generate a custom token
#         custom_token = auth.create_custom_token(user.uid)

#         # Exchange custom token for ID token using Firebase REST API
#         firebase_api_key = "AIzaSyCY22I94lUuBiZ1AnfiUPSK1A0qvVzw-8Q"  
#         url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={firebase_api_key}"
        
#         payload = {
#             "token": custom_token.decode('utf-8'),
#             "returnSecureToken": True
#         }
        
#         response = requests.post(url, json=payload)
#         id_token = response.json().get('idToken')
        
#         if id_token:
#             print("Firebase ID Token:", id_token)
#             return id_token
#         else:
#             print("Failed to get ID Token:", response.json())
#             return None

#     except Exception as e:
#         print("Error creating Firebase ID token:", str(e))
#         return None

# def send_otp_firebase(phone_number):
#     try:
#         return f"Firebase OTP must be sent from the frontend for {phone_number}." # returns message instructing frontend to handle OTP requests
#     except Exception as e:
#         return str(e)

# def send_otp_via_infobip(phone_number, request):
#     otp = random.randint(100000, 999999)
#     url = f"{settings.INFOBIP_BASE_URL}/sms/2/text/advanced" #4ewdyn.api.infobip.com
#     payload = {
#         "messages": [
#             {
#                 "from": "InfoSMS",
#                 "destinations": [{"to": phone_number}],
#                 "text": f"Your OTP is {otp}"
#             }
#         ]
#     }
#     headers = {
#         'Authorization': settings.INFOBIP_API_KEY,
#         'Content-Type': 'application/json'
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     print("Infobip Response:", response.status_code, response.text)  
#     if response.status_code == 200:
#         request.session['otp'] = otp  # ✅ Save OTP in session
#         request.session['phone_number'] = phone_number  # ✅ Save phone number too
#         print("Generated OTP:", otp)
#         return otp
#     else:
#         print("Error:", response.text)
#         return None
    
#     print("Generated OTP:", otp)

# SMSC_LOGIN = "madenna"        # SMSC.kz login
# SMSC_PASSWORD = "Madenna!2003"  # SMSC.kz password
# SMSC_SENDER = "SMSC.KZ"    # sender name (must be registered in SMSC.kz)
# SMSC_API_URL = "https://smsc.kz/sys/send.php"  # SMS sending endpoint
# SMSC_API_KEY = None  # Optional: API key if using API key authorization

# # Function to send OTP
# def send_otp_smsc(phone_number, otp_code):
#     # otp_code = str(random.randint(100000, 999999))
#     if not otp_code:
#         otp_code = str(random.randint(100000, 999999))
#     message = f"Your Balasteps OTP is {otp_code}"

#     params = {
#         "login": SMSC_LOGIN,
#         "psw": SMSC_PASSWORD,
#         "phones": phone_number,
#         "mes": message,
#         "fmt": 3,  # JSON response
#         "charset": "utf-8"
#     }
#     if SMSC_SENDER:
#         params["sender"] = SMSC_SENDER
#     # URL encode the parameters
#     url = SMSC_API_URL + "?" + urllib.parse.urlencode(params)

#     # Send SMS
#     response = requests.get(url)
#     print("SMSC Response:", response.text)
#     response_data = response.json()

#     print("SMSC Response:", response_data) 

#     # Handle different error codes
#     if "error" in response_data:
#         error_code = response_data.get("error_code")
#         if error_code == 2:
#             print("Invalid login or password.")
#         elif error_code == 8:
#             print("Message cannot be delivered.")
#         elif error_code == 6:
#             print("Message forbidden by text or sender name.")
#         else:
#             print(f"Unknown error (code {error_code}): {response_data['error']}")
#         return None

#     try:
#         user = User.objects.filter(phone_number=phone_number).first() or User.objects.filter(temp_phone_number=phone_number).first()

#         if user:
#             # Create or update the OTP record for the user
#             otp_record, created = OTPVerification.objects.update_or_create(
#                 user=user,
#                 defaults={'otp_code': otp_code}
#             )
#             print(f"Saved OTP: {otp_code} for {phone_number} (Created: {created})")
#         else:
#             print(f"User with phone number {phone_number} not found.")
#             return None

#     except Exception as e:
#         print(f"Error saving OTP: {str(e)}")
#         return None

#     print(f"Sent OTP: {otp_code} to {phone_number}")
#     return otp_code

# from .smsc_api import SMSC
from django.conf import settings

# def send_otp_smsc(phone_number, otp_code):
#     smsc = SMSC()
#     message = f"Your Balasteps OTP is {otp_code}"
#     response = smsc.send_sms(phone_number, message, sender=SMSC_SENDER)
#     print("SMSC Response:", response)  # Log response for debugging

#     if response[1].startswith("-"):
#         print(f"SMSC Error: {response}")
#         return None

#     return otp_code

# def send_otp_email(email):
#     """Generate OTP and send it via email."""
#     otp_code = str(random.randint(100000, 999999))

#     # Store OTP in the database
#     user = User.objects.get(email=email)
#     otp_verification, created = OTPVerification.objects.get_or_create(user=user)
#     otp_verification.otp_code = otp_code
#     otp_verification.save()

#     # Send email
#     subject = "Your BalaSteps Email OTP"
#     message = f"Your OTP for BalaSteps verification is: {otp_code}"
#     from_email = settings.DEFAULT_FROM_EMAIL

#     send_mail(subject, message, from_email, [email])

#     return otp_code  # Return OTP for debugging (remove this in production)
def send_verification_email(email, otp_code):
    subject = "Your Verification Code"
    message = f"Your OTP code is: {otp_code}. It is valid for 10 minutes."
    sender_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, sender_email, [email])
        print(f"Sent OTP: {otp_code} to {email}")
    except Exception as e:
        print(f"Email sending failed: {e}")

### ✅ Generate OTP Code ###
def generate_otp():
    return str(random.randint(100000, 999999))