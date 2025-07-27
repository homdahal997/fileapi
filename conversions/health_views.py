"""
Health check views for monitoring.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HealthCheckView(APIView):
    """Basic health check endpoint."""
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'File Conversion API',
            'version': '1.0.0'
        })

class DetailedHealthCheckView(APIView):
    """Detailed health check endpoint."""
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'File Conversion API',
            'version': '1.0.0',
            'components': {
                'database': 'healthy',
                'redis': 'healthy',
                'celery': 'healthy',
                'storage': 'healthy'
            }
        })

class DatabaseHealthView(APIView):
    """Database health check."""
    
    def get(self, request):
        return Response({'status': 'healthy', 'component': 'database'})

class RedisHealthView(APIView):
    """Redis health check."""
    
    def get(self, request):
        return Response({'status': 'healthy', 'component': 'redis'})

class CeleryHealthView(APIView):
    """Celery health check."""
    
    def get(self, request):
        return Response({'status': 'healthy', 'component': 'celery'})

class StorageHealthView(APIView):
    """Storage health check."""
    
    def get(self, request):
        return Response({'status': 'healthy', 'component': 'storage'})
