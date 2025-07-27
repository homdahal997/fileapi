# InMotion Hosting Python Application Configuration

## Python Application Setup Information

### 1. **Python Version**
```
3.8 or higher (recommended: 3.9 or 3.10)
```
*Select the highest Python version available in your InMotion cPanel*

### 2. **Application Root**
```
/home/cinciw5/public_html/
```
*If using a subdomain (e.g., api.yourdomain.com):*
```
/home/cinciw5/public_html/api/
```

### 3. **Application URL**
```
https://yourdomain.com/
```
*If using a subdomain:*
```
https://api.yourdomain.com/
```

### 4. **Application Startup File**
```
passenger_wsgi.py
```

### 5. **Application Entry Point**
```
application
```
*This refers to the WSGI callable object in passenger_wsgi.py*

### 6. **Passenger Log File**
```
/home/cinciw5/logs/passenger.log
```

## Complete Configuration Example

**For Main Domain Setup:**
- Python Version: `3.9` (or highest available)
- Application Root: `/home/cinciw5/public_html/`
- Application URL: `https://yourdomain.com/`
- Application Startup File: `passenger_wsgi.py`
- Application Entry Point: `application`
- Passenger Log File: `/home/cinciw5/logs/passenger.log`

**For Subdomain Setup (api.yourdomain.com):**
- Python Version: `3.9` (or highest available)
- Application Root: `/home/cinciw5/public_html/api/`
- Application URL: `https://api.yourdomain.com/`
- Application Startup File: `passenger_wsgi.py`
- Application Entry Point: `application`
- Passenger Log File: `/home/cinciw5/logs/passenger.log`

## Step-by-Step Setup in cPanel

### 1. **Access Python App Manager**
- Login to cPanel
- Find "Python App" or "Setup Python App"
- Click "Create Application"

### 2. **Fill Configuration Form**
```
Python Version: [Select 3.8+ from dropdown]
Application Root: /home/cinciw5/public_html/
Application URL: https://yourdomain.com/
Application Startup File: passenger_wsgi.py
Application Entry Point: application
Passenger Log File: /home/cinciw5/logs/passenger.log
```

### 3. **After Creating Application**
- Upload your Django files to the Application Root directory
- Install requirements: `pip install -r requirements.txt`
- Run deployment script: `./deploy_inmotion.sh`

## Important Notes

### **File Structure Should Look Like:**
```
/home/cinciw5/public_html/
├── passenger_wsgi.py          # WSGI entry point
├── manage.py                  # Django management
├── requirements.txt           # Dependencies
├── .env                      # Environment variables
├── .htaccess                 # Apache configuration
├── fileconvert_api/          # Django project
├── conversions/              # Django app
├── static/                   # Static files
├── media/                    # Media files
└── logs/                     # Log files
```

### **Environment Variables**
Make sure your `.env` file contains:
```bash
DEBUG=False
SECRET_KEY=your-50-character-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=cinciw5_fileapi
DB_USER=cinciw5_fileapi
DB_PASSWORD=Bhutan@2025
```

### **Testing Your Setup**
After configuration, test these URLs:
- Main site: `https://yourdomain.com/`
- Admin: `https://yourdomain.com/admin/`
- Simple interface: `https://yourdomain.com/simple/`
- API docs: `https://yourdomain.com/swagger/`

## Troubleshooting

### **If Application Doesn't Start:**
1. Check passenger log: `/home/cinciw5/logs/passenger.log`
2. Verify Python version compatibility
3. Ensure all dependencies are installed
4. Check file permissions (755 for directories, 644 for files)

### **Common Issues:**
- **Module not found**: Run `pip install -r requirements.txt`
- **Permission denied**: Check file permissions
- **Database connection**: Verify database credentials in .env
- **Static files**: Run `python manage.py collectstatic`

Your Django file conversion API will be live once configured! 🚀
