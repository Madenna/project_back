# from firebase_admin import auth
# from django.shortcuts import render
# import random

# from django.contrib.auth import get_user_model

# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import status
# from .serializers import (UserSerializer, LoginSerializer, RegisterSerializer, OTPVerificationSerializer,
#     PasswordResetSerializer, ProfileSerializer, PhoneNumberChangeSerializer,
#     VerifyNewPhoneNumberSerializer, RequestPhoneNumberChangeSerializer, OTPRequestSerializer, VerifyEmailSerializer)

# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from django.contrib.auth import authenticate
# from .models import User, OTPVerification, Profile, VerificationOTP

# from .utils import send_otp_firebase, create_firebase_id_token
# from .utils import send_otp_via_infobip, send_otp_smsc

# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# from django.core.mail import send_mail

# User = get_user_model()

# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]  # Require authentication

#     def get(self, request):
#         return Response({"message": "You are authenticated!"})

# # Register User
# # class RegisterView(APIView):
# #     serializer_class = RegisterSerializer
# #     @swagger_auto_schema(request_body=RegisterSerializer)
# #     def post(self, request):
# #         phone_number = request.data.get("phone_number")
        
# #         # Check if user already exists
# #         # Check if a non-verified user exists with this phone number
# #         existing_user = User.objects.filter(phone_number=phone_number).first()

# #         if existing_user:
# #             if not existing_user.is_active:
# #                 # Delete the non-verified user and proceed with registration
# #                 existing_user.delete()
# #             else:
# #                 return Response({"error": "A user with this phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)


# #         # Continue with registration
# #         serializer = RegisterSerializer(data=request.data)

# #         if serializer.is_valid():
# #             user = serializer.save()
# #             user.set_password(user.password)  # Hash the password before saving
# #             user.is_active = False  # User must verify OTP first
# #             user.save()

# #             # Generate OTP and save it in OTPVerification model
# #             otp_verification = OTPVerification.objects.create(user=user)
# #             otp_verification.generate_otp()

# #             # Send OTP via SMSC
# #             send_otp_smsc(user.phone_number, otp_verification.otp_code)

# #             # otp_code = send_otp_smsc(user.phone_number)
# #             # if not otp_code:
# #             #     return Response({"error": "Failed to send OTP. Try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #             # # Save OTP in the database (assuming you have an OTPVerification model)
# #             # OTPVerification.objects.create(phone_number=user.phone_number, otp_code=otp_code)
# #             print("OTP Sent to:", user.phone_number)
# #             print("Generated OTP:", otp_verification.otp_code)

# #             return Response({"message": "OTP sent successfully"}, status=status.HTTP_201_CREATED)
        
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # class RegisterView(APIView):
# #     serializer_class = RegisterSerializer
# #     @swagger_auto_schema(request_body=RegisterSerializer)
# #     def post(self, request):
# #         phone_number = request.data.get("phone_number")
# #         existing_user = User.objects.filter(phone_number=phone_number).first()

# #         if existing_user:
# #             if not existing_user.is_active:
# #                 existing_user.delete()
# #             else:
# #                 return Response({"error": "A user with this phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

# #         serializer = RegisterSerializer(data=request.data)

# #         if serializer.is_valid():
# #             user = serializer.save()
# #             user.set_password(user.password)  # Hash the password
# #             user.is_active = False  # User must verify OTP first
# #             user.save()

# #             # Generate and send OTP
# #             otp_verification, created = OTPVerification.objects.get_or_create(user=user)
# #             otp_verification.generate_otp()

# #             if not send_otp_smsc(user.phone_number, otp_verification.otp_code):
# #                 return Response({"error": "Failed to send OTP. Try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #             return Response({"message": "OTP sent successfully"}, status=status.HTTP_201_CREATED)

# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# # Login and get JWT token
# class LoginView(APIView):
#     serializer_class = LoginSerializer
#     @swagger_auto_schema(request_body=LoginSerializer)
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             phone_number = serializer.validated_data["phone_number"]
#             password = serializer.validated_data["password"]
#             user = authenticate(username=phone_number, password=password)
#             if user and user.is_active:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     "refresh": str(refresh),
#                     "access": str(refresh.access_token)
#                 })
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# # Logout 
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]  # Require authentication
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
#             }
#         )
#     )
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()  # Blacklist the refresh token

