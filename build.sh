#!/usr/bin/env bash
# Build script for Render.com deployment
# exit on error
set -o errexit

echo "🚀 Starting Render.com build process..."

# Upgrade pip first
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser automatically (for free tier users without shell access)
echo "👤 Creating superuser automatically..."
python manage.py create_superuser_env || echo "Superuser creation skipped (may already exist)"

echo "✅ Build completed successfully!"
