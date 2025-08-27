# PythonAnywhere Deployment Guide

## Step 1: Upload Code
1. Create a new web app on PythonAnywhere
2. Upload your code to `/home/yourusername/travel-lykk/`

## Step 2: Virtual Environment
```bash
cd /home/yourusername/travel-lykk
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 3: WSGI Configuration
Update `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

# Add your project directory to sys.path
path = '/home/yourusername/travel-lykk'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'travel_booking.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 4: Static Files
```bash
python manage.py collectstatic --noinput
```

## Step 5: Database Migration
```bash
python manage.py migrate
python manage.py create_sample_data
python manage.py createsuperuser
```

## Step 6: Web App Configuration
- Source code: `/home/yourusername/travel-lykk/`
- Working directory: `/home/yourusername/travel-lykk/`
- WSGI configuration file: `/var/www/yourusername_pythonanywhere_com_wsgi.py`
- Python version: 3.10
- Virtualenv: `/home/yourusername/travel-lykk/venv/`

## Step 7: Static Files Mapping
- URL: `/static/`
- Directory: `/home/yourusername/travel-lykk/staticfiles/`

## Environment Variables (if needed)
Set in the Files tab or add to WSGI file:
```python
os.environ['DJANGO_SECRET_KEY'] = 'your-secret-key-here'
os.environ['DJANGO_DEBUG'] = 'False'
```
