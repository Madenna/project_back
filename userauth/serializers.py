# from rest_framework import serializers
# from .models import User, Profile
# from .utils import send_otp_smsc
# from django.core.mail import send_mail
# import random
# from .models import User

# # Login Serializer
# class LoginSerializer(serializers.Serializer):
#     phone_number = serializers.CharField()
#     password = serializers.CharField(write_only=True)

# # Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         #fields = ['phone_number', 'full_name', 'password']
#         fields = ["email", "full_name", "password"]
#         extra_kwargs = {'password': {'write_only': True}}
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         user.is_active = False  # User must verify email first
#         user.save()

#         # Generate OTP and send verification email
#         otp = random.randint(100000, 999999)
#         VerificationOTP.objects.create(user=user, otp_code=otp)

#         send_mail(
#             "Verify Your Email",
#             f"Your verification code is {otp}",
#             "your_email@gmail.com",  # Change to your email
#             [user.email],
#             fail_silently=False,
#         )

#         return user

# class OTPRequestSerializer(serializers.Serializer):
#     phone_number = serializers.CharField()

#     def validate_phone_number(self, value):
#         if not value.startswith("+") or not value[1:].isdigit():
#             raise serializers.ValidationError("Phone number must start with '+' followed by digits.")
#         return value
    
# class VerifyEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField()

# # OTP Verification Serializer
# class OTPVerificationSerializer(serializers.Serializer):
#     phone_number = serializers.CharField()
#     otp = serializers.CharField()

# # Password Reset Serializer
# class PasswordResetSerializer(serializers.Serializer):
#     #phone_number = serializers.CharField()
#     email = serializers.EmailField()
#     new_password = serializers.CharField(write_only=True)

# # Phone Number Change Serializer
# class PhoneNumberChangeSerializer(serializers.Serializer):
#     new_phone_number = serializers.CharField()

# # Verify New Phone Number Serializer
# class VerifyNewPhoneNumberSerializer(serializers.Serializer):
#     new_phone_number = serializers.CharField()
#     otp = serializers.CharField()
#     def validate_new_phone_number(self, value):
#         if not value.startswith("+") or not value[1:].isdigit():
#             raise serializers.ValidationError("Phone number must start with '+' followed by digits.")
#         return value

# class RequestPhoneNumberChangeSerializer(serializers.Serializer):
#     new_phone_number = serializers.CharField(max_length=15)

#     def validate_new_phone_number(self, value):
#         if not value.startswith("+") or not value[1:].isdigit():
#             raise serializers.ValidationError("Phone number must start with '+' followed by digits.")
#         return value

# class ProfileSerializer(serializers.ModelSerializer):
#     full_name = serializers.CharField(source='user.full_name', required=False)
#     phone_number = serializers.CharField(source='user.phone_number', required=False)
#     profile_photo = serializers.ImageField(required=False, allow_null=True)
#     additional_info = serializers.CharField(required=False, allow_null=True)
#     city = serializers.CharField(required=False, allow_null=True)

#     class Meta:
#         model = Profile
#         fields = ['full_name', 'phone_number', 'profile_photo', 'additional_info', 'city']
    
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         if not rep['profile_photo']:
#             # rep['profile_photo'] = '/media/profile_photos/default.jpg'  # Default image path
#             request = self.context.get('request')
#             default_photo_url = '/media/profile_photos/default.jpg'
#             if request:
#                 default_photo_url = request.build_absolute_uri(default_photo_url)
#             rep['profile_photo'] = rep['profile_photo'] or default_photo_url
#         return rep

#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', {})
        
#         # Check if phone number is being changed
#         new_phone_number = user_data.get('phone_number')
#         if new_phone_number and new_phone_number != instance.user.phone_number:
#             # Send OTP for new phone number
#             otp_response = send_otp_smsc(new_phone_number)
#             # Temporarily store new phone number in profile model (or create a separate field)
#             instance.user.temp_phone_number = new_phone_number  # This field should exist in the User model
#             instance.user.save()
#             return {"message": "OTP sent to new phone number. Please verify."}

#         # Update User model fields
#         user = instance.user
#         user.full_name = user_data.get('full_name', user.full_name)
#         user.save()

#         # Update Profile model fields
#         instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
#         instance.additional_info = validated_data.get('additional_info', instance.additional_info)
#         instance.city = validated_data.get('city', instance.city)
#         instance.save()

#         return instance

# class UserSerializer(serializers.ModelSerializer):
#     profile = serializers.SerializerMethodField()
#     class Meta:
#         model = User
#         fields = ['id', 'full_name', 'phone_number', 'password', 'profile']
#         extra_kwargs = {'password': {'write_only': True}}

#     def get_profile(self, obj):
#         profile = getattr(obj, 'profile', None)
#         return ProfileSerializer(profile).data if profile else None

