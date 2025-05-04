from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Child, Diagnosis, OTPVerification

# Register User model
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'temp_email', 'is_active', 'is_staff')}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'full_name', 'password1', 'password2')}),
    )
    filter_horizontal = ('groups', 'user_permissions')

# Register Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'profile_photo')
    search_fields = ('user__email', 'city')
    list_filter = ('city',)

# Register Child model
class ChildAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'parent', 'birthday', 'gender')
    list_filter = ('gender', 'parent')
    search_fields = ('full_name', 'parent__email')

# Register Diagnosis model
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register OTPVerification model
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)

# Register the models in admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(OTPVerification, OTPVerificationAdmin)
