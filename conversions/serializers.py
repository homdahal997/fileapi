"""
Serializers for the conversions app.
"""
from rest_framework import serializers
from .models import (
    FileFormat, ConversionJob, BatchConversionJob, 
    ConversionQuota, ConversionHistory
)


class FileFormatSerializer(serializers.ModelSerializer):
    """Serializer for file formats."""
    
    class Meta:
        model = FileFormat
        fields = ['id', 'name', 'category', 'mime_type', 'description', 
                 'is_input_supported', 'is_output_supported']


class ConversionJobSerializer(serializers.ModelSerializer):
    """Serializer for conversion jobs."""
    
    input_format_name = serializers.CharField(source='input_format.name', read_only=True)
    output_format_name = serializers.CharField(source='output_format.name', read_only=True)
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ConversionJob
        fields = [
            'id', 'user', 'input_file', 'input_format', 'output_format',
            'input_format_name', 'output_format_name', 'output_file', 'download_url',
            'status', 'priority', 'progress_percentage', 'conversion_options',
            'created_at', 'updated_at', 'started_at', 'completed_at',
            'error_message', 'retry_count', 'max_retries', 'webhook_url',
            'input_file_size', 'output_file_size', 'is_completed', 'duration'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at', 'started_at', 
            'completed_at', 'output_file', 'progress_percentage', 'status',
            'error_message', 'retry_count', 'input_file_size', 'output_file_size'
        ]
    
    def get_download_url(self, obj):
        """Generate download URL for completed conversions."""
        if obj.status == 'completed' and obj.output_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(f'/api/v1/conversions/jobs/{obj.id}/download/')
        return None


class ConversionJobCreateSerializer(serializers.Serializer):
    """Serializer for creating conversion jobs."""
    
    file = serializers.FileField()
    output_format = serializers.CharField(max_length=10)
    conversion_options = serializers.JSONField(required=False, default=dict)
    webhook_url = serializers.URLField(required=False, allow_blank=True)
    priority = serializers.IntegerField(default=2, min_value=1, max_value=4)

    def validate_output_format(self, value):
        """Validate that the output format is supported."""
        if not FileFormat.objects.filter(name=value.lower(), is_output_supported=True).exists():
            raise serializers.ValidationError(f"Output format '{value}' is not supported.")
        return value.lower()

    def validate_file(self, value):
        """Validate uploaded file."""
        # Check file size (max 100MB)
        max_size = 100 * 1024 * 1024  # 100MB
        if value.size > max_size:
            raise serializers.ValidationError("File size must not exceed 100MB.")
        
        # Get file extension
        filename = value.name.lower()
        if '.' not in filename:
            raise serializers.ValidationError("File must have an extension.")
        
        file_ext = filename.split('.')[-1]
        
        # Check if input format is supported
        if not FileFormat.objects.filter(name=file_ext, is_input_supported=True).exists():
            raise serializers.ValidationError(f"Input format '{file_ext}' is not supported.")
        
        return value


class BatchConversionJobSerializer(serializers.ModelSerializer):
    """Serializer for batch conversion jobs."""
    
    individual_jobs = ConversionJobSerializer(many=True, read_only=True)
    
    class Meta:
        model = BatchConversionJob
        fields = [
            'id', 'user', 'name', 'description', 'output_format',
            'conversion_options', 'status', 'created_at', 'updated_at',
            'started_at', 'completed_at', 'webhook_url', 'webhook_sent',
            'total_files', 'completed_files', 'failed_files', 'progress_percentage',
            'individual_jobs'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at', 'started_at', 
            'completed_at', 'status', 'webhook_sent'
        ]


class ConversionQuotaSerializer(serializers.ModelSerializer):
    """Serializer for conversion quotas."""
    
    class Meta:
        model = ConversionQuota
        fields = [
            'user', 'monthly_conversions_limit', 'monthly_conversions_used',
            'monthly_storage_limit_mb', 'monthly_storage_used_mb',
            'last_reset_date', 'is_premium', 'premium_expires_at',
            'conversions_remaining', 'storage_remaining_mb'
        ]
        read_only_fields = ['user', 'last_reset_date']


class ConversionHistorySerializer(serializers.ModelSerializer):
    """Serializer for conversion history."""
    
    class Meta:
        model = ConversionHistory
        fields = [
            'id', 'user', 'conversion_job', 'input_format', 'output_format',
            'file_size_bytes', 'processing_time_seconds', 'created_at',
            'ip_address', 'user_agent'
        ]
        read_only_fields = ['id', 'user', 'created_at']
