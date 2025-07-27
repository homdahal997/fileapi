from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import ConversionJob, FileFormat
from .converter import FileConverterService
import json

def conversion_form(request):
    """Simple HTML form for file conversion"""
    formats = FileFormat.objects.filter(is_input_supported=True).values_list('name', flat=True)
    output_formats = FileFormat.objects.filter(is_output_supported=True).values_list('name', flat=True)
    
    context = {
        'input_formats': formats,
        'output_formats': output_formats,
    }
    return render(request, 'conversions/conversion_form.html', context)

@csrf_exempt
def simple_convert(request):
    """Handle file conversion from the simple form"""
    if request.method == 'POST':
        try:
            input_file = request.FILES.get('input_file')
            output_format = request.POST.get('output_format')
            
            if not input_file or not output_format:
                messages.error(request, 'Please provide both file and output format')
                return redirect('conversion-form')
            
            # Create conversion job
            converter = FileConverterService()
            job = converter.create_conversion_job(
                input_file=input_file,
                output_format=output_format,
                user=request.user if request.user.is_authenticated else None
            )
            
            # Perform conversion
            result = converter.convert_file(job.id)
            
            if result['success']:
                messages.success(request, f'Conversion successful! Job ID: {job.id}')
                return redirect('conversion-result', job_id=job.id)
            else:
                messages.error(request, f'Conversion failed: {result["error"]}')
                return redirect('conversion-form')
                
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('conversion-form')
    
    return redirect('conversion-form')

def conversion_result(request, job_id):
    """Display conversion result"""
    try:
        job = ConversionJob.objects.get(id=job_id)
        context = {'job': job}
        return render(request, 'conversions/conversion_result.html', context)
    except ConversionJob.DoesNotExist:
        messages.error(request, 'Conversion job not found')
        return redirect('conversion-form')
