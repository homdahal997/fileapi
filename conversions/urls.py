"""
URLs for the conversions app.
"""
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from . import views
from . import simple_views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'jobs', views.ConversionJobViewSet, basename='conversion-jobs')
router.register(r'batch-jobs', views.BatchConversionJobViewSet, basename='batch-jobs')
router.register(r'formats', views.FileFormatViewSet, basename='file-formats')
router.register(r'history', views.ConversionHistoryViewSet, basename='conversion-history')

urlpatterns = [
    # Default route for simple interface
    path('', simple_views.conversion_form, name='conversion-form'),
    path('convert/', simple_views.simple_convert, name='simple-convert'),
    path('result/<uuid:job_id>/', simple_views.conversion_result, name='conversion-result'),
    
    # API endpoints (when accessed via /api/v1/conversions/)
    path('', include(router.urls)),
    
    # Custom endpoints
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('convert/', views.ConvertFileView.as_view(), name='convert-file'),
    path('batch-convert/', views.BatchConvertView.as_view(), name='batch-convert'),
    
    # Job management
    path('jobs/<uuid:job_id>/cancel/', views.CancelJobView.as_view(), name='cancel-job'),
    path('jobs/<uuid:job_id>/retry/', views.RetryJobView.as_view(), name='retry-job'),
    path('jobs/<uuid:job_id>/download/', views.DownloadResultView.as_view(), name='download-result'),
    path('jobs/<uuid:job_id>/progress/', views.JobProgressView.as_view(), name='job-progress'),
    
    # Batch job management
    path('batch-jobs/<uuid:batch_id>/cancel/', views.CancelBatchJobView.as_view(), name='cancel-batch-job'),
    path('batch-jobs/<uuid:batch_id>/progress/', views.BatchJobProgressView.as_view(), name='batch-job-progress'),
    
    # Format validation and capabilities
    path('formats/validate/', views.ValidateFormatView.as_view(), name='validate-format'),
    path('formats/conversions/', views.SupportedConversionsView.as_view(), name='supported-conversions'),
    
    # User quota and analytics
    path('quota/', views.UserQuotaView.as_view(), name='user-quota'),
    path('analytics/', views.ConversionAnalyticsView.as_view(), name='conversion-analytics'),
    
    # Webhooks
    path('webhooks/test/', views.TestWebhookView.as_view(), name='test-webhook'),
]
