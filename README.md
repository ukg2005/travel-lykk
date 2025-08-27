# Travel Lykk - Travel Booking Application

A comprehensive travel booking web application built with Django that allows users to search, book, and manage travel reservations for flights, trains, and buses.

## 🚀 Live Demo

**Deployed Application**: [Coming Soon - Will be deployed to PythonAnywhere]
**GitHub Repository**: [Your GitHub URL will go here]

## Features

### User Management
- User registration and authentication
- Profile management with personal information
- Password change functionality
- Automatic user profile creation

### Travel Options
- Browse available travel options (flights, trains, buses)
- Advanced search and filtering capabilities
- Filter by travel type, source, destination, and date
- Pagination for better user experience
- Real-time availability tracking

### Booking System
- Secure booking process with validation
- Multiple passenger support
- Booking confirmation with unique booking IDs
- Contact information collection
- Seat availability validation

### Booking Management
- View all user bookings
- Detailed booking information
- Cancel bookings (with 24-hour policy)
- Booking status tracking (Confirmed, Cancelled, Pending)
- Print-friendly booking details

### User Interface
- Responsive design using Bootstrap 5
- Modern and intuitive interface
- Font Awesome icons for better UX
- Mobile-friendly layout
- Professional color scheme

## Technology Stack

- **Backend**: Django 5.2.5
- **Database**: SQLite (development) / MySQL (production)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6
- **Authentication**: Django's built-in authentication system

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Git
- MySQL (for production)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd travel-lykk
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - For development, SQLite is used by default
   - For production with MySQL, update settings.py:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'travel_booking_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Create sample data**
   ```bash
   python manage.py create_sample_data
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## MySQL Configuration

1. **Install MySQL**
   - Download and install MySQL from official website
   - Create a database named `travel_booking_db`

2. **Install MySQL client**
   ```bash
   pip install mysqlclient
   ```

3. **Update settings.py**
   - Uncomment the MySQL configuration section
   - Update database credentials

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

## Project Structure

```
travel_booking/
├── bookings/
│   ├── management/
│   │   └── commands/
│   │       └── create_sample_data.py
│   ├── migrations/
│   ├── templatetags/
│   │   └── booking_extras.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── bookings/
│   │   ├── booking_detail.html
│   │   ├── book_travel.html
│   │   ├── cancel_booking.html
│   │   ├── home.html
│   │   ├── my_bookings.html
│   │   ├── profile.html
│   │   └── travel_options.html
│   ├── registration/
│   │   ├── login.html
│   │   ├── password_change.html
│   │   ├── password_change_done.html
│   │   └── register.html
│   └── base.html
├── travel_booking/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

## Models

### TravelOption
- `travel_id`: Unique identifier
- `travel_type`: Flight, Train, or Bus
- `source`: Departure location
- `destination`: Arrival location
- `departure_date/time`: Departure schedule
- `arrival_date/time`: Arrival schedule
- `price`: Cost per seat
- `available_seats`: Current availability
- `total_seats`: Maximum capacity

### UserProfile
- `user`: One-to-one relation with Django User
- `phone_number`: Contact number
- `date_of_birth`: User's birth date
- `address`: Home address

### Booking
- `booking_id`: Unique booking identifier
- `user`: Foreign key to User
- `travel_option`: Foreign key to TravelOption
- `number_of_seats`: Seats booked
- `total_price`: Total cost
- `passenger_names`: List of passengers
- `contact_email/phone`: Contact information
- `status`: Confirmed, Cancelled, or Pending

## Key Features Implementation

### Search and Filtering
- Advanced search form with multiple criteria
- Dynamic filtering without page reload
- Pagination for large result sets
- Real-time availability checking

### Booking Process
1. User selects travel option
2. Fills booking form with passenger details
3. System validates availability
4. Creates booking and updates seat count
5. Generates unique booking ID
6. Sends confirmation

### Cancellation Policy
- Bookings can be cancelled up to 24 hours before departure
- Automatic seat restoration upon cancellation
- Status tracking for all bookings

### Security Features
- CSRF protection on all forms
- User authentication for sensitive operations
- Input validation and sanitization
- SQL injection prevention through ORM

## Testing

Run the test suite:
```bash
python manage.py test bookings
```

The test suite includes:
- Model validation tests
- Form validation tests
- View functionality tests
- User authentication tests

## Deployment

### PythonAnywhere Deployment

1. **Upload code to PythonAnywhere**
2. **Set up virtual environment**
3. **Install dependencies**
4. **Configure database**
5. **Update settings for production**
6. **Run migrations**
7. **Configure web app**

### AWS Deployment

1. **Set up EC2 instance**
2. **Install dependencies**
3. **Configure MySQL on RDS**
4. **Set up static files with S3**
5. **Configure security groups**
6. **Deploy with Gunicorn and Nginx**

## Environment Variables

For production deployment, set these environment variables:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated allowed hosts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team or create an issue in the repository.

## Future Enhancements

- Payment gateway integration
- Email notifications
- SMS alerts
- Multi-language support
- Advanced reporting
- API endpoints
- Mobile app integration
- Real-time seat maps
- Loyalty program
- Social media integration
