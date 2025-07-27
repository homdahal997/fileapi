from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import ConversionJob, FileFormat

@admin.register(FileFormat)
class FileFormatAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'mime_type', 'is_input_supported', 'is_output_supported']
    list_filter = ['category', 'is_input_supported', 'is_output_supported']
    search_fields = ['name', 'mime_type']

@admin.register(ConversionJob)
class ConversionJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'input_format', 'output_format', 'status', 'created_at', 'download_link']
    list_filter = ['status', 'input_format', 'output_format', 'created_at']
    search_fields = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'input_file', 'output_file']
    
    def download_link(self, obj):
        if obj.status == 'completed' and obj.output_file:
            url = reverse('download-result', kwargs={'job_id': obj.id})
            return format_html('<a href="{}" target="_blank">Download</a>', url)
        return "Not available"
    download_link.short_description = "Download"
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
