# MySQL Configuration Guide for Travel Lykk

## For Windows (using XAMPP or standalone MySQL):

1. Download and install MySQL from https://dev.mysql.com/downloads/mysql/
   OR install XAMPP from https://www.apachefriends.org/

2. Start MySQL service

3. Create database:
   ```sql
   CREATE DATABASE travel_booking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'travel_user'@'localhost' IDENTIFIED BY 'travel_password123';
   GRANT ALL PRIVILEGES ON travel_booking_db.* TO 'travel_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Update settings.py:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'travel_booking_db',
           'USER': 'travel_user',
           'PASSWORD': 'travel_password123',
           'HOST': 'localhost',
           'PORT': '3306',
           'OPTIONS': {
               'charset': 'utf8mb4',
           },
       }
   }
   ```

5. Install MySQL client:
   ```bash
   pip install mysqlclient
   ```

6. Run migrations:
   ```bash
   python manage.py migrate
   python manage.py create_sample_data
   ```

## For Production (AWS RDS):

1. Create RDS MySQL instance in AWS Console
2. Note the endpoint, username, and password
3. Update settings.py with RDS credentials
4. Update security groups to allow connections
5. Run migrations

## For Development:
- SQLite is used by default (no additional setup needed)
- Database file: db.sqlite3
