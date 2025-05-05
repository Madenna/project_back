from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from django.db import models
import uuid
import random

#Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=False):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, is_active=is_active)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password):
        user = self.create_user(email=email, full_name=full_name, password=password, is_active=True)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

#User Model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # Email-based authentication
    temp_email = models.EmailField(blank=True, null=True, unique=True)  # For email change requests
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)  # Users must verify email first
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.full_name

#Profile Model 
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    profile_photo = models.URLField(
        blank=True,
        null=True,
        default='https://res.cloudinary.com/dy936wtgc/image/upload/v1742898556/balasteps/ekcozvxutn136qtdorad.jpg'
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    additional_info = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name}'s Profile"

#OTP Verification Model (For Email Verification) 
class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        #Generates a 6-digit OTP and saves it
        self.otp_code = str(random.randint(100000, 999999))
        self.created_at = timezone.now()  # Ensure OTP timestamp is updated
        self.save()

    def is_expired(self):
        #Check if OTP is expired (10 minutes limit)
        return (timezone.now() - self.created_at).total_seconds() > 600  # 600 seconds = 10 minutes

    def __str__(self):
        return f"OTP for {self.user.email}"
    
class Diagnosis(models.Model):
    #Stores each diagnosis separately, allowing multiple diagnoses per child
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
    diagnoses = models.ManyToManyField(Diagnosis, related_name="children")  #Many-to-Many

    def __str__(self):
        return f"{self.full_name} (Child of {self.parent.full_name})"