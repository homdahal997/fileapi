"""
Models for cloud storage integrations.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CloudStorageProvider(models.Model):
    """Model to define supported cloud storage providers."""
    
    PROVIDER_CHOICES = [
        ('aws_s3', 'Amazon S3'),
        ('google_cloud', 'Google Cloud Storage'),
        ('dropbox', 'Dropbox'),
        ('azure_blob', 'Azure Blob Storage'),
        ('one_drive', 'Microsoft OneDrive'),
    ]
    
    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    supports_import = models.BooleanField(default=True)
    supports_export = models.BooleanField(default=True)
    
    # Configuration schema for validation
    required_fields = models.JSONField(default=list)
    optional_fields = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cloud_storage_providers'
        ordering = ['display_name']
    
    def __str__(self):
        return self.display_name


class UserCloudStorage(models.Model):
    """Model to store user's cloud storage configurations."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cloud_storages')
    provider = models.ForeignKey(CloudStorageProvider, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)  # User-defined name for this connection
    
    # Encrypted storage credentials
    credentials = models.JSONField()  # Store encrypted credentials
    
    # Configuration
    default_bucket = models.CharField(max_length=255, blank=True)
    default_folder = models.CharField(max_length=500, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Connection testing
    last_tested = models.DateTimeField(null=True, blank=True)
    connection_status = models.CharField(
        max_length=20,
        choices=[
            ('unknown', 'Unknown'),
            ('connected', 'Connected'),
            ('error', 'Error'),
        ],
        default='unknown'
    )
    connection_error = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_cloud_storages'
        ordering = ['-is_default', 'name']
        unique_together = ['user', 'name']
    
    def clean(self):
        # Ensure only one default storage per user
        if self.is_default:
            existing_default = UserCloudStorage.objects.filter(
                user=self.user, is_default=True
            ).exclude(pk=self.pk)
            if existing_default.exists():
                raise ValidationError("User can only have one default cloud storage.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.provider.display_name})"


class CloudStorageImport(models.Model):
    """Model to track file imports from cloud storage."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('downloading', 'Downloading'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='storage_imports')
    cloud_storage = models.ForeignKey(UserCloudStorage, on_delete=models.CASCADE)
    
    # Source file information
    source_path = models.CharField(max_length=1000)
    source_file_name = models.CharField(max_length=255)
    source_file_size = models.BigIntegerField(null=True, blank=True)
    
    # Local file information
    local_file = models.FileField(upload_to='imported_files/%Y/%m/%d/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    # Progress tracking
    progress_percentage = models.FloatField(default=0.0)
    bytes_downloaded = models.BigIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'cloud_storage_imports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Import: {self.source_file_name} from {self.cloud_storage.name}"


class CloudStorageExport(models.Model):
    """Model to track file exports to cloud storage."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('uploading', 'Uploading'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='storage_exports')
    cloud_storage = models.ForeignKey(UserCloudStorage, on_delete=models.CASCADE)
    
    # Source file (converted file)
    source_file = models.FileField(upload_to='temp_exports/')
    
    # Destination information
    destination_path = models.CharField(max_length=1000)
    destination_file_name = models.CharField(max_length=255)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    # Progress tracking
    progress_percentage = models.FloatField(default=0.0)
    bytes_uploaded = models.BigIntegerField(default=0)
    
    # Cloud storage metadata
    cloud_file_url = models.URLField(blank=True)
    cloud_file_id = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'cloud_storage_exports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Export: {self.destination_file_name} to {self.cloud_storage.name}"


class StorageQuota(models.Model):
    """Model to track storage usage across all providers."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='storage_quota')
    
    # Monthly quotas (in MB)
    monthly_import_limit_mb = models.IntegerField(default=5000)  # 5GB
    monthly_import_used_mb = models.IntegerField(default=0)
    monthly_export_limit_mb = models.IntegerField(default=5000)  # 5GB
    monthly_export_used_mb = models.IntegerField(default=0)
    
    # Reset tracking
    last_reset_date = models.DateField(auto_now_add=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'storage_quotas'
    
    def __str__(self):
        return f"Storage quota for {self.user.username}"
    
    @property
    def import_remaining_mb(self):
        return max(0, self.monthly_import_limit_mb - self.monthly_import_used_mb)
    
    @property
    def export_remaining_mb(self):
        return max(0, self.monthly_export_limit_mb - self.monthly_export_used_mb)


class StorageIntegrationLog(models.Model):
    """Model to log storage integration activities."""
    
    ACTION_CHOICES = [
        ('connect', 'Connect'),
        ('disconnect', 'Disconnect'),
        ('import', 'Import'),
        ('export', 'Export'),
        ('test_connection', 'Test Connection'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='storage_logs')
    cloud_storage = models.ForeignKey(
        UserCloudStorage, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.JSONField(default=dict)
    
    success = models.BooleanField()
    error_message = models.TextField(blank=True)
    
    # Request metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'storage_integration_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['cloud_storage', 'timestamp']),
        ]
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        storage_name = self.cloud_storage.name if self.cloud_storage else "N/A"
        return f"{self.user.username} - {self.action} ({storage_name}) - {status}"