#             return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# # class VerifyOTPView(APIView):
# #     serializer_class = OTPVerificationSerializer
# #     @swagger_auto_schema(request_body=OTPVerificationSerializer)
# #     def post(self, request):
# #         serializer = OTPVerificationSerializer(data=request.data)
# #         if serializer.is_valid():
# #             phone_number = serializer.validated_data["phone_number"]
# #             id_token = serializer.validated_data["id_token"]
# #             auth.verify_id_token(id_token)
# #             user = User.objects.get(phone_number=phone_number)
# #             user.is_active = True
# #             user.save()
# #             return Response({"message": "Phone number verified successfully"}, status=status.HTTP_200_OK)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# class ProfileView(generics.RetrieveUpdateAPIView):
#     from .serializers import ProfileSerializer
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user.profile

#     def update(self, request, *args, **kwargs):
#         #new_phone_number = request.data.get("new_phone_number")
#         user = request.user
#         serializer = self.get_serializer(data=request.data, partial=True)

#         # if new_phone_number:
#         #     if user.phone_number != new_phone_number:
#         #         user.temp_phone_number = new_phone_number
#         #         user.save()
#         #         otp_response = send_otp_firebase(new_phone_number)
#         #         return Response({"message": "OTP sent to new phone number. Please verify.", "otp_response": otp_response}, status=status.HTTP_200_OK)
#         #     else:
#         #         return Response({"message": "New phone number is the same as the current one."}, status=status.HTTP_400_BAD_REQUEST)

#         # return super().update(request, *args, **kwargs)
#         if serializer.is_valid():
#             new_phone_number = serializer.validated_data.get("new_phone_number", None)

#             # Handle phone number change with OTP
#             if new_phone_number:
#                 if user.phone_number != new_phone_number:
#                     user.temp_phone_number = new_phone_number
#                     user.save()
#                     otp_response = send_otp_firebase(new_phone_number)
#                     return Response({
#                         "message": "OTP sent to new phone number. Please verify.",
#                         "otp_response": otp_response
#                     }, status=status.HTTP_200_OK)
#                 else:
#                     return Response({
#                         "message": "New phone number is the same as the current one."
#                     }, status=status.HTTP_400_BAD_REQUEST)

#             # Save other profile details if no phone number change is requested
#             profile = self.get_object()
#             if isinstance(profile, Response):
#                 # If get_object returned an error Response
#                 return profile

#             serializer = self.get_serializer(profile, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# class PasswordResetView(APIView):
#     serializer_class = PasswordResetSerializer
#     @swagger_auto_schema(request_body=PasswordResetSerializer)
#     def post(self, request):
#         serializer = PasswordResetSerializer(data=request.data)
#         phone_number = request.data.get("phone_number")
#         new_password = request.data.get("new_password")

#         # try:
#         #     user = User.objects.get(phone_number=phone_number)
#         #     user.set_password(new_password)
#         #     user.save()
#         #     return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
#         # except User.DoesNotExist:
#         #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         if serializer.is_valid():
#             # phone_number = serializer.validated_data["phone_number"]
#             # new_password = serializer.validated_data["new_password"]
#             # id_token = serializer.validated_data.get("id_token")  # Firebase ID Token for OTP Verification

#             # Check if the user exists
#             try:
#                 user = User.objects.get(phone_number=phone_number)
#                 user.set_password(new_password)  # Hash the new password
#                 user.save()
#                 return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#             # # Verify OTP using Firebase
#             # try:
#             #     decoded_token = auth.verify_id_token(id_token)
#             #     if decoded_token.get("phone_number") == phone_number:
#             #         # Reset password if verification is successful
#             #         user.set_password(new_password)
#             #         user.save()
#             #         return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
#             #     else:
#             #         return Response({"error": "Phone number does not match the verified token."}, status=status.HTTP_400_BAD_REQUEST)
#             # except Exception as e:
#             #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # class VerifyNewPhoneNumberView(APIView):
# #     permission_classes = [permissions.IsAuthenticated]
# #     serializer_class = VerifyNewPhoneNumberSerializer
# #     @swagger_auto_schema(request_body=VerifyNewPhoneNumberSerializer)
# #     def post(self, request):
# #         serializer = VerifyNewPhoneNumberSerializer(data=request.data)
# #         if serializer.is_valid():
# #             new_phone_number = serializer.validated_data["new_phone_number"]
# #             user_otp = serializer.validated_data["otp"]
# #             if not new_phone_number or not user_otp:
# #                 return Response({"error": "New phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

