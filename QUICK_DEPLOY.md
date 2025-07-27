# Quick InMotion Hosting Deployment

## Step-by-Step Deployment

### 1. **Prepare Your Files**
```bash
# Create production environment file
cp .env.production .env

# Edit .env with your actual values:
# - Your domain name
# - Database credentials
# - Secret key
```

### 2. **Upload to InMotion**
Via cPanel File Manager or FTP, upload all files to your domain directory:
- If main domain: `/public_html/`
- If subdomain: `/public_html/subdomain_name/`

### 3. **Database Setup**
In cPanel → MySQL Databases:
1. Create database: `your_database_name`
2. Create user: `your_db_username`
3. Add user to database with all privileges

### 4. **Run Deployment Script**
SSH into your server:
```bash
cd /path/to/your/domain
chmod +x deploy.sh
./deploy.sh
```

### 5. **Configure Domain**
In cPanel → Subdomains (if using subdomain like api.yourdomain.com):
1. Create subdomain
2. Point to your Django directory

### 6. **Enable SSL**
In cPanel → SSL/TLS:
1. Enable Let's Encrypt SSL
2. Force HTTPS redirect

### 7. **Test Your Deployment**
Visit these URLs:
- `https://yourdomain.com/simple/` (Simple conversion interface)
- `https://yourdomain.com/admin/` (Django admin)
- `https://yourdomain.com/swagger/` (API documentation)

## Important Files Created:

1. **`.env.production`** - Template for production environment variables
2. **`passenger_wsgi.py`** - WSGI configuration for InMotion Passenger
3. **`.htaccess`** - Apache configuration with security headers
4. **`deploy.sh`** - Automated deployment script
5. **`DEPLOYMENT_GUIDE.md`** - Detailed deployment instructions

## Quick Troubleshooting:

**500 Error?**
- Check error logs: `~/logs/error_log`
- Verify `.env` file has correct database credentials
- Ensure all dependencies are installed

**Static files not loading?**
- Run: `python manage.py collectstatic --noinput`
- Check file permissions: `chmod -R 755 static/`

**Database connection failed?**
- Verify database name, username, password in .env
- Check MySQL database exists in cPanel

**File uploads not working?**
- Check media directory permissions: `chmod -R 755 media/`
- Verify upload size limits in .htaccess

## Performance Tips:
1. Use MySQL instead of SQLite for production
2. Enable gzip compression (already in .htaccess)
3. Set up browser caching (already in .htaccess)
4. Monitor resource usage in cPanel

Your Django file conversion API will be live and ready to use! 🚀
