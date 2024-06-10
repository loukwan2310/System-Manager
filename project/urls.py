from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('api/v1/', include('api.v1.urls')),
    path('api/v2/', include('api.v2.urls')),
    path('accounts/', include('allauth.urls')),

]
if settings.DEBUG:
    urlpatterns += [
        path('admin', admin.site.urls),
        path('api/schema', SpectacularAPIView.as_view(), name='schema'),
        path('api/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        path('api/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
