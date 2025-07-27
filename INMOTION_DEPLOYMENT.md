# 🚀 InMotion Hosting Deployment Checklist

## Your Database Configuration ✅
- **Database Name:** `cinciw5_fileapi`
- **Username:** `cinciw5_fileapi`  
- **Password:** `Bhutan@2025`
- **Host:** `localhost`
- **Port:** `3306`

## Pre-Deployment Steps

### 1. **Upload Files to InMotion**
Via cPanel File Manager or FTP, upload all files to:
- Main domain: `/public_html/`
- Subdomain: `/public_html/subdomain_name/`

### 2. **Configure Environment**
```bash
# Copy the InMotion-specific environment file
cp .env.inmotion .env

# Edit .env and update these values:
# SECRET_KEY=your-50-character-secret-key
# ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
# CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 3. **Run Deployment Script**
```bash
chmod +x deploy_inmotion.sh
./deploy_inmotion.sh
```

## Security Checklist ✅

- [ ] Change `SECRET_KEY` in `.env` (generate 50-character random string)
- [ ] Update `ALLOWED_HOSTS` with your actual domain
- [ ] Update `CORS_ALLOWED_ORIGINS` with your actual domain
- [ ] Set `DEBUG=False` (already configured)
- [ ] Enable SSL certificate in cPanel
- [ ] File permissions set correctly (automated in script)

## Testing Your Deployment

### 1. **Basic Functionality**
- [ ] Visit your domain (should show Django welcome or your app)
- [ ] Test admin panel: `https://yourdomain.com/admin/`
- [ ] Test simple interface: `https://yourdomain.com/simple/`

### 2. **File Conversion Testing**
- [ ] Upload a PDF file at `/simple/`
- [ ] Convert PDF to TXT
- [ ] Download converted file
- [ ] Verify file content is correct

### 3. **API Testing**
- [ ] Visit API docs: `https://yourdomain.com/swagger/`
- [ ] Test API endpoints with curl or Postman
- [ ] Verify CORS works for frontend

## Troubleshooting Guide

### **500 Internal Server Error**
```bash
# Check error logs
tail -f ~/logs/error_log

# Common fixes:
chmod 755 passenger_wsgi.py
python manage.py migrate
python manage.py collectstatic --noinput
```

### **Database Connection Issues**
```bash
# Test database connection
python manage.py dbshell

# If fails, verify in .env:
# DB_NAME=cinciw5_fileapi
# DB_USER=cinciw5_fileapi
# DB_PASSWORD=Bhutan@2025
```

### **Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check permissions
chmod -R 755 static/
chmod -R 755 staticfiles/
```

### **File Upload Issues**
```bash
# Check media directory permissions
chmod -R 755 media/

# Verify upload limits in .htaccess
LimitRequestBody 104857600  # 100MB
```

## Performance Optimization

### **Recommended Settings**
- ✅ MySQL database (configured)
- ✅ Static file compression (in .htaccess)
- ✅ Browser caching (in .htaccess)
- ✅ Security headers (in .htaccess)

### **Monitor Resource Usage**
- Check CPU/Memory usage in cPanel
- Monitor database size
- Watch file storage usage

## Success Indicators 🎉

Your deployment is successful when:
- [ ] ✅ Admin panel accessible
- [ ] ✅ Simple interface loads
- [ ] ✅ PDF to TXT conversion works
- [ ] ✅ File download works
- [ ] ✅ No 500 errors in logs
- [ ] ✅ SSL certificate active

## Support

If you encounter issues:
1. **Check error logs:** `~/logs/error_log`
2. **Test database connection:** Run `python manage.py dbshell`
3. **Verify environment:** Ensure `.env` has correct values
4. **Check permissions:** Files should be 755, directories 755, .env should be 600

Your Django file conversion API is ready for production! 🚀
