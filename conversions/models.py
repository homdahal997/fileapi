"""
Models for the conversions app.
"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class FileFormat(models.Model):
    """Model to store supported file formats."""
    
    name = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=50)
    mime_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_input_supported = models.BooleanField(default=True)
    is_output_supported = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'file_formats'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class ConversionJob(models.Model):
    """Model to track file conversion jobs."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Normal'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversion_jobs', null=True, blank=True)
    
    # File information
    input_file = models.FileField(upload_to='input_files/%Y/%m/%d/')
    input_format = models.ForeignKey(
        FileFormat, 
        on_delete=models.CASCADE, 
        related_name='input_conversions'
    )
    output_format = models.ForeignKey(
        FileFormat, 
        on_delete=models.CASCADE, 
        related_name='output_conversions'
    )
    output_file = models.FileField(upload_to='output_files/%Y/%m/%d/', null=True, blank=True)
    
    # Job metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    progress_percentage = models.FloatField(default=0.0)
    
    # Conversion options
    conversion_options = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    
    # Webhook configuration
    webhook_url = models.URLField(blank=True)
    webhook_sent = models.BooleanField(default=False)
    
    # File size tracking
    input_file_size = models.BigIntegerField(null=True, blank=True)
    output_file_size = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'conversion_jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status', 'priority']),
        ]
    
    def __str__(self):
        return f"Job {self.id}: {self.input_format.name} → {self.output_format.name}"
    
    @property
    def is_completed(self):
        return self.status in ['completed', 'failed', 'cancelled']
    
    @property
    def duration(self):
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None


class BatchConversionJob(models.Model):
    """Model for batch conversion jobs."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='batch_jobs')
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    output_format = models.ForeignKey(FileFormat, on_delete=models.CASCADE)
    conversion_options = models.JSONField(default=dict, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    webhook_url = models.URLField(blank=True)
    webhook_sent = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'batch_conversion_jobs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Batch Job {self.id}: {self.name}"
    
    @property
    def total_files(self):
        return self.individual_jobs.count()
    
    @property
    def completed_files(self):
        return self.individual_jobs.filter(status='completed').count()
    
    @property
    def failed_files(self):
        return self.individual_jobs.filter(status='failed').count()
    
    @property
    def progress_percentage(self):
        total = self.total_files
        if total == 0:
            return 0
        completed = self.completed_files
        return (completed / total) * 100


class BatchJobFile(models.Model):
    """Model to track individual files in a batch job."""
    
    batch_job = models.ForeignKey(
        BatchConversionJob, 
        on_delete=models.CASCADE, 
        related_name='individual_jobs'
    )
    conversion_job = models.OneToOneField(
        ConversionJob, 
        on_delete=models.CASCADE,
        related_name='batch_file'
    )
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'batch_job_files'
        ordering = ['order']
        unique_together = ['batch_job', 'order']


class ConversionQuota(models.Model):
    """Model to track user conversion quotas."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='quota')
    
    # Monthly limits
    monthly_conversions_limit = models.IntegerField(default=100)
    monthly_conversions_used = models.IntegerField(default=0)
    monthly_storage_limit_mb = models.IntegerField(default=1000)  # 1GB
    monthly_storage_used_mb = models.IntegerField(default=0)
    
    # Reset tracking
    last_reset_date = models.DateField(auto_now_add=True)
    
    # Premium features
    is_premium = models.BooleanField(default=False)
    premium_expires_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversion_quotas'
    
    def __str__(self):
        return f"Quota for {self.user.username}"
    
    @property
    def conversions_remaining(self):
        return max(0, self.monthly_conversions_limit - self.monthly_conversions_used)
    
    @property
    def storage_remaining_mb(self):
        return max(0, self.monthly_storage_limit_mb - self.monthly_storage_used_mb)


class ConversionHistory(models.Model):
    """Model to track conversion history and analytics."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversion_history')
    conversion_job = models.ForeignKey(ConversionJob, on_delete=models.CASCADE)
    
    # Analytics data
    input_format = models.CharField(max_length=10)
    output_format = models.CharField(max_length=10)
    file_size_bytes = models.BigIntegerField()
    processing_time_seconds = models.FloatField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        db_table = 'conversion_history'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['input_format', 'output_format']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.input_format} → {self.output_format}"
