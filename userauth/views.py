from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from .models import User, OTPVerification, Profile

from .utils import send_otp_firebase

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # 🔐 Require authentication

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
        serializer = UserSerializer(data=request.data)
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

        user = authenticate(phone_number=phone_number, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Logout 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # 🔐 Require authentication

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # ✅ Blacklist the refresh token

            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        id_token = request.data.get("id_token")  # ✅ Frontend sends Firebase ID Token

        try:
            decoded_token = auth.verify_id_token(id_token)  # ✅ Verify token with Firebase
            user = User.objects.get(phone_number=phone_number)

            if decoded_token:
                user.is_active = True  # ✅ Activate account
                user.save()
                return Response({"message": "Phone number verified successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile