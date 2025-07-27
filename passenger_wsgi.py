#!/usr/bin/env python
"""
WSGI config for InMotion Hosting deployment.
This file is used by InMotion's Passenger WSGI.
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Add your project directory to the Python path
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'fileconvert_api'))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fileconvert_api.settings')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()
