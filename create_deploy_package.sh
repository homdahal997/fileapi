#!/bin/bash

# Create deployment package for InMotion Hosting
# This script creates a zip file with all necessary files for deployment

echo "🚀 Creating InMotion Hosting deployment package..."

# Create deployment directory
DEPLOY_DIR="inmotion_deploy"
ZIP_FILE="django_fileconvert_api.zip"

# Clean up previous deployment
rm -rf $DEPLOY_DIR
rm -f $ZIP_FILE

# Create deployment directory
mkdir $DEPLOY_DIR

echo "📁 Copying essential files..."

# Copy core Django files
cp passenger_wsgi.py $DEPLOY_DIR/
cp manage.py $DEPLOY_DIR/
cp requirements.txt $DEPLOY_DIR/
cp .htaccess $DEPLOY_DIR/

# Copy Django project and apps
cp -r fileconvert_api/ $DEPLOY_DIR/
cp -r conversions/ $DEPLOY_DIR/
cp -r authentication/ $DEPLOY_DIR/
cp -r storage_integrations/ $DEPLOY_DIR/

# Create .env file from template
echo "🔧 Creating production .env file..."
cat > $DEPLOY_DIR/.env << 'EOF'
# Production Environment for InMotion Hosting
DEBUG=False
SECRET_KEY=CHANGE-THIS-TO-A-STRONG-SECRET-KEY-50-CHARACTERS-LONG
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# MySQL Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=cinciw5_fileapi
DB_USER=cinciw5_fileapi
DB_PASSWORD=Bhutan@2025
DB_HOST=localhost
DB_PORT=3306

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# File Upload Settings (100MB max)
FILE_UPLOAD_MAX_MEMORY_SIZE=104857600
DATA_UPLOAD_MAX_MEMORY_SIZE=104857600

# Static and Media Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Security Settings
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-different-from-django-secret
EOF

# Copy deployment scripts (optional)
cp deploy_inmotion.sh $DEPLOY_DIR/ 2>/dev/null || echo "deploy_inmotion.sh not found, skipping..."

# Copy documentation
mkdir $DEPLOY_DIR/docs
cp INMOTION_DEPLOYMENT.md $DEPLOY_DIR/docs/ 2>/dev/null || echo "INMOTION_DEPLOYMENT.md not found, skipping..."
cp QUICK_SETUP_VALUES.md $DEPLOY_DIR/docs/ 2>/dev/null || echo "QUICK_SETUP_VALUES.md not found, skipping..."
cp UPLOAD_GUIDE.md $DEPLOY_DIR/docs/ 2>/dev/null || echo "UPLOAD_GUIDE.md not found, skipping..."

# Clean up Python cache files
echo "🧹 Cleaning up cache files..."
find $DEPLOY_DIR -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find $DEPLOY_DIR -name "*.pyc" -delete 2>/dev/null || true

# Create README for deployment
cat > $DEPLOY_DIR/README_DEPLOYMENT.txt << 'EOF'
Django File Converter API - InMotion Hosting Deployment Package
================================================================

BEFORE UPLOADING:
1. Edit .env file and update:
   - SECRET_KEY (generate 50-character random string)
   - ALLOWED_HOSTS (replace with your actual domain)
   - CORS_ALLOWED_ORIGINS (replace with your actual domain)

UPLOAD INSTRUCTIONS:
1. Extract this zip file
2. Upload all contents to /home/cinciw5/public_html/
3. SSH into your server and run:
   cd /home/cinciw5/public_html/
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser

INMOTION PYTHON APP CONFIGURATION:
- Python Version: 3.9 (or highest available)
- Application Root: /home/cinciw5/public_html/
- Application URL: https://yourdomain.com/
- Application Startup File: passenger_wsgi.py
- Application Entry Point: application
- Passenger Log File: /home/cinciw5/logs/passenger.log

TEST URLS AFTER DEPLOYMENT:
- Simple Interface: https://yourdomain.com/simple/
- Admin Panel: https://yourdomain.com/admin/
- API Documentation: https://yourdomain.com/swagger/

Your PDF to TXT conversion functionality will be available immediately!
EOF

# Create the zip file
echo "📦 Creating zip file..."
cd $DEPLOY_DIR
zip -r ../$ZIP_FILE . -x "*.DS_Store" "*.git*" "node_modules/*" "venv/*" ".venv/*" "*.sqlite3"
cd ..

# Clean up deployment directory
rm -rf $DEPLOY_DIR

echo ""
echo "✅ Deployment package created successfully!"
echo ""
echo "📦 File: $ZIP_FILE"
echo "📊 Size: $(du -h $ZIP_FILE | cut -f1)"
echo ""
echo "🚀 Upload Instructions:"
echo "1. Upload $ZIP_FILE to your InMotion hosting"
echo "2. Extract in /home/cinciw5/public_html/"
echo "3. Edit .env file with your domain and secret key"
echo "4. Configure Python app in cPanel"
echo "5. Run deployment commands via SSH"
echo ""
echo "📋 See README_DEPLOYMENT.txt in the zip for detailed instructions"
echo ""
echo "🎉 Your Django file conversion API is ready for deployment!"
