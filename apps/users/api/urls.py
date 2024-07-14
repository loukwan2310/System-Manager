from django.urls import path

from .views import MyProfileAPIView, MyConfigAPIView

urlpatterns = [
    path('my-config', MyConfigAPIView.as_view(), name='user_my_config'),
    path('my-profile', MyProfileAPIView.as_view(), name='user_my_profile'),
]
