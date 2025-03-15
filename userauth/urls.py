# from django.urls import path
# from .views import RegisterView, LoginView, LogoutView, ProtectedView, ProfileView, PasswordResetView, VerifyNewPhoneNumberView, RequestPhoneNumberChangeView, VerifyOTPView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/',  LoginView.as_view(), name='login'),  # custom Login
#     path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
#     path('logout/', LogoutView.as_view(), name='logout'), 
#     path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
#     path('protected/', ProtectedView.as_view(), name='protected'),  # New protected route
#     path('profile/', ProfileView.as_view(), name='profile'),
#     path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
#     path('request-phone-change/', RequestPhoneNumberChangeView.as_view(), name='request_phone_change'),
#     path('verify-new-phone/', VerifyNewPhoneNumberView.as_view(), name='verify_new_phone')
# ]
from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProtectedView, ProfileView, 
    PasswordResetView, VerifyOTPView, ResendEmailOTPView, AddChildView, EditChildView, RequestPasswordResetView, VerifyPasswordResetOTPView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # ✅ Register
    path('login/', LoginView.as_view(), name='login'),  # ✅ Custom Login
    path('logout/', LogoutView.as_view(), name='logout'),  # ✅ Logout
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ✅ Refresh JWT Token

    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),  # ✅ Verify Email OTP
    path('resend-otp/', ResendEmailOTPView.as_view(), name='resend_otp'),  # ✅ Resend Email OTP

    path('protected/', ProtectedView.as_view(), name='protected'),  # ✅ Protected route
    path('profile/', ProfileView.as_view(), name='profile'),  # ✅ User Profile
    path("edit-profile/", ProfileView.as_view(), name="edit_profile"),  # ✅ Edit Profile
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request_password_reset'),  # ✅ Step 1: Request OTP
    path('verify-password-reset-otp/', VerifyPasswordResetOTPView.as_view(), name='verify_password_reset_otp'),  # ✅ Step 2: Verify OTP
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),  # ✅ Step 3: Set new password
    path('add-child/', AddChildView.as_view(), name='add_child'), # ✅ API to Add Child
    path('edit-child/<uuid:pk>/', EditChildView.as_view(), name='edit_child'),  # ✅ Edit Child
]
