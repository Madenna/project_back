# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models
# import random
# from django.contrib.auth import get_user_model
# import uuid
# from django.contrib.auth.models import AbstractUser
# from django.conf import settings
# from django.utils import timezone

# class CustomUserManager(BaseUserManager):
#     def create_user(self, phone_number, full_name, password=None, **extra_fields):
#         if not phone_number:
#             raise ValueError("Users must have a phone number")
#         user = self.model(phone_number=phone_number, full_name=full_name)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, phone_number, full_name, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(phone_number, full_name, password,)

# from django.utils.translation import gettext_lazy as _
# class UserManager(BaseUserManager):
#     def create_user(self, email, full_name, password=None):
#         if not email:
#             raise ValueError("Users must have an email address")
#         email = self.normalize_email(email)
#         user = self.model(email=email, full_name=full_name)
#         user.set_password(password)  # Hash password
#         user.save(using=self._db)
#         return user
#     def create_superuser(self, email, full_name, password):
#         user = self.create_user(email, full_name, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save(using=self._db)
#         return user
    
# class User(AbstractBaseUser, PermissionsMixin):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     full_name = models.CharField(max_length=255)

#     email = models.EmailField(unique=True)  # Email for authentication
#     email_verified = models.BooleanField(default=False)  # Email verification flag
    
#     phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
#     # temp_phone_number = models.CharField(max_length=15, blank=True, null=True) 
#     password = models.CharField(max_length=255)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now) 

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_groups',  # Fix Name Conflict
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_permissions',  # Fix Name Conflict
#         blank=True
#     )

#     objects = CustomUserManager()

#     #USERNAME_FIELD = 'phone_number'
#     USERNAME_FIELD = 'email' 
#     REQUIRED_FIELDS = ['full_name']

#     def __str__(self):
#         return self.email
#     def verify_email(self):
#         """ Mark email as verified """
#         self.email_verified = True
#         self.is_active = True  # Activate user once email is verified
#         self.save()
    
# User = get_user_model()

# class OTPVerification(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     otp_code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def generate_otp(self):
#         #Generate a 6-digit OTP
#         self.otp_code = str(random.randint(100000, 999999))
#         self.save()

#     def __str__(self):
#         return f"OTP for {self.user.phone_number}"

# class Profile(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, default='profile_photos/default.jpg')
#     city = models.CharField(max_length=100, blank=True, null=True)
#     additional_info = models.TextField(max_length=1000, blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.full_name}'s Profile"
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from django.db import models
import uuid
import random

### ✅ Custom User Manager ###
class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name)
        user.set_password(password)
        user.is_active = False  # Users must verify email first
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password):
        user = self.create_user(email=email, full_name=full_name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  # Superusers are active by default
        user.save(using=self._db)
        return user


### ✅ User Model ###
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # ✅ Email-based authentication
    temp_email = models.EmailField(blank=True, null=True)  # ✅ For email change requests
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)  # ✅ Users must verify email first
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.full_name


### ✅ Profile Model ###
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True, default="profile_photos/default.jpg")
    city = models.CharField(max_length=100, blank=True, null=True)
    additional_info = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name}'s Profile"


### ✅ OTP Verification Model (For Email Verification) ###
class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        """Generates a 6-digit OTP and saves it."""
        self.otp_code = str(random.randint(100000, 999999))
        self.created_at = timezone.now()  # Ensure OTP timestamp is updated
        self.save()

    def is_expired(self):
        """Check if OTP is expired (10 minutes limit)"""
        return (timezone.now() - self.created_at).total_seconds() > 600  # 600 seconds = 10 minutes

    def __str__(self):
        return f"OTP for {self.user.email}"
    
class Diagnosis(models.Model):
    """✅ Stores each diagnosis separately, allowing multiple diagnoses per child."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True) 

    def __str__(self):
        return self.name 
       
class Child(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="children")
    full_name = models.CharField(max_length=255)
    birthday = models.DateField()
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    diagnoses = models.ManyToManyField(Diagnosis, related_name="children")  # ✅ Many-to-Many

    def __str__(self):
        return f"{self.full_name} (Child of {self.parent.full_name})"

