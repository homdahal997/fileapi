"""
URLs for the storage_integrations app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'connections', views.CloudStorageConnectionViewSet, basename='storage-connections')
router.register(r'imports', views.ImportJobViewSet, basename='import-jobs')
router.register(r'exports', views.ExportJobViewSet, basename='export-jobs')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Provider information
    path('providers/', views.StorageProvidersView.as_view(), name='storage-providers'),
    path('providers/<str:provider_name>/auth/', views.ProviderAuthView.as_view(), name='provider-auth'),
    
    # Connection management
    path('connections/test/<int:connection_id>/', views.TestConnectionView.as_view(), name='test-connection'),
    path('connections/<int:connection_id>/browse/', views.BrowseStorageView.as_view(), name='browse-storage'),
    path('connections/<int:connection_id>/set-default/', views.SetDefaultStorageView.as_view(), name='set-default-storage'),
    
    # File operations
    path('import/', views.ImportFileView.as_view(), name='import-file'),
    path('import/batch/', views.BatchImportView.as_view(), name='batch-import'),
    path('export/', views.ExportFileView.as_view(), name='export-file'),
    path('export/batch/', views.BatchExportView.as_view(), name='batch-export'),
    
    # Import/Export management
    path('imports/<int:import_id>/cancel/', views.CancelImportView.as_view(), name='cancel-import'),
    path('exports/<int:export_id>/cancel/', views.CancelExportView.as_view(), name='cancel-export'),
    path('imports/<int:import_id>/progress/', views.ImportProgressView.as_view(), name='import-progress'),
    path('exports/<int:export_id>/progress/', views.ExportProgressView.as_view(), name='export-progress'),
    
    # Storage quota and usage
    path('quota/', views.StorageQuotaView.as_view(), name='storage-quota'),
    path('usage/', views.StorageUsageView.as_view(), name='storage-usage'),
    
    # OAuth callbacks (for cloud providers that require OAuth)
    path('oauth/callback/<str:provider_name>/', views.OAuthCallbackView.as_view(), name='oauth-callback'),
    path('oauth/disconnect/<str:provider_name>/', views.OAuthDisconnectView.as_view(), name='oauth-disconnect'),
    
    # Storage logs and activity
    path('logs/', views.StorageLogsView.as_view(), name='storage-logs'),
    path('activity/', views.StorageActivityView.as_view(), name='storage-activity'),
]
