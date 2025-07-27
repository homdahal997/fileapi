# Alternative Render.com Configuration (Without build.sh)

## 🚀 **Option 1: Direct Build Commands**

Instead of using `build.sh`, use these direct commands in Render.com:

### **Web Service Configuration:**
```
Name: django-fileconvert-api
Runtime: Python 3
Build Command: pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
Start Command: gunicorn fileconvert_api.wsgi:application
```

### **Environment Variables:**
```
PYTHON_VERSION=3.11.0
DEBUG=False
SECRET_KEY=your-50-character-secret-key-here
RENDER=True
WEB_CONCURRENCY=4
```

## 🚀 **Option 2: Using render.yaml (Recommended)**

Create a `render.yaml` file in your project root:

```yaml
services:
  - type: web
    name: django-fileconvert-api
    env: python
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate"
    startCommand: "gunicorn fileconvert_api.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DEBUG
        value: False
      - key: RENDER
        value: True
      - key: WEB_CONCURRENCY
        value: 4
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: fileconvert-db
          property: connectionString

databases:
  - name: fileconvert-db
    databaseName: fileconvert_api
    user: fileapi_user
```

## 🚀 **Option 3: Simplified Build Script**

If you want to keep using build.sh, ensure it's executable:

1. **In Git Bash or WSL:**
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build.sh executable"
   ```

2. **Alternative: Rename to build_render.sh**
   - Rename `build.sh` to `build_render.sh`
   - Use Build Command: `bash build_render.sh`

## 🎯 **Recommended Solution: Use Direct Commands**

For simplicity, I recommend using **Option 1** with direct build commands:

```
Build Command: pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
Start Command: gunicorn fileconvert_api.wsgi:application
```

This eliminates the need for a separate build script and is more reliable on Render.com.

## 🔧 **Complete Setup Steps:**

1. **Push your code to GitHub**
2. **Create Web Service on Render.com**
3. **Use direct build commands above**
4. **Add PostgreSQL database**
5. **Set environment variables**
6. **Deploy!**

Your Django file conversion API will be live! 🎉
