"""
URL configuration for fileconvert_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from conversions import views
from conversions import simple_api_views

# API Documentation Schema
schema_view = get_schema_view(
    openapi.Info(
        title="File Conversion API",
        default_version='v1',
        description="""
        A comprehensive file conversion API service that supports conversion between 200+ file formats.
        
        ## Features
        - Convert between documents, images, audio, video, archives, spreadsheets, presentations, and ebooks
        - Batch processing with webhook notifications
        - Cloud storage integrations (AWS S3, Google Cloud Storage, Dropbox)
        - JWT and API key authentication
        - Rate limiting and quota management
        - Real-time conversion progress tracking
        
        ## Authentication
        This API supports two authentication methods:
        1. **JWT Authentication**: Obtain a JWT token via the `/auth/login/` endpoint
        2. **API Key Authentication**: Use your API key in the `Authorization` header as `Api-Key YOUR_API_KEY`
        
        ## Rate Limits
        - Free tier: 100 conversions/month, 1000 requests/hour
        - Basic tier: 1000 conversions/month, 5000 requests/hour
        - Pro tier: 10000 conversions/month, 20000 requests/hour
        - Enterprise: Custom limits
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@fileconvert.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Simple Web Interface (redirect root to simple converter)
    path('', RedirectView.as_view(url='/simple/', permanent=False)),
    path('simple/', include('conversions.urls')),
    
    # API Documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-alt'),
    
    # API Endpoints - Direct access (for easy integration)
    path('api/convert/', simple_api_views.SimpleConvertView.as_view(), name='api-convert'),
    path('api/convert/<uuid:job_id>/status/', simple_api_views.SimpleJobStatusView.as_view(), name='api-job-status'),
    path('api/convert/<uuid:job_id>/download/', simple_api_views.SimpleDownloadView.as_view(), name='api-download'),
    
    # API Endpoints - Versioned
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/conversions/', include('conversions.urls')),
    path('api/v1/storage/', include('storage_integrations.urls')),
    
    # Health check endpoint
    path('health/', include('conversions.health_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