#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         user = User.objects.create_user(
#             phone_number=validated_data['phone_number'],
#             full_name=validated_data['full_name'],
#             password=validated_data['password']
#         )
#         if profile_data:
#             Profile.objects.create(user=user, **profile_data)
#         return user
    
#     def update(self, instance, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         instance.full_name = validated_data.get('full_name', instance.full_name)
#         instance.phone_number = validated_data.get('phone_number', instance.phone_number)
#         if 'password' in validated_data:
#             instance.set_password(validated_data['password'])
#         instance.save()

#         if profile_data:
#             profile = instance.profile
#             profile.profile_photo = profile_data.get('profile_photo', profile.profile_photo)
#             profile.city = profile_data.get('city', profile.city)
#             profile.additional_info = profile_data.get('additional_info', profile.additional_info)
#             profile.save()

#         return instance

from rest_framework import serializers
from django.utils import timezone
from .models import User, Profile, OTPVerification, Child, Diagnosis
from userauth.utils import send_verification_email
from django.conf import settings

# -------------------------------
# ✅ REGISTER SERIALIZER
# -------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Ensure password is hashed before saving"""
        # user = User(
        #     email=validated_data['email'],
        #     full_name=validated_data['full_name']
        # )
        # user.set_password(validated_data['password'])  # Hash password
        # user.is_active = False  # Require email verification
        # user.save()
        
        # # Create an empty profile for the user
        # Profile.objects.create(user=user)
        user = User.objects.create_user(**validated_data)
        user.is_active = False  # ✅ Require email verification
        user.save()
        
        # ✅ Only create a profile if it does not exist
        Profile.objects.get_or_create(user=user)  


        return user

# -------------------------------
# ✅ LOGIN SERIALIZER
# -------------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# -------------------------------
# ✅ OTP VERIFICATION SERIALIZER
# -------------------------------
class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        """Check if the OTP is expired"""
        try:
            otp_record = OTPVerification.objects.get(user__email=data["email"], otp_code=data["otp"])
            
            # Check if OTP is expired (10 min limit)
            time_difference = timezone.now() - otp_record.created_at
            if time_difference.total_seconds() > 600:  # 600 sec = 10 min
                raise serializers.ValidationError("OTP has expired. Request a new one.")

            return data

        except OTPVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

