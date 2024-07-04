from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('', include('apps.users.api.urls')),
    path('', include('apps.register.api.urls')),
    path('', include('apps.authentication.api.urls')),
]
