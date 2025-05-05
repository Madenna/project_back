from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProtectedView, ProfileView, ListChildrenView, VerifyNewEmailView, health_check,
    PasswordResetView, VerifyOTPView, ResendEmailOTPView, AddChildView, EditChildView, RequestPasswordResetView, VerifyPasswordResetOTPView, DeleteAccountView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path('register/', RegisterView.as_view(), name='register'),  # Register
    path('login/', LoginView.as_view(), name='login'),  # Custom Login
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT Token

    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),  # Verify Email OTP
    path("verify-new-email/", VerifyNewEmailView.as_view(), name="verify_new_email"),
    path('resend-otp/', ResendEmailOTPView.as_view(), name='resend_otp'),  # Resend Email OTP

    path('protected/', ProtectedView.as_view(), name='protected'),  # Protected route
    path('profile/', ProfileView.as_view(), name='profile'),  # User Profile
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request_password_reset'),  # Step 1: Request OTP
    path('verify-password-reset-otp/', VerifyPasswordResetOTPView.as_view(), name='verify_password_reset_otp'),  # Step 2: Verify OTP
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),  # Step 3: Set new password
    path('add-child/', AddChildView.as_view(), name='add_child'), # API to Add Child
    path('children/', ListChildrenView.as_view(), name='list_children'),
    path('edit-child/<uuid:id>/', EditChildView.as_view(), name='edit_child'),  # Edit Child

    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
]
