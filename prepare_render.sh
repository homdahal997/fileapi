#!/bin/bash

# Render.com Deployment Preparation Script

echo "🚀 Preparing Django project for Render.com deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    echo "# Django File Converter API" > README.md
    
    # Create .gitignore
    cat > .gitignore << 'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Environment variables
.env
.env.local
.env.production
.env.render

# Static files
/staticfiles/
/static/

# Media files
/media/

# Virtual environment
venv/
.venv/
env/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Node modules (if any)
node_modules/
EOF

    echo "✅ Git repository initialized"
fi

# Make build.sh executable
chmod +x build.sh

# Check if dependencies are in requirements.txt
echo "📦 Checking requirements.txt..."
if grep -q "gunicorn" requirements.txt && grep -q "dj-database-url" requirements.txt; then
    echo "✅ Requirements.txt is ready for Render.com"
else
    echo "⚠️  Please check requirements.txt - make sure it includes gunicorn and dj-database-url"
fi

# Stage all files for commit
git add .
git status

echo ""
echo "🎯 Next Steps for Render.com Deployment:"
echo ""
echo "1. 📝 Commit your changes:"
echo "   git commit -m 'Prepare for Render.com deployment'"
echo ""
echo "2. 📤 Push to GitHub:"
echo "   git remote add origin https://github.com/yourusername/your-repo.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 🌐 Deploy on Render.com:"
echo "   - Go to https://render.com"
echo "   - Sign up with GitHub"
echo "   - Click 'New +' → 'Web Service'"
echo "   - Connect your GitHub repository"
echo ""
echo "4. ⚙️  Configure Web Service:"
echo "   Name: django-fileconvert-api"
echo "   Runtime: Python 3"
echo "   Build Command: ./build.sh"
echo "   Start Command: gunicorn fileconvert_api.wsgi:application"
echo ""
echo "5. 🗄️  Add PostgreSQL Database:"
echo "   - Click 'New +' → 'PostgreSQL'"
echo "   - Name: fileconvert-db"
echo ""
echo "6. 🔧 Set Environment Variables:"
echo "   Copy values from .env.render to Render dashboard"
echo ""
echo "7. 🧪 Test Your Deployment:"
echo "   https://your-app-name.onrender.com/simple/"
echo ""
echo "✨ Your Django file conversion API will be live on Render.com!"
echo "🔄 PDF to TXT conversion will work immediately!"
