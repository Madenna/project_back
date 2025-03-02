from rest_framework import serializers
from .models import User, Profile
from .utils import send_otp_firebase

# Login Serializer
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'full_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

# OTP Verification Serializer
class OTPVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    id_token = serializers.CharField()

# Password Reset Serializer
class PasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

# Phone Number Change Serializer
class PhoneNumberChangeSerializer(serializers.Serializer):
    new_phone_number = serializers.CharField()

# Verify New Phone Number Serializer
class VerifyNewPhoneNumberSerializer(serializers.Serializer):
    new_phone_number = serializers.CharField()
    id_token = serializers.CharField()

class RequestPhoneNumberChangeSerializer(serializers.Serializer):
    new_phone_number = serializers.CharField(max_length=15)

    def validate_new_phone_number(self, value):
        if not value.startswith("+") or not value[1:].isdigit():
            raise serializers.ValidationError("Phone number must start with '+' followed by digits.")
        return value

class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', required=False)
    phone_number = serializers.CharField(source='user.phone_number', required=False)
    profile_photo = serializers.ImageField(required=False, allow_null=True)
    additional_info = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)


    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'profile_photo', 'additional_info', 'city']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        
        # Check if phone number is being changed
        new_phone_number = user_data.get('phone_number')
        if new_phone_number and new_phone_number != instance.user.phone_number:
            # Send OTP for new phone number
            otp_response = send_otp_firebase(new_phone_number)
            # Temporarily store new phone number in profile model (or create a separate field)
            instance.user.temp_phone_number = new_phone_number  # This field should exist in the User model
            instance.user.save()
            return {"message": "OTP sent to new phone number. Please verify."}

        # Update User model fields
        user = instance.user
        user.full_name = user_data.get('full_name', user.full_name)
        user.save()

        # Update Profile model fields
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
        instance.additional_info = validated_data.get('additional_info', instance.additional_info)
        instance.city = validated_data.get('city', instance.city)
        instance.save()

        return instance

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def get_profile(self, obj):
        return ProfileSerializer(obj.profile).data if obj.profile else None

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()

        if profile_data:
            profile = instance.profile
            profile.profile_photo = profile_data.get('profile_photo', profile.profile_photo)
            profile.city = profile_data.get('city', profile.city)
            profile.additional_info = profile_data.get('additional_info', profile.additional_info)
            profile.save()

        return instance