# -------------------------------
# ✅ PASSWORD RESET SERIALIZER
# -------------------------------
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Ensure email exists in the system before resetting"""
        if not User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("No user found with this email.")
        return data

# -------------------------------
# ✅ EMAIL VERIFICATION SERIALIZER
# -------------------------------
class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        """Validate OTP for email verification"""
        try:
            otp_record = OTPVerification.objects.get(user__email=data["email"], otp_code=data["otp"])
            
            # Check if OTP is expired
            time_difference = timezone.now() - otp_record.created_at
            if time_difference.total_seconds() > 600:
                raise serializers.ValidationError("OTP has expired. Request a new one.")

            return data

        except OTPVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

# # -------------------------------
# # ✅ PROFILE SERIALIZER (VIEW PROFILE)
# # -------------------------------
# class ProfileSerializer(serializers.ModelSerializer):
#     full_name = serializers.CharField(source='user.full_name', required=False)
#     email = serializers.EmailField(source='user.email', required=False)
#     profile_photo = serializers.ImageField(required=False, allow_null=True)
#     additional_info = serializers.CharField(required=False, allow_null=True)
#     city = serializers.CharField(required=False, allow_null=True)

#     class Meta:
#         model = Profile
#         fields = ['full_name', 'email', 'profile_photo', 'additional_info', 'city']
    
#     def to_representation(self, instance):
#         """Set a default profile image if none is uploaded"""
#         rep = super().to_representation(instance)
#         if not rep['profile_photo']:
#             rep['profile_photo'] = '/media/profile_photos/default.jpg'  # Default image path
#         return rep

# -------------------------------
# ✅ EDIT PROFILE SERIALIZER
# -------------------------------
# class EditProfileSerializer(serializers.ModelSerializer):
#     full_name = serializers.CharField(source='user.full_name', required=False)
#     email = serializers.EmailField(source='user.email', required=False)
#     profile_photo = serializers.URLField(required=False, allow_null=True)
#     additional_info = serializers.CharField(required=False, allow_null=True)
#     city = serializers.CharField(required=False, allow_null=True)

#     class Meta:
#         model = Profile
#         fields = ['full_name', 'email', 'profile_photo', 'additional_info', 'city']
    
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         if not rep['profile_photo']:
#             rep['profile_photo'] = '/media/profile_photos/default.jpg'
#         return rep

#     def update(self, instance, validated_data):
#         """Update both user and profile information"""
#         user_data = validated_data.pop('user', {})
        
#         user = instance.user
#         user.full_name = user_data.get('full_name', user.full_name)

#         # Handle email change separately
#         new_email = user_data.get('email')
#         if new_email and new_email != user.email:
#             user.temp_email = new_email  # Store the new email temporarily
#             user.save()
#             return {"message": "Verification email sent to new email address."}

#         user.save()

#         # Update Profile model fields
#         instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
#         instance.additional_info = validated_data.get('additional_info', instance.additional_info)
#         instance.city = validated_data.get('city', instance.city)
#         instance.save()

#         return instance

# -------------------------------
# ✅ VERIFY NEW EMAIL SERIALIZER
# -------------------------------
class VerifyNewEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        """Check if OTP is valid and email matches"""
        try:
            # ✅ Get user with matching temp_email
            user = User.objects.get(temp_email=data["new_email"])

            # ✅ Get OTP record
            otp_record = OTPVerification.objects.get(user=user, otp_code=data["otp"])

            # ✅ Check if expired
            if (timezone.now() - otp_record.created_at).total_seconds() > 600:
                raise serializers.ValidationError("OTP has expired. Request a new one.")

            self.user = user
            self.otp_record = otp_record
            return data

        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            raise serializers.ValidationError("Invalid OTP or email.")

### ✅ User Serializer ###
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
    
### ✅ Profile Serializer ###
# class ProfileSerializer(serializers.ModelSerializer):
#     full_name = serializers.CharField(source='user.full_name', required=False)
#     email = serializers.CharField(source='user.email', required=False)
#     profile_photo = serializers.URLField(required=False, allow_null=True)
#     additional_info = serializers.CharField(required=False, allow_null=True)
#     city = serializers.CharField(required=False, allow_null=True)

#     class Meta:
#         model = Profile
#         fields = ['full_name', 'email', 'profile_photo', 'additional_info', 'city']
    
#     # def to_representation(self, instance):
#     #     """Set a default profile image if none is uploaded"""
#     #     rep = super().to_representation(instance)
#     #     if not rep.get('profile_photo'):
#     #         rep['profile_photo'] = settings.DEFAULT_PROFILE_PHOTO
#     #     return rep
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         return rep

#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', {})

#         # Update User model
#         user = instance.user
#         user.full_name = user_data.get('full_name', user.full_name)
#         user.save()

#         # Update Profile model
#         instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
#         instance.additional_info = validated_data.get('additional_info', instance.additional_info)
#         instance.city = validated_data.get('city', instance.city)
#         instance.save()

#         return instance
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

        # ✅ Update User model
        user = instance.user
        user.full_name = user_data.get('full_name', user.full_name)

        new_email = user_data.get('email')
        if new_email and new_email != user.email:
            user.temp_email = new_email  # you can trigger OTP verification if needed
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
        # ✅ Don’t raise error for existing diagnoses
        return value

# class ChildSerializer(serializers.ModelSerializer):
#     diagnoses = DiagnosisSerializer(many=True)  # ✅ Allowing nested input

#     class Meta:
#         model = Child
#         fields = ["id", "full_name", "birthday", "gender", "diagnoses"]
#         read_only_fields = ['id', 'parent']  

#     def create(self, validated_data):
#         """
#         ✅ Automatically assigns `parent` (current user) when adding a child.
#         ✅ Ensures diagnoses are created or linked correctly.
#         """
#         request = self.context.get("request")
#         if not request:
#             raise serializers.ValidationError("Request context is required.")
        
#         validated_data["parent"] = request.user  # ✅ Assign parent automatically

#         # Handle multiple diagnoses
#         diagnoses_data = validated_data.pop('diagnoses', [])
#         child = Child.objects.create(**validated_data)

#         for diagnosis in diagnoses_data:
#             diagnosis_obj, _ = Diagnosis.objects.get_or_create(name=diagnosis['name'])  
#             child.diagnoses.add(diagnosis_obj)  # ✅ Add to ManyToMany field

#         return child
    
#     def update(self, instance, validated_data):
#         """
#         ✅ Allows updating child details while keeping `parent` unchanged.
#         ✅ Properly updates diagnoses.
#         """
#         diagnoses_data = validated_data.pop('diagnoses', None)
#         if diagnoses_data is not None:
#             # Only update diagnoses if they are included in the request
#             existing_diagnoses = {diag.name: diag for diag in instance.diagnoses.all()}  

#             for diagnosis in diagnoses_data:
#                 diagnosis_name = diagnosis['name']
#                 if diagnosis_name not in existing_diagnoses:
#                     diagnosis_obj, _ = Diagnosis.objects.get_or_create(name=diagnosis_name)
#                     instance.diagnoses.add(diagnosis_obj)

#         # ✅ Update other child fields
#         instance.full_name = validated_data.get('full_name', instance.full_name)
#         instance.birthday = validated_data.get('birthday', instance.birthday)
#         instance.gender = validated_data.get('gender', instance.gender)
#         instance.save()
#         return instance

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
