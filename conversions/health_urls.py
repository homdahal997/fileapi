"""
Health check URLs for monitoring and load balancing.
"""
from django.urls import path
from . import health_views

urlpatterns = [
    path('', health_views.HealthCheckView.as_view(), name='health-check'),
    path('detailed/', health_views.DetailedHealthCheckView.as_view(), name='detailed-health-check'),
    path('database/', health_views.DatabaseHealthView.as_view(), name='database-health'),
    path('redis/', health_views.RedisHealthView.as_view(), name='redis-health'),
    path('celery/', health_views.CeleryHealthView.as_view(), name='celery-health'),
    path('storage/', health_views.StorageHealthView.as_view(), name='storage-health'),
]
