#!/bin/bash

# InMotion Hosting Django Deployment Script
# Run this script on your InMotion server after uploading files

echo "Starting Django deployment on InMotion Hosting..."

# Set correct permissions
echo "Setting file permissions..."
chmod 755 passenger_wsgi.py
chmod -R 755 static/ 2>/dev/null || echo "Static directory doesn't exist yet"
chmod -R 755 media/ 2>/dev/null || echo "Media directory doesn't exist yet"
chmod -R 755 staticfiles/ 2>/dev/null || echo "Staticfiles directory doesn't exist yet"
chmod 600 .env 2>/dev/null || echo ".env file not found - please create it from .env.production"

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p static
mkdir -p media/input_files
mkdir -p media/output_files
mkdir -p staticfiles
mkdir -p logs
mkdir -p temp

# Set directory permissions
chmod 755 static media staticfiles logs temp
chmod 755 media/input_files media/output_files

# Install/upgrade pip packages
echo "Installing Python packages..."
pip install --user -r requirements.txt

# Django management commands
echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional - will prompt for details)
echo "Would you like to create a superuser? (y/n)"
read -p "" create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

# Check for any issues
echo "Running Django check..."
python manage.py check --deploy

echo ""
echo "Deployment completed!"
echo ""
echo "Next steps:"
echo "1. Update your .env file with production settings"
echo "2. Configure your domain to point to this directory"
echo "3. Enable SSL certificate in cPanel"
echo "4. Test your application at your domain"
echo ""
echo "Important URLs:"
echo "- Admin: https://yourdomain.com/admin/"
echo "- API Documentation: https://yourdomain.com/swagger/"
echo "- Simple Interface: https://yourdomain.com/simple/"
echo "- API Base: https://yourdomain.com/api/v1/"
echo ""
echo "Check logs at: ~/logs/error_log and ~/logs/access_log"
