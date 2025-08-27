from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    'ukg2005.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
