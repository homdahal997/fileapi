"""
App configuration to auto-create superuser on startup.
This is useful for Render.com free tier users without shell access.
"""
from django.apps import AppConfig
import os


class ConversionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conversions'

    def ready(self):
        """
        Auto-create superuser when app is ready (only in production).
        """
        # Only run in production (Render.com)
        if os.environ.get('RENDER') == 'True':
            try:
                from django.contrib.auth import get_user_model
                from django.db import connection
                from django.db.utils import OperationalError
                
                # Check if database is ready
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                
                User = get_user_model()
                
                # Check if any superuser exists
                if not User.objects.filter(is_superuser=True).exists():
                    # Create superuser from environment variables
                    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
                    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@fileconvert.com')
                    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'AdminFileConvert2025!')
                    
                    User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )
                    print(f"✅ Superuser '{username}' created automatically!")
                    print(f"🔑 Login at /admin/ with username: {username}")
                    print("⚠️  Please change the default password after first login!")
                else:
                    print("ℹ️  Superuser already exists, skipping creation.")
                    
            except (OperationalError, Exception) as e:
                # Database might not be ready yet, that's okay
                print(f"⚠️  Could not auto-create superuser: {e}")
                pass
