"""
Management command to populate the FileFormat model with supported formats.
"""
from django.core.management.base import BaseCommand
from conversions.models import FileFormat


class Command(BaseCommand):
    help = 'Populate the FileFormat model with supported file formats'

    def handle(self, *args, **options):
        """Populate file formats."""
        
        formats_data = [
            # Document formats
            {'name': 'pdf', 'category': 'document', 'mime_type': 'application/pdf', 
             'description': 'Portable Document Format', 'input': True, 'output': True},
            {'name': 'docx', 'category': 'document', 'mime_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
             'description': 'Microsoft Word Document', 'input': True, 'output': True},
            {'name': 'doc', 'category': 'document', 'mime_type': 'application/msword',
             'description': 'Microsoft Word Document (Legacy)', 'input': True, 'output': True},
            {'name': 'txt', 'category': 'document', 'mime_type': 'text/plain',
             'description': 'Plain Text', 'input': True, 'output': True},
            {'name': 'rtf', 'category': 'document', 'mime_type': 'application/rtf',
             'description': 'Rich Text Format', 'input': True, 'output': True},
            {'name': 'odt', 'category': 'document', 'mime_type': 'application/vnd.oasis.opendocument.text',
             'description': 'OpenDocument Text', 'input': True, 'output': True},
            {'name': 'html', 'category': 'document', 'mime_type': 'text/html',
             'description': 'HyperText Markup Language', 'input': True, 'output': True},
            {'name': 'epub', 'category': 'ebook', 'mime_type': 'application/epub+zip',
             'description': 'Electronic Publication', 'input': True, 'output': True},
            {'name': 'mobi', 'category': 'ebook', 'mime_type': 'application/x-mobipocket-ebook',
             'description': 'Mobipocket eBook', 'input': True, 'output': True},
            {'name': 'azw3', 'category': 'ebook', 'mime_type': 'application/vnd.amazon.ebook',
             'description': 'Amazon Kindle Format', 'input': True, 'output': True},

            # Image formats
            {'name': 'jpg', 'category': 'image', 'mime_type': 'image/jpeg',
             'description': 'JPEG Image', 'input': True, 'output': True},
            {'name': 'jpeg', 'category': 'image', 'mime_type': 'image/jpeg',
             'description': 'JPEG Image', 'input': True, 'output': True},
            {'name': 'png', 'category': 'image', 'mime_type': 'image/png',
             'description': 'Portable Network Graphics', 'input': True, 'output': True},
            {'name': 'gif', 'category': 'image', 'mime_type': 'image/gif',
             'description': 'Graphics Interchange Format', 'input': True, 'output': True},
            {'name': 'bmp', 'category': 'image', 'mime_type': 'image/bmp',
             'description': 'Bitmap Image', 'input': True, 'output': True},
            {'name': 'tiff', 'category': 'image', 'mime_type': 'image/tiff',
             'description': 'Tagged Image File Format', 'input': True, 'output': True},
            {'name': 'webp', 'category': 'image', 'mime_type': 'image/webp',
             'description': 'WebP Image', 'input': True, 'output': True},
            {'name': 'svg', 'category': 'image', 'mime_type': 'image/svg+xml',
             'description': 'Scalable Vector Graphics', 'input': True, 'output': True},
            {'name': 'ico', 'category': 'image', 'mime_type': 'image/x-icon',
             'description': 'Icon Format', 'input': True, 'output': True},
            {'name': 'avif', 'category': 'image', 'mime_type': 'image/avif',
             'description': 'AV1 Image File Format', 'input': True, 'output': True},

            # Spreadsheet formats
            {'name': 'xlsx', 'category': 'spreadsheet', 'mime_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
             'description': 'Microsoft Excel Spreadsheet', 'input': True, 'output': True},
            {'name': 'xls', 'category': 'spreadsheet', 'mime_type': 'application/vnd.ms-excel',
             'description': 'Microsoft Excel Spreadsheet (Legacy)', 'input': True, 'output': True},
            {'name': 'csv', 'category': 'spreadsheet', 'mime_type': 'text/csv',
             'description': 'Comma Separated Values', 'input': True, 'output': True},
            {'name': 'ods', 'category': 'spreadsheet', 'mime_type': 'application/vnd.oasis.opendocument.spreadsheet',
             'description': 'OpenDocument Spreadsheet', 'input': True, 'output': True},
            {'name': 'tsv', 'category': 'spreadsheet', 'mime_type': 'text/tab-separated-values',
             'description': 'Tab Separated Values', 'input': True, 'output': True},

            # Presentation formats
            {'name': 'pptx', 'category': 'presentation', 'mime_type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
             'description': 'Microsoft PowerPoint Presentation', 'input': True, 'output': True},
            {'name': 'ppt', 'category': 'presentation', 'mime_type': 'application/vnd.ms-powerpoint',
             'description': 'Microsoft PowerPoint Presentation (Legacy)', 'input': True, 'output': True},
            {'name': 'odp', 'category': 'presentation', 'mime_type': 'application/vnd.oasis.opendocument.presentation',
             'description': 'OpenDocument Presentation', 'input': True, 'output': True},

            # Audio formats
            {'name': 'mp3', 'category': 'audio', 'mime_type': 'audio/mpeg',
             'description': 'MPEG Audio Layer 3', 'input': True, 'output': True},
            {'name': 'wav', 'category': 'audio', 'mime_type': 'audio/wav',
             'description': 'Waveform Audio File Format', 'input': True, 'output': True},
            {'name': 'flac', 'category': 'audio', 'mime_type': 'audio/flac',
             'description': 'Free Lossless Audio Codec', 'input': True, 'output': True},
            {'name': 'aac', 'category': 'audio', 'mime_type': 'audio/aac',
             'description': 'Advanced Audio Codec', 'input': True, 'output': True},
            {'name': 'ogg', 'category': 'audio', 'mime_type': 'audio/ogg',
             'description': 'Ogg Vorbis Audio', 'input': True, 'output': True},
            {'name': 'm4a', 'category': 'audio', 'mime_type': 'audio/mp4',
             'description': 'MPEG-4 Audio', 'input': True, 'output': True},
            {'name': 'wma', 'category': 'audio', 'mime_type': 'audio/x-ms-wma',
             'description': 'Windows Media Audio', 'input': True, 'output': True},

            # Video formats
            {'name': 'mp4', 'category': 'video', 'mime_type': 'video/mp4',
             'description': 'MPEG-4 Video', 'input': True, 'output': True},
            {'name': 'avi', 'category': 'video', 'mime_type': 'video/x-msvideo',
             'description': 'Audio Video Interleave', 'input': True, 'output': True},
            {'name': 'mov', 'category': 'video', 'mime_type': 'video/quicktime',
             'description': 'QuickTime Movie', 'input': True, 'output': True},
            {'name': 'wmv', 'category': 'video', 'mime_type': 'video/x-ms-wmv',
             'description': 'Windows Media Video', 'input': True, 'output': True},
            {'name': 'flv', 'category': 'video', 'mime_type': 'video/x-flv',
             'description': 'Flash Video', 'input': True, 'output': True},
            {'name': 'webm', 'category': 'video', 'mime_type': 'video/webm',
             'description': 'WebM Video', 'input': True, 'output': True},
            {'name': 'mkv', 'category': 'video', 'mime_type': 'video/x-matroska',
             'description': 'Matroska Video', 'input': True, 'output': True},

            # Archive formats
            {'name': 'zip', 'category': 'archive', 'mime_type': 'application/zip',
             'description': 'ZIP Archive', 'input': True, 'output': True},
            {'name': 'rar', 'category': 'archive', 'mime_type': 'application/x-rar-compressed',
             'description': 'RAR Archive', 'input': True, 'output': False},
            {'name': '7z', 'category': 'archive', 'mime_type': 'application/x-7z-compressed',
             'description': '7-Zip Archive', 'input': True, 'output': True},
            {'name': 'tar', 'category': 'archive', 'mime_type': 'application/x-tar',
             'description': 'Tape Archive', 'input': True, 'output': True},
            {'name': 'gz', 'category': 'archive', 'mime_type': 'application/gzip',
             'description': 'Gzip Compressed Archive', 'input': True, 'output': True},

            # Code/Data formats
            {'name': 'json', 'category': 'data', 'mime_type': 'application/json',
             'description': 'JavaScript Object Notation', 'input': True, 'output': True},
            {'name': 'xml', 'category': 'data', 'mime_type': 'application/xml',
             'description': 'Extensible Markup Language', 'input': True, 'output': True},
            {'name': 'yaml', 'category': 'data', 'mime_type': 'application/x-yaml',
             'description': 'YAML Ain\'t Markup Language', 'input': True, 'output': True},
            {'name': 'yml', 'category': 'data', 'mime_type': 'application/x-yaml',
             'description': 'YAML Ain\'t Markup Language', 'input': True, 'output': True},

            # Font formats
            {'name': 'ttf', 'category': 'font', 'mime_type': 'font/ttf',
             'description': 'TrueType Font', 'input': True, 'output': True},
            {'name': 'otf', 'category': 'font', 'mime_type': 'font/otf',
             'description': 'OpenType Font', 'input': True, 'output': True},
            {'name': 'woff', 'category': 'font', 'mime_type': 'font/woff',
             'description': 'Web Open Font Format', 'input': True, 'output': True},
            {'name': 'woff2', 'category': 'font', 'mime_type': 'font/woff2',
             'description': 'Web Open Font Format 2', 'input': True, 'output': True},
        ]

        created_count = 0
        updated_count = 0

        for format_data in formats_data:
            format_obj, created = FileFormat.objects.get_or_create(
                name=format_data['name'],
                defaults={
                    'category': format_data['category'],
                    'mime_type': format_data['mime_type'],
                    'description': format_data['description'],
                    'is_input_supported': format_data['input'],
                    'is_output_supported': format_data['output'],
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created format: {format_data["name"]}')
                )
            else:
                # Update existing format
                format_obj.category = format_data['category']
                format_obj.mime_type = format_data['mime_type']
                format_obj.description = format_data['description']
                format_obj.is_input_supported = format_data['input']
                format_obj.is_output_supported = format_data['output']
                format_obj.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated format: {format_data["name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created {created_count} new formats, '
                f'updated {updated_count} existing formats.'
            )
        )
