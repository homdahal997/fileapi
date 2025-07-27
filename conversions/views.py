"""
Views for the conversions app.
"""
import os
import uuid
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from .models import ConversionJob, FileFormat, BatchConversionJob, ConversionQuota, ConversionHistory
from .serializers import (
    ConversionJobSerializer, ConversionJobCreateSerializer, FileFormatSerializer,
    BatchConversionJobSerializer, ConversionQuotaSerializer, ConversionHistorySerializer
)
from .converter import converter_service, ConversionError


class FileFormatViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for file formats."""
    queryset = FileFormat.objects.all()
    serializer_class = FileFormatSerializer
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all available format categories."""
        categories = FileFormat.objects.values_list('category', flat=True).distinct()
        return Response({'categories': list(categories)})
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get formats grouped by category."""
        formats_by_category = {}
        for format_obj in FileFormat.objects.all():
            if format_obj.category not in formats_by_category:
                formats_by_category[format_obj.category] = []
            formats_by_category[format_obj.category].append({
                'id': format_obj.id,
                'name': format_obj.name,
                'mime_type': format_obj.mime_type,
                'description': format_obj.description,
                'is_input_supported': format_obj.is_input_supported,
                'is_output_supported': format_obj.is_output_supported,
            })
        return Response(formats_by_category)


class ConvertFileView(APIView):
    """API view for file conversion."""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        """Convert a file to a different format."""
        serializer = ConversionJobCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = serializer.validated_data['file']
        output_format = serializer.validated_data['output_format']
        conversion_options = serializer.validated_data.get('conversion_options', {})
        webhook_url = serializer.validated_data.get('webhook_url')
        priority = serializer.validated_data.get('priority', 2)
        
        try:
            # Detect input format from file extension
            filename = uploaded_file.name.lower()
            input_format = filename.split('.')[-1] if '.' in filename else ''
            
            # Get or create format objects
            input_format_obj = get_object_or_404(FileFormat, name=input_format, is_input_supported=True)
            output_format_obj = get_object_or_404(FileFormat, name=output_format, is_output_supported=True)
            
            # Create conversion job
            job_data = {
                'user': request.user if request.user.is_authenticated else None,
                'input_format': input_format_obj,
                'output_format': output_format_obj,
                'conversion_options': conversion_options,
                'priority': priority,
                'input_file_size': uploaded_file.size,
                'status': 'processing'
            }
            
            # Only add webhook_url if it's provided and not empty
            if webhook_url:
                job_data['webhook_url'] = webhook_url
            
            job = ConversionJob.objects.create(**job_data)
            
            # Save input file
            input_filename = f"conversions/input/{job.id}_{uploaded_file.name}"
            job.input_file.save(input_filename, uploaded_file, save=False)
            job.started_at = timezone.now()
            job.save()
            
            try:
                # Perform conversion
                converted_content, output_filename = converter_service.convert_file(
                    uploaded_file, input_format, output_format, conversion_options
                )
                
                # Save output file
                output_file_path = f"conversions/output/{job.id}_{output_filename}"
                output_file = ContentFile(converted_content)
                job.output_file.save(output_file_path, output_file, save=False)
                job.output_file_size = len(converted_content)
                job.status = 'completed'
                job.completed_at = timezone.now()
                job.progress_percentage = 100
                
                # Create conversion history
                if request.user.is_authenticated:
                    ConversionHistory.objects.create(
                        user=request.user,
                        conversion_job=job,
                        input_format=input_format_obj,
                        output_format=output_format_obj,
                        file_size_bytes=uploaded_file.size,
                        processing_time_seconds=(job.completed_at - job.started_at).total_seconds(),
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                
            except ConversionError as e:
                job.status = 'failed'
                job.error_message = str(e)
                job.completed_at = timezone.now()
            
            job.save()
            
            # Return job details with request context for download URL
            serializer = ConversionJobSerializer(job, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Conversion failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ConversionJobViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversion jobs."""
    queryset = ConversionJob.objects.all()
    serializer_class = ConversionJobSerializer
    
    def get_queryset(self):
        """Filter jobs by user if authenticated."""
        queryset = ConversionJob.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download the converted file."""
        job = self.get_object()
        
        if job.status != 'completed' or not job.output_file:
            return Response(
                {'error': 'File not available for download'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Get file content
            file_content = job.output_file.read()
            
            # Determine content type
            content_type = job.output_format.mime_type or 'application/octet-stream'
            
            # Create response
            response = HttpResponse(file_content, content_type=content_type)
            
            # Set filename
            filename = os.path.basename(job.output_file.name)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(file_content)
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Failed to download file: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """Retry a failed conversion."""
        job = self.get_object()
        
        if job.status not in ['failed', 'cancelled']:
            return Response(
                {'error': 'Only failed or cancelled jobs can be retried'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if job.retry_count >= job.max_retries:
            return Response(
                {'error': 'Maximum retry count exceeded'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reset job status
        job.status = 'processing'
        job.error_message = ''
        job.retry_count += 1
        job.started_at = timezone.now()
        job.completed_at = None
        job.progress_percentage = 0
        job.save()
        
        # TODO: Add to Celery queue for processing
        
        serializer = self.get_serializer(job)
        return Response(serializer.data)


class BatchConversionJobViewSet(viewsets.ModelViewSet):
    """ViewSet for batch conversion jobs."""
    queryset = BatchConversionJob.objects.all()
    serializer_class = BatchConversionJobSerializer
    
    def get_queryset(self):
        """Filter jobs by user if authenticated."""
        queryset = BatchConversionJob.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset.order_by('-created_at')


class ConversionQuotaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for conversion quotas."""
    queryset = ConversionQuota.objects.all()
    serializer_class = ConversionQuotaSerializer
    
    def get_queryset(self):
        """Filter quotas by user if authenticated."""
        if self.request.user.is_authenticated:
            return ConversionQuota.objects.filter(user=self.request.user)
        return ConversionQuota.objects.none()


class ConversionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for conversion history."""
    queryset = ConversionHistory.objects.all()
    serializer_class = ConversionHistorySerializer
    
    def get_queryset(self):
        """Filter history by user if authenticated."""
        if self.request.user.is_authenticated:
            return ConversionHistory.objects.filter(user=self.request.user).order_by('-created_at')
        return ConversionHistory.objects.none()


# Legacy API views for backward compatibility
class FileUploadView(APIView):
    def post(self, request):
        return Response({'message': 'Use /api/convert/ endpoint instead'})

class BatchConvertView(APIView):
    def post(self, request):
        return Response({'message': 'Batch convert endpoint'})

class CancelJobView(APIView):
    def post(self, request, job_id):
        return Response({'message': f'Cancel job {job_id}'})

class RetryJobView(APIView):
    def post(self, request, job_id):
        return Response({'message': f'Retry job {job_id}'})

class DownloadResultView(APIView):
    """Download converted file."""
    
    def get(self, request, job_id):
        try:
            job = get_object_or_404(ConversionJob, id=job_id)
            
            if job.status != 'completed' or not job.output_file:
                return Response(
                    {'error': 'File not ready for download'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the file path
            file_path = job.output_file.path
            
            if not os.path.exists(file_path):
                return Response(
                    {'error': 'File not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Create response with file content
            with open(file_path, 'rb') as f:
                response = HttpResponse(
                    f.read(),
                    content_type='application/octet-stream'
                )
                
            # Set download headers
            filename = f"converted_file.{job.output_format.name}"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Download failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class JobProgressView(APIView):
    def get(self, request, job_id):
        return Response({'message': f'Progress for job {job_id}'})

class CancelBatchJobView(APIView):
    def post(self, request, batch_id):
        return Response({'message': f'Cancel batch job {batch_id}'})

class BatchJobProgressView(APIView):
    def get(self, request, batch_id):
        return Response({'message': f'Batch job progress {batch_id}'})

class ValidateFormatView(APIView):
    def post(self, request):
        return Response({'message': 'Validate format'})

class SupportedConversionsView(APIView):
    def get(self, request):
        return Response({'message': 'Supported conversions'})

class UserQuotaView(APIView):
    def get(self, request):
        return Response({'message': 'User quota'})

class ConversionAnalyticsView(APIView):
    def get(self, request):
        return Response({'message': 'Conversion analytics'})

class TestWebhookView(APIView):
    def post(self, request):
        return Response({'message': 'Test webhook'})
