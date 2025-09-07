# Deployment Guide for ZipGo

## PythonAnywhere Deployment

### 1. Prepare Your Code
```bash
# Generate requirements.txt if needed
pip freeze > requirements.txt

# Ensure all files are ready
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Upload to PythonAnywhere
1. Create account at https://www.pythonanywhere.com/
2. Go to Files tab and upload your project
3. Or clone from GitHub:
   ```bash
   git clone https://github.com/yourusername/zipgo.git
   ```

### 3. Set up Virtual Environment
```bash
cd travel-lykk
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure Database
- For free accounts, use SQLite (already configured)
- For paid accounts, you can use MySQL

### 5. Run Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py create_sample_data
python manage.py collectstatic
```

### 6. Configure Web App
1. Go to Web tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose Manual Configuration
4. Choose Python 3.11
5. Set source code directory: `/home/yourusername/zipgo`
6. Set working directory: `/home/yourusername/zipgo`
7. Edit WSGI file:
   ```python
   import os
   import sys
   
   path = '/home/yourusername/zipgo'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'travel_booking.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

### 7. Static Files
1. Go to Web tab → Static files
2. Add: URL: `/static/` Directory: `/home/yourusername/zipgo/staticfiles/`
3. Add: URL: `/media/` Directory: `/home/yourusername/zipgo/media/`

### 8. Update Settings for Production
```python
# In settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Static files
STATIC_ROOT = '/home/yourusername/zipgo/staticfiles'
```

### 9. Reload and Test
1. Click "Reload" button in Web tab
2. Visit https://yourusername.pythonanywhere.com

---

## AWS Deployment (Advanced)

### 1. Set up EC2 Instance
1. Launch Ubuntu EC2 instance
2. Configure security groups (HTTP, HTTPS, SSH)
3. Connect via SSH

### 2. Install Dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx mysql-server
```

### 3. Set up Application
```bash
git clone https://github.com/yourusername/zipgo.git
cd zipgo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 4. Configure MySQL
```bash
sudo mysql_secure_installation
sudo mysql -u root -p
```
```sql
CREATE DATABASE travel_booking_db;
CREATE USER 'travel_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON travel_booking_db.* TO 'travel_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. Update Settings
```python
# settings.py for production
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'your-ec2-ip']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'travel_booking_db',
        'USER': 'travel_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_ROOT = '/home/ubuntu/zipgo/staticfiles'
```

### 6. Run Migrations and Collect Static
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py create_sample_data
python manage.py collectstatic
```

### 7. Configure Gunicorn
Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/zipgo
ExecStart=/home/ubuntu/zipgo/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/zipgo/travel_booking.sock travel_booking.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 8. Configure Nginx
Create `/etc/nginx/sites-available/zipgo`:
```nginx
server {
    listen 80;
    server_name your-domain.com your-ec2-ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/zipgo;
    }
    location /media/ {
        root /home/ubuntu/zipgo;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/zipgo/travel_booking.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/zipgo /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Start Services
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

### 10. Set up SSL (Optional)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Environment Variables for Production

Create `.env` file:
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
DATABASE_URL=mysql://user:password@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

Install python-decouple:
```bash
pip install python-decouple
```

Update settings.py:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
```

---

## Post-Deployment Checklist

- [ ] Application loads without errors
- [ ] Admin panel accessible (/admin/)
- [ ] User registration works
- [ ] User login/logout works
- [ ] Travel search and filtering works
- [ ] Booking process works
- [ ] Email notifications work (if configured)
- [ ] Static files load correctly
- [ ] Database migrations applied
- [ ] Sample data loaded
- [ ] SSL certificate installed (for production)
- [ ] Backup strategy implemented
- [ ] Monitoring set up

---

## Troubleshooting

### Common Issues:
1. **Static files not loading**: Check STATIC_ROOT and run `collectstatic`
2. **Database connection errors**: Verify database credentials
3. **Permission errors**: Check file permissions and user groups
4. **Import errors**: Ensure all dependencies in requirements.txt
5. **Template not found**: Check TEMPLATES setting in settings.py

### Logs:
- Application logs: Check Gunicorn/uWSGI logs
- Web server logs: Check Nginx/Apache logs
- Django logs: Set up proper logging in settings.py
