@echo off
echo 🚀 Preparing Django project for Render.com deployment...

REM Check if git is initialized
if not exist ".git" (
    echo 📝 Initializing Git repository...
    git init
    echo # Django File Converter API > README.md
    
    REM Create .gitignore
    (
    echo # Byte-compiled / optimized / DLL files
    echo __pycache__/
    echo *.py[cod]
    echo *$py.class
    echo.
    echo # Django stuff:
    echo *.log
    echo local_settings.py
    echo db.sqlite3
    echo db.sqlite3-journal
    echo.
    echo # Environment variables
    echo .env
    echo .env.local
    echo .env.production
    echo .env.render
    echo.
    echo # Static files
    echo /staticfiles/
    echo /static/
    echo.
    echo # Media files
    echo /media/
    echo.
    echo # Virtual environment
    echo venv/
    echo .venv/
    echo env/
    echo.
    echo # IDE
    echo .vscode/
    echo .idea/
    echo.
    echo # OS
    echo .DS_Store
    echo Thumbs.db
    echo.
    echo # Node modules ^(if any^)
    echo node_modules/
    ) > .gitignore

    echo ✅ Git repository initialized
)

REM Check requirements.txt
echo 📦 Checking requirements.txt...
findstr /C:"gunicorn" requirements.txt >nul && findstr /C:"dj-database-url" requirements.txt >nul
if %errorlevel%==0 (
    echo ✅ Requirements.txt is ready for Render.com
) else (
    echo ⚠️  Please check requirements.txt - make sure it includes gunicorn and dj-database-url
)

REM Stage files for commit
git add .
git status

echo.
echo 🎯 Next Steps for Render.com Deployment:
echo.
echo 1. 📝 Commit your changes:
echo    git commit -m "Prepare for Render.com deployment"
echo.
echo 2. 📤 Push to GitHub:
echo    git remote add origin https://github.com/yourusername/your-repo.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. 🌐 Deploy on Render.com:
echo    - Go to https://render.com
echo    - Sign up with GitHub
echo    - Click 'New +' → 'Web Service'
echo    - Connect your GitHub repository
echo.
echo 4. ⚙️  Configure Web Service:
echo    Name: django-fileconvert-api
echo    Runtime: Python 3
echo    Build Command: ./build.sh
echo    Start Command: gunicorn fileconvert_api.wsgi:application
echo.
echo 5. 🗄️  Add PostgreSQL Database:
echo    - Click 'New +' → 'PostgreSQL'
echo    - Name: fileconvert-db
echo.
echo 6. 🔧 Set Environment Variables:
echo    Copy values from .env.render to Render dashboard
echo.
echo 7. 🧪 Test Your Deployment:
echo    https://your-app-name.onrender.com/simple/
echo.
echo ✨ Your Django file conversion API will be live on Render.com!
echo 🔄 PDF to TXT conversion will work immediately!
pause