# #             try:
# #                 # Check if OTP is correct for the new phone number
# #                 print(f"Checking OTP for {new_phone_number}...")
# #                 otp_verification = OTPVerification.objects.filter(user=request.user).first()
# #                 print("OTP Verification Record:", otp_verification)
# #                 if str(user_otp) == str(otp_verification.otp_code):
# #                     # Update phone number if OTP is correct
# #                     user = request.user
# #                     user.phone_number = new_phone_number
# #                     user.temp_phone_number = None  # Clear temporary field
# #                     user.save()

# #                     # Delete OTP record after successful verification
# #                     otp_verification.delete()

# #                     return Response({
# #                         "message": "Phone number updated successfully."
# #                     }, status=status.HTTP_200_OK)
# #                 else:
# #                     return Response({
# #                         "error": "Invalid OTP"
# #                     }, status=status.HTTP_400_BAD_REQUEST)
# #             except OTPVerification.DoesNotExist:
# #                 return Response({
# #                     "error": "OTP not found or expired"
# #                 }, status=status.HTTP_404_NOT_FOUND)
# #             except Exception as e:
# #                 return Response({
# #                     "error": str(e)
# #                 }, status=status.HTTP_400_BAD_REQUEST)

# #         # If serializer is not valid
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# class VerifyNewPhoneNumberView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VerifyNewPhoneNumberSerializer

#     @swagger_auto_schema(request_body=VerifyNewPhoneNumberSerializer)
#     def post(self, request):
#         serializer = VerifyNewPhoneNumberSerializer(data=request.data)
        
#         # Validate request body
#         if serializer.is_valid():
#             new_phone_number = serializer.validated_data["new_phone_number"]
#             user_otp = serializer.validated_data["otp"]

#             if not new_phone_number or not user_otp:
#                 return Response({"error": "New phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

#             try:
#                 user = request.user

#                 # Check if the temporary phone number matches the request
#                 if user.temp_phone_number != new_phone_number:
#                     return Response({
#                         "error": "Temporary phone number mismatch."
#                     }, status=status.HTTP_400_BAD_REQUEST)

#                 # Check if OTP exists for this user
#                 otp_verification = OTPVerification.objects.filter(user=user).first()
#                 if not otp_verification:
#                     return Response({
#                         "error": "OTP not found or expired"
#                     }, status=status.HTTP_404_NOT_FOUND)

#                 # Compare OTPs
#                 if str(user_otp) == str(otp_verification.otp_code):
#                     # ✅ Update phone number if OTP is correct
#                     user.phone_number = new_phone_number
#                     user.temp_phone_number = None  # Clear temporary field
#                     user.save()

#                     # Delete OTP record after successful verification
#                     otp_verification.delete()

#                     return Response({
#                         "message": "Phone number updated successfully."
#                     }, status=status.HTTP_200_OK)
#                 else:
#                     return Response({
#                         "error": "Invalid OTP"
#                     }, status=status.HTTP_400_BAD_REQUEST)

#             except Exception as e:
#                 return Response({
#                     "error": str(e)
#                 }, status=status.HTTP_400_BAD_REQUEST)

#         # If serializer is not valid
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RequestPhoneNumberChangeView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = RequestPhoneNumberChangeSerializer
#     @swagger_auto_schema(request_body=RequestPhoneNumberChangeSerializer)
#     def post(self, request):
#         serializer = RequestPhoneNumberChangeSerializer(data=request.data)
#         if serializer.is_valid():
#             new_phone_number = serializer.validated_data["new_phone_number"]
#             user = request.user

#             print("Attempting to send OTP to:", new_phone_number)

#             if user.phone_number != new_phone_number:
#                 otp = str(random.randint(100000, 999999))
#                 send_otp_smsc(new_phone_number, otp)  # Send OTP

