# 🚀 InMotion Python App Quick Setup

## Copy-Paste Configuration Values

### **Main Domain Setup**
```
Python Version: 3.9 (or highest available)
Application Root: /home/cinciw5/public_html/
Application URL: https://yourdomain.com/
Application Startup File: passenger_wsgi.py
Application Entry Point: application
Passenger Log File: /home/cinciw5/logs/passenger.log
```

### **Subdomain Setup (api.yourdomain.com)**
```
Python Version: 3.9 (or highest available)
Application Root: /home/cinciw5/public_html/api/
Application URL: https://api.yourdomain.com/
Application Startup File: passenger_wsgi.py
Application Entry Point: application
Passenger Log File: /home/cinciw5/logs/passenger.log
```

## 📝 Environment Variables (.env file)
```bash
DEBUG=False
SECRET_KEY=generate-a-50-character-random-string-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.mysql
DB_NAME=cinciw5_fileapi
DB_USER=cinciw5_fileapi
DB_PASSWORD=Bhutan@2025
DB_HOST=localhost
DB_PORT=3306
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 🔧 Post-Setup Commands
```bash
# SSH into your server and run:
cd /home/cinciw5/public_html/
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## ✅ Test URLs
- Home: https://yourdomain.com/
- Admin: https://yourdomain.com/admin/
- Simple Interface: https://yourdomain.com/simple/
- API Docs: https://yourdomain.com/swagger/

## 📊 Log Locations
- Passenger Log: /home/cinciw5/logs/passenger.log
- Error Log: /home/cinciw5/logs/error_log
- Access Log: /home/cinciw5/logs/access_log
