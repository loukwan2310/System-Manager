from django.urls import path

from .views import MyProfileAPIView, MyConfigAPIView, UserHairStyleListAPIView

urlpatterns = [
    path('my-config', MyConfigAPIView.as_view(), name='user_my_config'),
    path('my-profile', MyProfileAPIView.as_view(), name='user_my_profile'),
    path('users/hair-styles', UserHairStyleListAPIView.as_view(), name='user_hair_style_list'),
]