#                 print("OTP sent to:", new_phone_number)  # Print confirmation
#                 return Response({"message": "OTP sent to new phone number. Please verify."}, status=status.HTTP_200_OK)
#                 # user.temp_phone_number = new_phone_number
#                 # user.save()
#                 # otp_response = send_otp_firebase(new_phone_number)
#                 # return Response({"message": "OTP sent to new phone number. Please verify.", "otp_response": otp_response}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"message": "New phone number is the same as the current one."}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # class SendOTPView(APIView):
# #     serializer_class = OTPRequestSerializer
# #     @swagger_auto_schema(request_body=OTPRequestSerializer)
# #     def post(self, request):
# #         serializer = OTPRequestSerializer(data=request.data)
# #         if serializer.is_valid():
# #             phone_number = serializer.validated_data["phone_number"]

# #             # Generate and send OTP
# #             otp_code = send_otp_smsc(phone_number)
# #             if otp_code:
# #                 return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
# #             else:
# #                 return Response({"error": "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #         # If request body is invalid
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# # class VerifyOTPView(APIView):
# #     def post(self, request):
# #         phone_number = request.data.get("phone_number")
# #         user_otp = request.data.get("otp")

# #         if not phone_number or not user_otp:
# #             return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

# #         try:
# #             # Get OTP from the database
# #             otp_record = OTPVerification.objects.filter(phone_number=phone_number).last()

# #             if otp_record:
# #                 # Check if the OTP matches
# #                 if str(user_otp) == str(otp_record.otp_code):
# #                     # Activate user if OTP is correct
# #                     user = User.objects.get(phone_number=phone_number)
# #                     user.is_active = True
# #                     user.save()

# #                     # Delete the OTP record after successful verification
# #                     otp_record.delete()

# #                     return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
# #                 else:
# #                     return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
# #             else:
# #                 return Response({"error": "OTP expired or invalid request"}, status=status.HTTP_400_BAD_REQUEST)

# #         except User.DoesNotExist:
# #             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# #         except Exception as e:
# #             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # class VerifyOTPView(APIView):
# #     serializer_class = OTPVerificationSerializer 
# #     @swagger_auto_schema(request_body=OTPVerificationSerializer)
# #     def post(self, request):
# #         serializer = OTPVerificationSerializer(data=request.data)
# #         user_otp = request.data.get("otp")
# #         phone_number = request.data.get("phone_number")
# #         if not phone_number or not user_otp:
# #             return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

# #         try:
# #             # Get user by phone number
# #             user = User.objects.get(phone_number=phone_number)
# #             otp_verification = OTPVerification.objects.get(user=user)

# #             if str(user_otp) == str(otp_verification.otp_code):
# #                 user.is_active = True  # Activate user
# #                 user.save()
# #                 otp_verification.delete()  # Delete OTP record after successful verification
# #                 return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
# #             else:
# #                 return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

# #         except User.DoesNotExist:
# #             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
# #         except OTPVerification.DoesNotExist:
# #             return Response({"error": "OTP not found or expired"}, status=status.HTTP_404_NOT_FOUND)

# # class VerifyOTPView(APIView):
# #     serializer_class = OTPVerificationSerializer
# #     @swagger_auto_schema(request_body=OTPVerificationSerializer)
# #     def post(self, request):
# #         serializer = OTPVerificationSerializer(data=request.data)
# #         # user_otp = request.data.get("otp")
# #         # phone_number = request.data.get("phone_number")

# #         # if not phone_number or not user_otp:
# #         #     return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

# #         # try:
# #         #     user = User.objects.get(phone_number=phone_number)
# #         #     otp_verification = OTPVerification.objects.get(user=user)

# #         #     if str(user_otp) == str(otp_verification.otp_code):
# #         #         user.is_active = True
# #         #         user.save()
# #         #         otp_verification.delete()  # Delete OTP after verification
# #         #         return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
# #         #     else:
# #         #         return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
# #         # except (User.DoesNotExist, OTPVerification.DoesNotExist):
# #         #     return Response({"error": "User or OTP not found"}, status=status.HTTP_404_NOT_FOUND)
# #         if serializer.is_valid():
# #             phone_number = serializer.validated_data["phone_number"]
# #             user_otp = serializer.validated_data["otp"]

