"""
Celery configuration for file conversion tasks.
"""
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fileconvert_api.settings')

app = Celery('fileconvert_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    'reset-monthly-quotas': {
        'task': 'conversions.tasks.reset_monthly_quotas',
        'schedule': 86400.0,  # Run daily to check for quota resets
    },
    'cleanup-old-files': {
        'task': 'conversions.tasks.cleanup_old_files',
        'schedule': 3600.0,  # Run hourly
    },
    'retry-failed-jobs': {
        'task': 'conversions.tasks.retry_failed_jobs',
        'schedule': 1800.0,  # Run every 30 minutes
    },
    'update-storage-usage': {
        'task': 'storage_integrations.tasks.update_storage_usage',
        'schedule': 3600.0,  # Run hourly
    },
}

# Task routing
app.conf.task_routes = {
    'conversions.tasks.convert_file': {'queue': 'conversion'},
    'conversions.tasks.batch_convert': {'queue': 'batch'},
    'storage_integrations.tasks.*': {'queue': 'storage'},
    'authentication.tasks.*': {'queue': 'auth'},
}

# Task priorities
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True
app.conf.worker_disable_rate_limits = False

# Result backend settings
app.conf.result_expires = 3600  # 1 hour

# Error handling
app.conf.task_reject_on_worker_lost = True
app.conf.task_ignore_result = False

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
