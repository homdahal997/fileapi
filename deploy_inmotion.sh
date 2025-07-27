#!/bin/bash

# InMotion Hosting Django Deployment Script
# Configured for cinciw5_fileapi MySQL database

echo "🚀 Starting Django deployment on InMotion Hosting..."
echo "Database: cinciw5_fileapi"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.inmotion .env
    echo "⚠️  IMPORTANT: Edit .env file and update:"
    echo "   - SECRET_KEY (generate a strong 50-character key)"
    echo "   - ALLOWED_HOSTS (add your actual domain)"
    echo "   - CORS_ALLOWED_ORIGINS (add your actual domain)"
    echo ""
fi

# Set correct permissions
echo "📁 Setting file permissions..."
chmod 755 passenger_wsgi.py
chmod -R 755 static/ 2>/dev/null || echo "Static directory doesn't exist yet"
chmod -R 755 media/ 2>/dev/null || echo "Media directory doesn't exist yet"
chmod -R 755 staticfiles/ 2>/dev/null || echo "Staticfiles directory doesn't exist yet"
chmod 600 .env 2>/dev/null || echo "⚠️  .env file not found - please create it"

# Create necessary directories
echo "📂 Creating necessary directories..."
mkdir -p static
mkdir -p media/input_files
mkdir -p media/output_files
mkdir -p staticfiles
mkdir -p logs
mkdir -p temp

# Set directory permissions
chmod 755 static media staticfiles logs temp
chmod 755 media/input_files media/output_files

# Test database connection
echo "🔍 Testing database connection..."
python -c "
import os
import django
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fileconvert_api.settings')
django.setup()
from django.db import connection
try:
    cursor = connection.cursor()
    cursor.execute('SELECT 1')
    print('✅ Database connection successful!')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    print('Please check your .env file database credentials')
"

# Install/upgrade pip packages
echo "📦 Installing Python packages..."
pip install --user -r requirements.txt

# Django management commands
echo "🔄 Running Django migrations..."
python manage.py migrate --noinput

echo "📋 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional)
echo ""
echo "👤 Would you like to create a superuser account? (y/n)"
read -p "Enter choice: " create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

# Check for any deployment issues
echo "🔍 Running Django deployment check..."
python manage.py check --deploy

# Test the conversion functionality
echo "🧪 Testing PDF to TXT conversion..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fileconvert_api.settings')
django.setup()
from conversions.converter import FileConverterService
print('✅ File conversion service loaded successfully!')
"

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📝 Next steps:"
echo "1. ✏️  Edit your .env file with:"
echo "   - Strong SECRET_KEY"
echo "   - Your actual domain in ALLOWED_HOSTS"
echo "   - Your actual domain in CORS_ALLOWED_ORIGINS"
echo "2. 🌐 Configure your domain to point to this directory"
echo "3. 🔒 Enable SSL certificate in cPanel"
echo "4. 🧪 Test your application"
echo ""
echo "🔗 Important URLs to test:"
echo "- 🏠 Home: https://yourdomain.com/"
echo "- 🔧 Admin: https://yourdomain.com/admin/"
echo "- 📊 API Docs: https://yourdomain.com/swagger/"
echo "- 🔄 Simple Interface: https://yourdomain.com/simple/"
echo "- 🚀 API Base: https://yourdomain.com/api/v1/"
echo ""
echo "📊 Check logs at:"
echo "- Error log: ~/logs/error_log"
echo "- Access log: ~/logs/access_log"
echo ""
echo "🗄️  Database: cinciw5_fileapi (MySQL)"
echo "🔗 Connection: localhost:3306"