# #             if not phone_number or not user_otp:
# #                 return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

# #             try:
# #                 # Get user by phone number
# #                 user = User.objects.get(phone_number=phone_number)
# #                 otp_verification = OTPVerification.objects.get(user=user)

# #                 if str(user_otp) == str(otp_verification.otp_code):
# #                     user.is_active = True  # Activate user
# #                     user.save()
# #                     otp_verification.delete()  # Delete OTP record after successful verification
# #                     return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
# #                 else:
# #                     return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

# #             except User.DoesNotExist:
# #                 return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
# #             except OTPVerification.DoesNotExist:
# #                 return Response({"error": "OTP not found or expired"}, status=status.HTTP_404_NOT_FOUND)
# #         else:
# #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from userauth.utils import send_otp_email
# class RegisterView(APIView):
#     serializer_class = RegisterSerializer

#     def post(self, request):
#         email = request.data.get("email")

#         # Check if user already exists
#         existing_user = User.objects.filter(email=email).first()
#         if existing_user:
#             if not existing_user.is_active:
#                 existing_user.delete()  # Delete non-verified user
#             else:
#                 return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

#         # Continue with registration
#         serializer = RegisterSerializer(data=request.data)

#         if serializer.is_valid():
#             user = serializer.save()
#             user.is_active = False  # User must verify OTP first
#             user.save()

#             # Send OTP via email
#             send_otp_email(user.email)

#             return Response({"message": "OTP sent to email. Please verify to activate your account."}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class VerifyOTPView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         user_otp = request.data.get("otp")

#         if not email or not user_otp:
#             return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#             otp_verification = OTPVerification.objects.get(user=user)

#             if str(user_otp) == str(otp_verification.otp_code):
#                 user.is_active = True  # Activate user
#                 user.save()
#                 otp_verification.delete()  # Delete OTP record after successful verification
#                 return Response({"message": "Email verified successfully. You can now log in."}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         except OTPVerification.DoesNotExist:
#             return Response({"error": "OTP not found or expired"}, status=status.HTTP_404_NOT_FOUND)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.timezone import now
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers  

from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer, OTPVerificationSerializer,
    PasswordResetSerializer, ProfileSerializer, EmailVerificationSerializer, EditProfileSerializer, ChildSerializer
)
from .models import OTPVerification, Profile, Child, Diagnosis
from .utils import send_verification_email, generate_otp
# Get the custom User model
User = get_user_model()


