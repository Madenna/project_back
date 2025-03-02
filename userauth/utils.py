from django.conf import settings
import firebase_admin
from firebase_admin import auth
import requests

def create_firebase_id_token(phone_number):
    try:
        # Check if user exists on Firebase
        try:
            user = auth.get_user_by_phone_number(f"{phone_number}")
        except firebase_admin.auth.UserNotFoundError:
            # Create a new user if not found
            user = auth.create_user(phone_number=f"{phone_number}")

        # Generate a custom token
        custom_token = auth.create_custom_token(user.uid)

        # Exchange custom token for ID token using Firebase REST API
        firebase_api_key = "AIzaSyCY22I94lUuBiZ1AnfiUPSK1A0qvVzw-8Q"  
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={firebase_api_key}"
        
        payload = {
            "token": custom_token.decode('utf-8'),
            "returnSecureToken": True
        }
        
        response = requests.post(url, json=payload)
        id_token = response.json().get('idToken')
        
        if id_token:
            print("Firebase ID Token:", id_token)
            return id_token
        else:
            print("Failed to get ID Token:", response.json())
            return None

    except Exception as e:
        print("Error creating Firebase ID token:", str(e))
        return None

def send_otp_firebase(phone_number):
    try:
        return f"Firebase OTP must be sent from the frontend for {phone_number}." # returns message instructing frontend to handle OTP requests
    except Exception as e:
        return str(e)

