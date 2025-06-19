from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

# Configure Swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="BalaSteps API",
        default_version="v1",
        description="API documentation for authentication and user management",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/swagger/')), 
    path('auth/', include('userauth.urls')),  
    path("info-hub/", include("information.urls")),

    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('forum/', include('forum.urls')),
    path('symptoms/', include('symptom_tracker.urls')),
    path("marketplace/", include("marketplace.urls")),
    path('komekai/', include('komekai.urls')),
    path('contact_us/', include('contact.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)