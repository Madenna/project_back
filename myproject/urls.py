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

    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
