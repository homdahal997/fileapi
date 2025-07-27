# InMotion Hosting Deployment Guide for Django File Converter API

## Prerequisites
- InMotion Hosting VPS or Dedicated Server account
- Python 3.8+ support
- SSH access to your server

## Deployment Steps

### 1. Prepare Production Environment File

Create `.env` file in your project root:

```bash
# Production Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-here-change-this
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# Database Configuration (MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_database_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE=104857600
DATA_UPLOAD_MAX_MEMORY_SIZE=104857600

# Static/Media Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.yourdomain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your_email_password

# Security
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
```

### 2. Update requirements.txt for Production

Add MySQL support:
```
mysqlclient==2.2.4
```

### 3. Create Apache Configuration

Create `public_html/.htaccess`:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /django/fileconvert_api/wsgi.py/$1 [QSA,L]
```

### 4. Create passenger_wsgi.py

Create in your domain root directory:
```python
import sys
import os

# Add your project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'django', 'fileconvert_api'))

# Set environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'fileconvert_api.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5. Database Setup Commands

SSH into your server and run:
```bash
# Create database
mysql -u root -p
CREATE DATABASE your_database_name;
CREATE USER 'your_db_username'@'localhost' IDENTIFIED BY 'your_db_password';
GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_db_username'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Django migrations
cd /path/to/your/project
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6. File Permissions

Set proper permissions:
```bash
chmod 755 passenger_wsgi.py
chmod -R 755 static/
chmod -R 755 media/
chmod 600 .env
```

### 7. Subdomain Setup (Optional)

If you want to use a subdomain like `api.yourdomain.com`:

1. Create subdomain in cPanel
2. Point it to your Django application directory
3. Update ALLOWED_HOSTS in .env

### 8. SSL Certificate

Enable SSL through InMotion's Let's Encrypt or upload your certificate.

### 9. Testing Deployment

1. Visit your domain
2. Test the simple conversion interface at `/simple/`
3. Check admin panel at `/admin/`
4. Test API endpoints

### 10. Monitoring and Logs

Check logs in cPanel File Manager or via SSH:
```bash
tail -f ~/logs/error_log
tail -f ~/logs/access_log
```

## Important Notes

1. **File Conversion Libraries**: Ensure python-docx, PyPDF2, and reportlab are installed
2. **Memory Limits**: InMotion shared hosting may have memory limitations
3. **File Upload Size**: Check your hosting plan's upload limits
4. **Static Files**: Use WhiteNoise for serving static files
5. **Database**: SQLite won't work well in production, use MySQL

## Troubleshooting

### Common Issues:
1. **500 Error**: Check error logs, usually permissions or missing dependencies
2. **Static files not loading**: Run `collectstatic` and check file permissions
3. **Database connection**: Verify database credentials and host
4. **File uploads failing**: Check upload directory permissions and size limits

### Performance Tips:
1. Enable caching in Django settings
2. Optimize static file serving
3. Use compression for responses
4. Monitor resource usage

## Security Checklist

- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY
- [ ] Proper ALLOWED_HOSTS
- [ ] SSL enabled
- [ ] Secure file permissions
- [ ] Database credentials protected
- [ ] Error pages don't expose sensitive info
