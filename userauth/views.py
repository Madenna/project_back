from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.timezone import now
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers  
from rest_framework.decorators import api_view
from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer, OTPVerificationSerializer, VerifyNewEmailSerializer,
    PasswordResetSerializer, ProfileSerializer, EmailVerificationSerializer, ChildSerializer
)
from .models import OTPVerification, Profile, Child, Diagnosis
from .utils import send_verification_email, generate_otp

@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})

# Get the custom User model
User = get_user_model()

# Protected API View 
class ProtectedView(APIView):
    #Requires authentication to access
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"}, status=status.HTTP_200_OK)


#Register User
class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                full_name = serializer.validated_data['full_name']
                password = serializer.validated_data['password']

                user = User.objects.filter(email=email).first()

                if user:
                    if user.is_active:
                        return Response({"error": "User already exists and verified."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        # User exists but not verified → resend new OTP
                        otp_verification, _ = OTPVerification.objects.get_or_create(user=user)
                        otp_verification.generate_otp()
                        send_verification_email(user.email, otp_verification.otp_code)

                        return Response({"message": "User already exists but not verified. New OTP sent."}, status=status.HTTP_200_OK)
                else:
                    # User doesn't exist → create
                    user = User.objects.create_user(
                        email=email, 
                        full_name=full_name,  
                        password=password, 
                        is_active=False
                    )
                    
                    # Default profile
                    Profile.objects.get_or_create(
                        user=user,
                        defaults={'profile_photo': settings.DEFAULT_PROFILE_PHOTO}
                    )

                    otp_verification, _ = OTPVerification.objects.get_or_create(user=user)
                    otp_verification.generate_otp()
                    send_verification_email(user.email, otp_verification.otp_code)

                    return Response({"message": "User registered successfully. OTP sent."}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as ve:
            print(f"ValueError: {str(ve)}")
            return Response({"error": f"ValueError: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return Response({"error": "Something went wrong on the server."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = User.objects.filter(email=email).first()
            if not user:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if not user.is_active:
                otp_record, _ = OTPVerification.objects.get_or_create(user=user)
                otp_record.generate_otp()
                send_verification_email(user.email, otp_record.otp_code)

                return Response({
                    "error": "Your account is not verified. A new verification code has been sent to your email."
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not user.check_password(password):
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Logout User
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

#Verify Email OTP (with expiration check) 
class VerifyOTPView(APIView):
    serializer_class = OTPVerificationSerializer

    @swagger_auto_schema(request_body=OTPVerificationSerializer)
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Email verified successfully"}, status=200)
        return Response(serializer.errors, status=400)

#Generates a new OTP and sends it to the user's email.
class RequestPasswordResetView(APIView):
    @swagger_auto_schema(request_body=serializers.Serializer)
    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)

            if not user.is_active:
                return Response({"error": "User is not verified."}, status=status.HTTP_403_FORBIDDEN)

            # Generate and send a new OTP
            otp_verification, _ = OTPVerification.objects.get_or_create(user=user)
            otp_verification.generate_otp()
            send_verification_email(user.email, otp_verification.otp_code)

            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#Verifies the OTP before allowing password reset.
class VerifyPasswordResetOTPView(APIView):
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

                # Check if OTP is expired
                if otp_verification.is_expired():
                    otp_verification.delete()
                    return Response({"error": "OTP expired, request a new one."}, status=status.HTTP_400_BAD_REQUEST)

                # Check if OTP matches
                if otp_verification.otp_code == user_otp:
                    return Response({"message": "OTP verified successfully. You can now reset your password."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            except (User.DoesNotExist, OTPVerification.DoesNotExist):
                return Response({"error": "Invalid request. Please request a password reset again."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Password Reset with Email OTP
class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer

    @swagger_auto_schema(request_body=PasswordResetSerializer)
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            new_password = serializer.validated_data["new_password"]

            try:
                user = User.objects.get(email=email)

                # Check if user has already verified OTP
                otp_verification = OTPVerification.objects.get(user=user)
                if otp_verification.is_expired():
                    otp_verification.delete()
                    return Response({"error": "OTP expired, request a new one."}, status=status.HTTP_400_BAD_REQUEST)

                # Set new password and delete OTP record
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
import logging
logger = logging.getLogger(__name__)
from .utils import upload_to_cloudinary
#User Profile Management
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_object(self):
        # Auto-create profile if not found
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        data = request.data.copy()

        # Handle file upload if present
        if 'profile_photo' in request.FILES:
            uploaded_file = request.FILES['profile_photo']
            photo_url = upload_to_cloudinary(uploaded_file)
            data['profile_photo'] = photo_url

        serializer = self.get_serializer(profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        # Return custom message if email was changed
        if serializer.context.get("email_verification_sent"):
            return Response({"message": "Verification code sent to your new email."})

        return Response(self.get_serializer(result).data)

#Resend Email Verification OTP 
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

    def get_serializer_context(self):
        return {"request": self.request}

class ListChildrenView(generics.ListAPIView):
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Child.objects.filter(parent=self.request.user)

class EditChildView(generics.RetrieveUpdateAPIView):
    """
    Allows parents to retrieve and update their child's information.
    Supports GET (retrieve), PUT (full update), and PATCH (partial update).
    Ensures that users can only edit their own children.
    """
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id" 

    def get_queryset(self):
        #Ensure users can only access their own children
        user = self.request.user
        queryset = Child.objects.filter(parent=user)
        logger.warning(f"[EditChildView] User: {user} | Accessible children IDs: {[str(child.id) for child in queryset]}")
        return queryset
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Child PATCH failed validation: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)
    
class VerifyNewEmailView(APIView):
    serializer_class = VerifyNewEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=VerifyNewEmailSerializer)
    def post(self, request):
        serializer = VerifyNewEmailSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = getattr(serializer, 'validated_data', {}).get('user', request.user)
            otp_record = serializer.validated_data.get('otp_record')

            user.email = serializer.validated_data["new_email"]
            user.temp_email = None
            user.save()
            otp_record.delete()

            return Response({"message": "Email updated successfully."}, status=200)

        return Response(serializer.errors, status=400)