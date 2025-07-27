# 📁 Files to Upload to InMotion Hosting

## Essential Files for Deployment

### **Core Django Files** (Required)
```
✅ passenger_wsgi.py           # WSGI entry point for InMotion
✅ manage.py                   # Django management commands
✅ requirements.txt            # Python dependencies
✅ .htaccess                   # Apache configuration
```

### **Django Project Structure** (Required)
```
✅ fileconvert_api/            # Main Django project folder
   ├── __init__.py
   ├── settings.py
   ├── urls.py
   ├── wsgi.py
   └── asgi.py

✅ conversions/                # Django app folder
   ├── __init__.py
   ├── admin.py
   ├── apps.py
   ├── models.py
   ├── views.py
   ├── urls.py
   ├── converter.py            # File conversion logic
   ├── serializers.py
   ├── simple_views.py         # Simple HTML interface
   ├── health_views.py
   ├── health_urls.py
   ├── migrations/
   └── templates/

✅ authentication/             # Django app folder
   ├── __init__.py
   ├── admin.py
   ├── apps.py
   ├── models.py
   ├── views.py
   ├── urls.py
   └── migrations/

✅ storage_integrations/       # Django app folder
   ├── __init__.py
   ├── admin.py
   ├── apps.py
   ├── models.py
   ├── views.py
   ├── urls.py
   └── migrations/
```

### **Configuration Files** (Create from templates)
```
🔧 .env                       # Create from .env.production
```

### **Optional Helper Files**
```
📝 deploy_inmotion.sh         # Deployment script
📝 DEPLOYMENT_GUIDE.md        # Documentation
📝 INMOTION_DEPLOYMENT.md     # Deployment checklist
📝 QUICK_SETUP_VALUES.md      # Quick reference
```

### **DO NOT Upload These Files:**
```
❌ .env.production            # Template file only
❌ .env.inmotion             # Template file only
❌ db.sqlite3                # Local database
❌ __pycache__/              # Python cache
❌ .git/                     # Git repository
❌ venv/                     # Virtual environment
❌ .venv/                    # Virtual environment
❌ node_modules/             # If you have React frontend
```

## Step-by-Step Upload Process

### **1. Create .env File First**
Before uploading, create your production .env file:
```bash
# Copy the template
cp .env.production .env

# Edit .env and update:
DEBUG=False
SECRET_KEY=your-generated-50-character-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### **2. Upload Methods**

**Option A: cPanel File Manager**
1. Login to cPanel
2. Open File Manager
3. Navigate to `/public_html/`
4. Upload files/folders listed above

**Option B: FTP/SFTP**
1. Use FileZilla or similar FTP client
2. Connect to your InMotion server
3. Upload to `/public_html/` directory

**Option C: Git Clone (if using Git)**
```bash
# SSH into your server
cd /home/cinciw5/public_html/
git clone your-repository-url .
```

### **3. Directory Structure on Server**
After upload, your server should look like:
```
/home/cinciw5/public_html/
├── passenger_wsgi.py          # ✅ WSGI entry point
├── manage.py                  # ✅ Django management
├── requirements.txt           # ✅ Dependencies
├── .env                      # ✅ Your environment config
├── .htaccess                 # ✅ Apache config
├── fileconvert_api/          # ✅ Django project
├── conversions/              # ✅ Main app
├── authentication/           # ✅ Auth app
└── storage_integrations/     # ✅ Storage app
```

### **4. Post-Upload Commands**
SSH into your server and run:
```bash
cd /home/cinciw5/public_html/
chmod +x deploy_inmotion.sh
./deploy_inmotion.sh
```

## Quick Upload Checklist

- [ ] ✅ Upload `passenger_wsgi.py`
- [ ] ✅ Upload `manage.py`
- [ ] ✅ Upload `requirements.txt`
- [ ] ✅ Upload `.htaccess`
- [ ] ✅ Upload `fileconvert_api/` folder
- [ ] ✅ Upload `conversions/` folder
- [ ] ✅ Upload `authentication/` folder
- [ ] ✅ Upload `storage_integrations/` folder
- [ ] ✅ Create `.env` from template
- [ ] ✅ Upload deployment scripts (optional)

## Essential Files Summary

**Minimum files needed for your Django app to work:**
1. `passenger_wsgi.py` - Entry point
2. `manage.py` - Django commands
3. `requirements.txt` - Dependencies
4. `fileconvert_api/` - Django project
5. `conversions/` - Main app with PDF conversion
6. `.env` - Configuration
7. `.htaccess` - Apache config

Your PDF to TXT conversion functionality is in the `conversions/` app, so make sure that folder is uploaded completely! 🚀
