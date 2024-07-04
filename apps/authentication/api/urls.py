from django.urls import path

from .views import LoginAPIView, LogoutAPIView, RegisterAPIView, VerifyOTPCodeAPIView, \
    SendgridEmailAPIView

urlpatterns = [
    path('auth/login', LoginAPIView.as_view(), name='auth_login'),
    path('auth/logout', LogoutAPIView.as_view(), name='auth_logout'),
    path('auth/register', RegisterAPIView.as_view(), name='auth_register'),
    path('auth/verify-otp-code', VerifyOTPCodeAPIView.as_view(), name='auth_verify_otp_code'),
    path('auth/send-otp-code', SendgridEmailAPIView.as_view(), name='auth_send_otp_code'),
]
