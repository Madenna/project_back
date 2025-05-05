from rest_framework import serializers
from django.utils import timezone
from .models import User, Profile, OTPVerification, Child, Diagnosis
from userauth.utils import send_verification_email
from django.conf import settings

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        return value

    def validate(self, data):
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        #Validate OTP and activate user
        try:
            otp_record = OTPVerification.objects.get(user__email=data["email"], otp_code=data["otp"])

            # Check expiration
            if (timezone.now() - otp_record.created_at).total_seconds() > 600:
                otp_record.delete()
                raise serializers.ValidationError("OTP has expired. Request a new one.")

            # Activate the user
            user = otp_record.user
            user.is_active = True
            user.save()

            # Remove used OTP
            otp_record.delete()

            return data

        except OTPVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        #Ensure email exists in the system before resetting
        if not User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("No user found with this email.")
        return data

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        #Validate OTP for email verification
        try:
            otp_record = OTPVerification.objects.get(user__email=data["email"], otp_code=data["otp"])
            
            # Check if OTP is expired
            time_difference = timezone.now() - otp_record.created_at
            if time_difference.total_seconds() > 600:
                raise serializers.ValidationError("OTP has expired. Request a new one.")

            return data

        except OTPVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

class VerifyNewEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        try:
            request = self.context.get("request")
            user = request.user  # get user from request context
            otp_record = OTPVerification.objects.get(user=user, otp_code=data["otp"])

            if (timezone.now() - otp_record.created_at).total_seconds() > 600:
                raise serializers.ValidationError("OTP has expired. Request a new one.")

            data['user'] = user
            data['otp_record'] = otp_record
            return data

        except OTPVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    profile_photo = serializers.URLField(required=False, allow_null=True)
    additional_info = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'profile_photo', 'additional_info', 'city']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if not rep.get('profile_photo'):  # ✅ Fix: use .get()
            rep['profile_photo'] = getattr(settings, 'DEFAULT_PROFILE_PHOTO', '')
        return rep

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Update User model
        user = instance.user
        user.full_name = user_data.get('full_name', user.full_name)

        new_email = user_data.get('email')
        if new_email and new_email != user.email:
            user.temp_email = new_email  
            user.save()

            otp_obj, _ = OTPVerification.objects.get_or_create(user=user)
            otp_obj.generate_otp()
            send_verification_email(new_email, otp_obj.otp_code)
            self.context['email_verification_sent'] = True

        user.save()

        for field in ['profile_photo', 'additional_info', 'city']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

        return instance

class DiagnosisSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Diagnosis
        fields = ['id', 'name']
        read_only_fields = ['id']

    def validate_name(self, value):
        return value
    
class ChildSerializer(serializers.ModelSerializer):
    diagnoses = DiagnosisSerializer(many=True)

    class Meta:
        model = Child
        fields = ["id", "full_name", "birthday", "gender", "diagnoses"]
        read_only_fields = ['id', 'parent']

    def create(self, validated_data):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request context is required.")

        diagnoses_data = validated_data.pop('diagnoses', [])
        validated_data["parent"] = request.user

        child = Child.objects.create(**validated_data)

        for diagnosis in diagnoses_data:
            name = diagnosis.get('name')
            if not name:
                raise serializers.ValidationError("Each diagnosis must have a 'name'.")
            diagnosis_obj, _ = Diagnosis.objects.get_or_create(name=name.strip())
            child.diagnoses.add(diagnosis_obj)

        return child

    def update(self, instance, validated_data):
        diagnoses_data = validated_data.pop('diagnoses', None)

        if diagnoses_data is not None:
            instance.diagnoses.clear()
            for diagnosis in diagnoses_data:
                name = diagnosis.get('name')
                if not name:
                    raise serializers.ValidationError("Each diagnosis must have a 'name'.")
                diagnosis_obj, _ = Diagnosis.objects.get_or_create(name=name.strip())
                instance.diagnoses.add(diagnosis_obj)

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()

        return instance
    
from django.contrib.auth import get_user_model

User = get_user_model()

class DeleteAccountSerializer(serializers.Serializer):
    # The user needs to provide their password for confirmation
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context.get("request").user
        password = attrs.get("password")

        # Check if the password matches the current user's password
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password. Please try again.")
        
        return attrs

    def delete_account(self):
        user = self.context.get("request").user
        user.delete()  # Deletes the user from the database