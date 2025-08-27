# Travel Lykk

Django travel booking application.

## Setup

```bash
git clone https://github.com/ukg2005/travel-lykk.git
cd travel-lykk
pip install -r requirements.txt
python manage.py migrate
python manage.py create_sample_data
python manage.py runserver
```

## Features

- User registration and login
- Search and book travel options (flights, trains, buses)
- Booking management
- Admin interface

## Tech Stack

- Django 4.2
- SQLite
- Bootstrap 5
- Python 3.8+

## Admin

Create superuser: `python manage.py createsuperuser`
Access admin at: `/admin/`
