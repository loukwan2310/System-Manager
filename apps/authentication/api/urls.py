from django.urls import path

from .views import LoginAPIView, LogoutAPIView, FitbitVerifyCodeAPIView

urlpatterns = [
    path('auth/login', LoginAPIView.as_view(), name='auth_login'),
    path('auth/logout', LogoutAPIView.as_view(), name='auth_logout'),
    path('auth/verify-fitbit-code', FitbitVerifyCodeAPIView.as_view(), name='auth_verify_fitbit_code'),
]
