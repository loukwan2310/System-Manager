from django.urls import path
from django.urls.conf import include

from .views import GoogleLoginRedirectApi, GoogleLoginApi, TestLoginGoogleAPIView

urlpatterns = [
    path('auth/google-login', GoogleLoginRedirectApi.as_view(), name='auth_redirect'),
    path('accounts3/google-oauth2/login/callback', GoogleLoginApi.as_view(), name='auth_login'),
    path('test/login', TestLoginGoogleAPIView.as_view(), name='auth_login'),
]
