@echo off
echo 🚀 Creating InMotion Hosting deployment package (Backend Only)...

REM Set variables
set DEPLOY_DIR=inmotion_deploy_backend
set ZIP_FILE=django_api_backend.zip

REM Clean up previous deployment
if exist %DEPLOY_DIR% rmdir /s /q %DEPLOY_DIR%
if exist %ZIP_FILE% del %ZIP_FILE%

REM Create deployment directory
mkdir %DEPLOY_DIR%

echo 📁 Copying Django backend files only...

REM Copy core Django files
copy passenger_wsgi.py %DEPLOY_DIR%\
copy manage.py %DEPLOY_DIR%\
copy requirements.txt %DEPLOY_DIR%\
copy .htaccess %DEPLOY_DIR%\

REM Copy Django project (excluding frontapi folder)
mkdir %DEPLOY_DIR%\fileconvert_api
copy fileconvert_api\*.py %DEPLOY_DIR%\fileconvert_api\
if exist fileconvert_api\__pycache__ xcopy fileconvert_api\__pycache__ %DEPLOY_DIR%\fileconvert_api\__pycache__\ /e /i /q

REM Copy Django apps
xcopy conversions %DEPLOY_DIR%\conversions\ /e /i /q
xcopy authentication %DEPLOY_DIR%\authentication\ /e /i /q
xcopy storage_integrations %DEPLOY_DIR%\storage_integrations\ /e /i /q

echo 🔧 Creating production .env file...

REM Create .env file
(
echo # Production Environment for InMotion Hosting
echo DEBUG=False
echo SECRET_KEY=CHANGE-THIS-TO-A-STRONG-SECRET-KEY-50-CHARACTERS-LONG
echo ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
echo.
echo # MySQL Database Configuration
echo DB_ENGINE=django.db.backends.mysql
echo DB_NAME=cinciw5_fileapi
echo DB_USER=cinciw5_fileapi
echo DB_PASSWORD=Bhutan@2025
echo DB_HOST=localhost
echo DB_PORT=3306
echo.
echo # CORS Configuration
echo CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
echo.
echo # File Upload Settings ^(100MB max^)
echo FILE_UPLOAD_MAX_MEMORY_SIZE=104857600
echo DATA_UPLOAD_MAX_MEMORY_SIZE=104857600
echo.
echo # Static and Media Files
echo STATIC_URL=/static/
echo MEDIA_URL=/media/
echo.
echo # Security Settings
echo SECURE_SSL_REDIRECT=True
echo SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
echo SECURE_BROWSER_XSS_FILTER=True
echo SECURE_CONTENT_TYPE_NOSNIFF=True
echo.
echo # JWT Configuration
echo JWT_SECRET_KEY=your-jwt-secret-key-different-from-django-secret
) > %DEPLOY_DIR%\.env

REM Copy deployment scripts if they exist
if exist deploy_inmotion.sh copy deploy_inmotion.sh %DEPLOY_DIR%\

REM Copy documentation
mkdir %DEPLOY_DIR%\docs
if exist INMOTION_DEPLOYMENT.md copy INMOTION_DEPLOYMENT.md %DEPLOY_DIR%\docs\
if exist QUICK_SETUP_VALUES.md copy QUICK_SETUP_VALUES.md %DEPLOY_DIR%\docs\
if exist UPLOAD_GUIDE.md copy UPLOAD_GUIDE.md %DEPLOY_DIR%\docs\

echo 🧹 Cleaning up cache files...
REM Remove Python cache directories
for /d /r %DEPLOY_DIR% %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
REM Remove .pyc files
del /s /q "%DEPLOY_DIR%\*.pyc" 2>nul

echo 📝 Creating deployment README...
(
echo Django File Converter API - InMotion Hosting Deployment Package ^(Backend Only^)
echo =================================================================================
echo.
echo BEFORE UPLOADING:
echo 1. Edit .env file and update:
echo    - SECRET_KEY ^(generate 50-character random string^)
echo    - ALLOWED_HOSTS ^(replace with your actual domain^)
echo    - CORS_ALLOWED_ORIGINS ^(replace with your actual domain^)
echo.
echo UPLOAD INSTRUCTIONS:
echo 1. Extract this zip file
echo 2. Upload all contents to /home/cinciw5/public_html/
echo 3. SSH into your server and run:
echo    cd /home/cinciw5/public_html/
echo    pip install -r requirements.txt
echo    python manage.py migrate
echo    python manage.py collectstatic --noinput
echo    python manage.py createsuperuser
echo.
echo INMOTION PYTHON APP CONFIGURATION:
echo - Python Version: 3.9 ^(or highest available^)
echo - Application Root: /home/cinciw5/public_html/
echo - Application URL: https://yourdomain.com/
echo - Application Startup File: passenger_wsgi.py
echo - Application Entry Point: application
echo - Passenger Log File: /home/cinciw5/logs/passenger.log
echo.
echo TEST URLS AFTER DEPLOYMENT:
echo - Simple Interface: https://yourdomain.com/simple/
echo - Admin Panel: https://yourdomain.com/admin/
echo - API Documentation: https://yourdomain.com/swagger/
echo.
echo PDF to TXT conversion will work immediately!
echo This package contains ONLY the Django backend - no React frontend included.
) > %DEPLOY_DIR%\README_DEPLOYMENT.txt

echo 📦 Creating zip file...
REM Use PowerShell to create zip file (Windows 10/11)
powershell -command "Compress-Archive -Path '%DEPLOY_DIR%\*' -DestinationPath '%ZIP_FILE%' -Force"

REM Clean up deployment directory
rmdir /s /q %DEPLOY_DIR%

echo.
echo ✅ Django Backend deployment package created successfully!
echo.
echo 📦 File: %ZIP_FILE%
for %%A in (%ZIP_FILE%) do echo 📊 Size: %%~zA bytes
echo.
echo 🚀 Upload Instructions:
echo 1. Upload %ZIP_FILE% to your InMotion hosting cPanel File Manager
echo 2. Extract in /home/cinciw5/public_html/
echo 3. Edit .env file with your domain and secret key
echo 4. Configure Python app in cPanel with provided settings
echo 5. Run deployment commands via SSH
echo.
echo 📋 See README_DEPLOYMENT.txt in the zip for detailed instructions
echo.
echo 🎉 Your Django file conversion API backend is ready for deployment!
echo ✅ PDF to TXT conversion functionality included!
pause
