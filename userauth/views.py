from firebase_admin import auth
from django.shortcuts import render

from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import (UserSerializer, LoginSerializer, RegisterSerializer, OTPVerificationSerializer,
    PasswordResetSerializer, ProfileSerializer, PhoneNumberChangeSerializer,
    VerifyNewPhoneNumberSerializer, RequestPhoneNumberChangeSerializer)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from .models import User, OTPVerification, Profile

from .utils import send_otp_firebase, create_firebase_id_token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        return Response({"message": "You are authenticated!"})

# Register User
class RegisterView(APIView):
    serializer_class = RegisterSerializer
    @swagger_auto_schema(request_body=RegisterSerializer)
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
    serializer_class = LoginSerializer
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            password = serializer.validated_data["password"]
            user = authenticate(username=phone_number, password=password)
            if user and user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Logout 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            }
        )
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    serializer_class = OTPVerificationSerializer
    @swagger_auto_schema(request_body=OTPVerificationSerializer)
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            id_token = serializer.validated_data["id_token"]
            auth.verify_id_token(id_token)
            user = User.objects.get(phone_number=phone_number)
            user.is_active = True
            user.save()
            return Response({"message": "Phone number verified successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(generics.RetrieveUpdateAPIView):
    from .serializers import ProfileSerializer
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        #new_phone_number = request.data.get("new_phone_number")
        user = request.user
        serializer = self.get_serializer(data=request.data, partial=True)

        # if new_phone_number:
        #     if user.phone_number != new_phone_number:
        #         user.temp_phone_number = new_phone_number
        #         user.save()
        #         otp_response = send_otp_firebase(new_phone_number)
        #         return Response({"message": "OTP sent to new phone number. Please verify.", "otp_response": otp_response}, status=status.HTTP_200_OK)
        #     else:
        #         return Response({"message": "New phone number is the same as the current one."}, status=status.HTTP_400_BAD_REQUEST)

        # return super().update(request, *args, **kwargs)
        if serializer.is_valid():
            new_phone_number = serializer.validated_data.get("new_phone_number", None)

            # Handle phone number change with OTP
            if new_phone_number:
                if user.phone_number != new_phone_number:
                    user.temp_phone_number = new_phone_number
                    user.save()
                    otp_response = send_otp_firebase(new_phone_number)
                    return Response({
                        "message": "OTP sent to new phone number. Please verify.",
                        "otp_response": otp_response
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "New phone number is the same as the current one."
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Save other profile details if no phone number change is requested
            profile = self.get_object()
            if isinstance(profile, Response):
                # If get_object returned an error Response
                return profile

            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer
    @swagger_auto_schema(request_body=PasswordResetSerializer)
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        # phone_number = request.data.get("phone_number")
        # new_password = request.data.get("new_password")

        # try:
        #     user = User.objects.get(phone_number=phone_number)
        #     user.set_password(new_password)
        #     user.save()
        #     return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        # except User.DoesNotExist:
        #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            new_password = serializer.validated_data["new_password"]
            id_token = serializer.validated_data.get("id_token")  # Firebase ID Token for OTP Verification

            # Check if the user exists
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Verify OTP using Firebase
            try:
                decoded_token = auth.verify_id_token(id_token)
                if decoded_token.get("phone_number") == phone_number:
                    # Reset password if verification is successful
                    user.set_password(new_password)
                    user.save()
                    return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Phone number does not match the verified token."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyNewPhoneNumberView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VerifyNewPhoneNumberSerializer
    @swagger_auto_schema(request_body=VerifyNewPhoneNumberSerializer)
    def post(self, request):
        serializer = VerifyNewPhoneNumberSerializer(data=request.data)
        # if serializer.is_valid():
        #     new_phone_number = serializer.validated_data["new_phone_number"]
        #     id_token = serializer.validated_data["id_token"]
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     decoded_token = auth.verify_id_token(id_token)  # Verify token with Firebase
        #     user = request.user

        #     if decoded_token.get("phone_number") == new_phone_number:
        #         user.phone_number = new_phone_number
        #         user.temp_phone_number = None  # Clear temporary field
        #         user.save()
        #         return Response({"message": "Phone number updated successfully."}, status=status.HTTP_200_OK)
        #     else:
        #         return Response({"error": "Phone number does not match the verified token."}, status=status.HTTP_400_BAD_REQUEST)
            
        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            new_phone_number = serializer.validated_data["new_phone_number"]
            id_token = serializer.validated_data["id_token"]
            try:
                decoded_token = auth.verify_id_token(id_token)
                user = request.user

                if decoded_token.get("phone_number") == new_phone_number:
                    user.phone_number = new_phone_number
                    user.temp_phone_number = None
                    user.save()
                    return Response({
                        "message": "Phone number updated successfully."
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "error": "Phone number does not match the verified token."
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RequestPhoneNumberChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RequestPhoneNumberChangeSerializer
    @swagger_auto_schema(request_body=RequestPhoneNumberChangeSerializer)
    def post(self, request):
        serializer = RequestPhoneNumberChangeSerializer(data=request.data)
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

