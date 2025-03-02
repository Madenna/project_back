from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProtectedView, VerifyOTPView, ProfileView, PasswordResetView, VerifyNewPhoneNumberView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',  LoginView.as_view(), name='login'),  # custom Login
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
    path('protected/', ProtectedView.as_view(), name='protected'),  # New protected route
    path('profile/', ProfileView.as_view(), name='profile'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('verify-new-phone/', VerifyNewPhoneNumberView.as_view(), name='verify_new_phone'),
]