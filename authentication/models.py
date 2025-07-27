"""
Authentication models for API key management and user profiles.
"""
import secrets
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with additional information."""
    
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Plan information
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    plan_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Contact information
    company = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Preferences
    webhook_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Usage tracking
    total_conversions = models.IntegerField(default=0)
    total_storage_used_mb = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.plan}"
    
    @property
    def is_premium(self):
        return self.plan in ['pro', 'enterprise']
    
    @property
    def plan_active(self):
        if self.plan == 'free':
            return True
        return self.plan_expires_at and self.plan_expires_at > timezone.now()


class APIKey(models.Model):
    """Model for managing API keys."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True, editable=False)
    prefix = models.CharField(max_length=8, editable=False)
    
    # Permissions
    is_active = models.BooleanField(default=True)
    permissions = models.JSONField(default=dict)  # Store specific permissions
    
    # Usage tracking
    last_used = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    
    # Rate limiting
    rate_limit_requests_per_hour = models.IntegerField(default=1000)
    
    # Expiration
    expires_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'api_keys'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            self.prefix = self.key[:8]
        super().save(*args, **kwargs)
    
    def generate_key(self):
        """Generate a secure API key."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(64))
    
    def __str__(self):
        return f"{self.name} ({self.prefix}...)"
    
    @property
    def is_valid(self):
        """Check if the API key is valid and not expired."""
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
    
    @property
    def masked_key(self):
        """Return a masked version of the key for display."""
        return f"{self.prefix}{'*' * 48}{self.key[-8:]}"


class APIKeyUsage(models.Model):
    """Track API key usage for rate limiting and analytics."""
    
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, related_name='usage_logs')
    
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    
    # Request metadata
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    
    # Performance tracking
    response_time_ms = models.FloatField()
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'api_key_usage'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['api_key', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.api_key.name} - {self.endpoint} ({self.timestamp})"


class RefreshToken(models.Model):
    """Model for managing JWT refresh tokens."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.CharField(max_length=255, unique=True)
    
    # Device information
    device_info = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField()
    
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'refresh_tokens'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refresh token for {self.user.username}"
    
    @property
    def is_valid(self):
        """Check if the refresh token is valid and not expired."""
        return self.is_active and self.expires_at > timezone.now()


class LoginAttempt(models.Model):
    """Track login attempts for security monitoring."""
    
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    
    success = models.BooleanField()
    failure_reason = models.CharField(max_length=100, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'login_attempts'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['username', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.username} - {status} ({self.timestamp})"