### ✅ Protected API View ###
class ProtectedView(APIView):
    """🔐 Requires authentication to access."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"}, status=status.HTTP_200_OK)


### ✅ Register User ###
class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(user.password)  # Hash password before saving
                user.is_active = False  # User must verify email first
                user.save()

                # Generate OTP and send verification email
                otp_verification, _ = OTPVerification.objects.get_or_create(user=user)
                otp_verification.generate_otp()
                send_verification_email(user.email, otp_verification.otp_code)

                return Response({"message": "OTP sent to email"}, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"🚨 ERROR: {str(e)}")  # Log error in console
            return Response({"error": "Something went wrong on the server."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


### ✅ Login User ###
class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            #user = get_object_or_404(User, email=email)
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            if not user.check_password(password):
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
                return Response({"error": "User is not verified. Please verify your email."}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
        #     if user.check_password(password):
        #         if user.is_active:
        #             refresh = RefreshToken.for_user(user)
        #             return Response({"refresh": str(refresh), "access": str(refresh.access_token)})
        #         else:
        #             return Response({"error": "User is not verified. Please verify your email."}, status=status.HTTP_401_UNAUTHORIZED)
        #     return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### ✅ Logout User ###
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


### ✅ Verify Email OTP (with expiration check) ###
class VerifyOTPView(APIView):
    serializer_class = OTPVerificationSerializer

    @swagger_auto_schema(request_body=OTPVerificationSerializer)
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user_otp = serializer.validated_data["otp"]

            try:
                user = User.objects.get(email=email)
                otp_verification = OTPVerification.objects.get(user=user)

                # Check if OTP is expired (10 min limit)
                if otp_verification.is_expired():
                    otp_verification.delete()
                    return Response({"error": "OTP expired, request a new one."}, status=status.HTTP_400_BAD_REQUEST)

                if otp_verification.otp_code == user_otp:
                    user.is_active = True
                    user.save()
                    otp_verification.delete()
                    return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except (User.DoesNotExist, OTPVerification.DoesNotExist):
                return Response({"error": "OTP expired or user not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetView(APIView):
    """
    ✅ Generates a new OTP and sends it to the user's email.
    """
    @swagger_auto_schema(request_body=serializers.Serializer)
    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)

            if not user.is_active:
                return Response({"error": "User is not verified."}, status=status.HTTP_403_FORBIDDEN)

            # ✅ Generate and send a new OTP
            otp_verification, _ = OTPVerification.objects.get_or_create(user=user)
            otp_verification.generate_otp()
            send_verification_email(user.email, otp_verification.otp_code)

            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
class VerifyPasswordResetOTPView(APIView):
    """
    ✅ Verifies the OTP before allowing password reset.
    """
    serializer_class = OTPVerificationSerializer

    @swagger_auto_schema(request_body=OTPVerificationSerializer)
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user_otp = serializer.validated_data["otp"]

            try:
                user = User.objects.get(email=email)
                otp_verification = OTPVerification.objects.get(user=user)

                # ✅ Check if OTP is expired
                if otp_verification.is_expired():
                    otp_verification.delete()
                    return Response({"error": "OTP expired, request a new one."}, status=status.HTTP_400_BAD_REQUEST)

                # ✅ Check if OTP matches
                if otp_verification.otp_code == user_otp:
                    return Response({"message": "OTP verified successfully. You can now reset your password."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            except (User.DoesNotExist, OTPVerification.DoesNotExist):
                return Response({"error": "Invalid request. Please request a password reset again."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### ✅ Password Reset with Email OTP ###
class PasswordResetView(APIView):
    """
    ✅ Allows the user to reset their password after verifying OTP.
    """
    serializer_class = PasswordResetSerializer

    @swagger_auto_schema(request_body=PasswordResetSerializer)
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            new_password = serializer.validated_data["new_password"]

            try:
                user = User.objects.get(email=email)

                # ✅ Check if user has already verified OTP
                otp_verification = OTPVerification.objects.get(user=user)
                if otp_verification.is_expired():
                    otp_verification.delete()
                    return Response({"error": "OTP expired, request a new one."}, status=status.HTTP_400_BAD_REQUEST)

                # ✅ Set new password and delete OTP record
                user.set_password(new_password)
                user.save()
                otp_verification.delete()

                return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except OTPVerification.DoesNotExist:
                return Response({"error": "OTP verification required before resetting password."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import parsers
### ✅ User Profile Management ###
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser] 

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, partial=True)

        if serializer.is_valid():
            profile = self.get_object()
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### ✅ Resend Email Verification OTP ###
class ResendEmailOTPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        otp_verification, _ = OTPVerification.objects.get_or_create(user=user)
        otp_verification.generate_otp()
        send_verification_email(user.email, otp_verification.otp_code)

        return Response({"message": "New OTP sent to email"}, status=status.HTTP_200_OK)

class AddChildView(generics.CreateAPIView):
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        ✅ Automatically assign the current user as the parent.
        ✅ Ensure only valid diagnoses are assigned.
        """
        diagnoses_data = self.request.data.get("diagnoses", [])  # Extract diagnoses from request

        # Ensure diagnoses exist
        valid_diagnoses = Diagnosis.objects.filter(id__in=diagnoses_data)
        child = serializer.save(parent=self.request.user)

        # Assign diagnoses (if any)
        child.diagnoses.set(valid_diagnoses)

class EditChildView(generics.RetrieveUpdateAPIView):
    """
    ✅ Allows parents to retrieve and update their child's information.
    ✅ Supports GET (retrieve), PUT (full update), and PATCH (partial update).
    ✅ Ensures that users can only edit their own children.
    """
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id" 

    def get_queryset(self):
        """✅ Ensure users can only access their own children"""
        return Child.objects.filter(parent=self.request.user)