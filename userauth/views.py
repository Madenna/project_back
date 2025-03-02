from firebase_admin import auth
from django.shortcuts import render

from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import (UserSerializer, LoginSerializer, RegisterSerializer, OTPVerificationSerializer,
    PasswordResetSerializer, ProfileSerializer, PhoneNumberChangeSerializer,
    VerifyNewPhoneNumberSerializer)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from .models import User, OTPVerification, Profile

from .utils import send_otp_firebase, create_firebase_id_token

User = get_user_model()

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        return Response({"message": "You are authenticated!"})

# Register User
class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        
        # Check if user already exists
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "A user with this phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Continue with registration
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # User must verify OTP first
            user.save()

            # Notify the frontend that Firebase should handle OTP
            otp_response = send_otp_firebase(user.phone_number)

            return Response({"message": "OTP must be sent from frontend", "otp_response": otp_response}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Login and get JWT token
class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        user = authenticate(phone_number=phone_number, password=password)  #may be username=phone_number (???)
 
        if user is not None:
            if user.is_active:  # Check if the user is active
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
            else:
                return Response({"error": "User is not verified. Please verify your phone number."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Logout 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token

            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        id_token = request.data.get("id_token")  # Frontend sends Firebase ID Token

        try:
            decoded_token = auth.verify_id_token(id_token)  # Verify token with Firebase
            user = User.objects.get(phone_number=phone_number)

            if decoded_token:
                user.is_active = True  # Activate account
                user.save()
                return Response({"message": "Phone number verified successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(generics.RetrieveUpdateAPIView):
    from .serializers import ProfileSerializer
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    def update(self, request, *args, **kwargs):
        new_phone_number = request.data.get("new_phone_number")
        user = request.user

        if new_phone_number:
            if user.phone_number != new_phone_number:
                user.temp_phone_number = new_phone_number
                user.save()
                otp_response = send_otp_firebase(new_phone_number)
                return Response({"message": "OTP sent to new phone number. Please verify.", "otp_response": otp_response}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "New phone number is the same as the current one."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    
class PasswordResetView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        new_password = request.data.get("new_password")

        try:
            user = User.objects.get(phone_number=phone_number)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class VerifyNewPhoneNumberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        new_phone_number = request.data.get("new_phone_number")
        id_token = request.data.get("id_token")  # Firebase ID Token

        try:
            decoded_token = auth.verify_id_token(id_token)  # Verify token with Firebase
            user = request.user

            if decoded_token.get("phone_number") == new_phone_number:
                user.phone_number = new_phone_number
                user.temp_phone_number = None  # Clear temporary field
                user.save()
                return Response({"message": "Phone number updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Phone number does not match the verified token."}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class RequestPhoneNumberChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PhoneNumberChangeSerializer(data=request.data)
        if serializer.is_valid():
            new_phone_number = serializer.validated_data["new_phone_number"]
            user = request.user

            if user.phone_number != new_phone_number:
                user.temp_phone_number = new_phone_number
                user.save()
                otp_response = send_otp_firebase(new_phone_number)
                return Response({"message": "OTP sent to new phone number. Please verify.", "otp_response": otp_response}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "New phone number is the same as the current one."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

