"""
Simple API views for direct integration (matching client expectations).
"""
import os
import uuid
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile

from .models import ConversionJob, FileFormat
from .converter import converter_service, ConversionError


class SimpleConvertView(APIView):
    """Simple API view that matches client expectations."""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        """Convert a file - expects 'input_file' and 'output_format'."""
        try:
            # Get file and output format from request
            input_file = request.FILES.get('input_file')
            output_format = request.data.get('output_format', '').lower()
            
            if not input_file:
                return Response(
                    {'error': 'input_file is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not output_format:
                return Response(
                    {'error': 'output_format is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate file size (100MB max)
            if input_file.size > 100 * 1024 * 1024:
                return Response(
                    {'error': 'File size must not exceed 100MB'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Detect input format from file extension
            filename = input_file.name.lower()
            if '.' not in filename:
                return Response(
                    {'error': 'File must have an extension'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            input_format = filename.split('.')[-1]
            
            # Validate formats
            try:
                input_format_obj = FileFormat.objects.get(
                    name=input_format, 
                    is_input_supported=True
                )
                output_format_obj = FileFormat.objects.get(
                    name=output_format, 
                    is_output_supported=True
                )
            except FileFormat.DoesNotExist:
                return Response(
                    {'error': f'Conversion from {input_format} to {output_format} is not supported'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create conversion job
            job = ConversionJob.objects.create(
                user=request.user if request.user.is_authenticated else None,
                input_format=input_format_obj,
                output_format=output_format_obj,
                input_file_size=input_file.size,
                status='processing',
                started_at=timezone.now()
            )
            
            # Save input file
            input_filename = f"conversions/input/{job.id}_{input_file.name}"
            job.input_file.save(input_filename, input_file, save=False)
            job.save()
            
            try:
                # Perform conversion
                converted_content, output_filename = converter_service.convert_file(
                    input_file, input_format, output_format, {}
                )
                
                # Save output file
                output_file_path = f"conversions/output/{job.id}_{output_filename}"
                output_file = ContentFile(converted_content)
                job.output_file.save(output_file_path, output_file, save=False)
                job.output_file_size = len(converted_content)
                job.status = 'completed'
                job.completed_at = timezone.now()
                job.progress_percentage = 100
                
            except ConversionError as e:
                job.status = 'failed'
                job.error_message = str(e)
                job.completed_at = timezone.now()
            except Exception as e:
                job.status = 'failed'
                job.error_message = f'Conversion failed: {str(e)}'
                job.completed_at = timezone.now()
            
            job.save()
            
            # Return response in expected format
            return Response({
                'job_id': str(job.id),
                'status': job.status,
                'input_format': input_format,
                'output_format': output_format,
                'created_at': job.created_at.isoformat(),
                'error_message': job.error_message if job.status == 'failed' else None
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Conversion failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SimpleJobStatusView(APIView):
    """Simple job status view."""
    
    def get(self, request, job_id):
        """Get job status."""
        try:
            job = get_object_or_404(ConversionJob, id=job_id)
            
            response_data = {
                'job_id': str(job.id),
                'status': job.status,
                'input_format': job.input_format.name,
                'output_format': job.output_format.name,
                'created_at': job.created_at.isoformat(),
                'progress_percentage': job.progress_percentage or 0,
            }
            
            if job.status == 'completed':
                response_data['download_url'] = f'/api/convert/{job.id}/download/'
            elif job.status == 'failed':
                response_data['error_message'] = job.error_message
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to get job status: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SimpleDownloadView(APIView):
    """Simple download view."""
    
    def get(self, request, job_id):
        """Download converted file."""
        try:
            job = get_object_or_404(ConversionJob, id=job_id)
            
            if job.status != 'completed' or not job.output_file:
                return Response(
                    {'error': 'File not ready for download'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Read file content
            try:
                file_content = job.output_file.read()
            except Exception:
                return Response(
                    {'error': 'File not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Create response
            response = HttpResponse(
                file_content,
                content_type='application/octet-stream'
            )
            
            # Set download headers
            original_name = os.path.basename(job.input_file.name) if job.input_file else 'converted_file'
            base_name = original_name.rsplit('.', 1)[0] if '.' in original_name else original_name
            filename = f"{base_name}.{job.output_format.name}"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(file_content)
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Download failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
