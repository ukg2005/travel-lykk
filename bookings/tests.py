from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, time, timedelta
from .models import TravelOption, Booking, UserProfile
from .forms import CustomUserCreationForm, BookingForm


class TravelOptionModelTest(TestCase):
    def setUp(self):
        self.travel_option = TravelOption.objects.create(
            travel_id='FL001',
            travel_type='flight',
            source='New York',
            destination='Los Angeles',
            departure_date=date.today() + timedelta(days=1),
            departure_time=time(10, 0),
            arrival_date=date.today() + timedelta(days=1),
            arrival_time=time(13, 0),
            price=299.99,
            available_seats=50,
            total_seats=100
        )
    
    def test_travel_option_creation(self):
        self.assertEqual(self.travel_option.travel_id, 'FL001')
        self.assertEqual(self.travel_option.travel_type, 'flight')
        self.assertEqual(self.travel_option.source, 'New York')
        self.assertEqual(self.travel_option.destination, 'Los Angeles')
    
    def test_is_available_property(self):
        self.assertTrue(self.travel_option.is_available)
        
        # Test with no available seats
        self.travel_option.available_seats = 0
        self.travel_option.save()
        self.assertFalse(self.travel_option.is_available)


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        try:
            profile = UserProfile.objects.get(user=self.user)
            self.assertEqual(profile.user, self.user)
        except UserProfile.DoesNotExist:
            self.fail("UserProfile was not created for the user")


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.travel_option = TravelOption.objects.create(
            travel_id='FL001',
            travel_type='flight',
            source='New York',
            destination='Los Angeles',
            departure_date=date.today() + timedelta(days=2),
            departure_time=time(10, 0),
            arrival_date=date.today() + timedelta(days=2),
            arrival_time=time(13, 0),
            price=299.99,
            available_seats=50,
            total_seats=100
        )
    
    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            passenger_names='John Doe, Jane Doe',
            contact_email='test@example.com',
            contact_phone='123-456-7890'
        )
        
        self.assertIsNotNone(booking.booking_id)
        self.assertEqual(booking.total_price, 599.98)  # 299.99 * 2
        self.assertEqual(booking.status, 'confirmed')
    
    def test_can_cancel_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            passenger_names='John Doe, Jane Doe',
            contact_email='test@example.com',
            contact_phone='123-456-7890'
        )
        
        self.assertTrue(booking.can_cancel())


class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'wrongpass'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class BookingFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.travel_option = TravelOption.objects.create(
            travel_id='FL001',
            travel_type='flight',
            source='New York',
            destination='Los Angeles',
            departure_date=date.today() + timedelta(days=1),
            departure_time=time(10, 0),
            arrival_date=date.today() + timedelta(days=1),
            arrival_time=time(13, 0),
            price=299.99,
            available_seats=5,
            total_seats=100
        )
    
    def test_valid_booking_form(self):
        form_data = {
            'number_of_seats': 2,
            'passenger_names': 'John Doe, Jane Doe',
            'contact_email': 'test@example.com',
            'contact_phone': '123-456-7890'
        }
        form = BookingForm(
            data=form_data,
            travel_option=self.travel_option,
            user=self.user
        )
        self.assertTrue(form.is_valid())
    
    def test_too_many_seats(self):
        form_data = {
            'number_of_seats': 10,  # More than available
            'passenger_names': 'John Doe, Jane Doe',
            'contact_email': 'test@example.com',
            'contact_phone': '123-456-7890'
        }
        form = BookingForm(
            data=form_data,
            travel_option=self.travel_option,
            user=self.user
        )
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.travel_option = TravelOption.objects.create(
            travel_id='FL001',
            travel_type='flight',
            source='New York',
            destination='Los Angeles',
            departure_date=date.today() + timedelta(days=1),
            departure_time=time(10, 0),
            arrival_date=date.today() + timedelta(days=1),
            arrival_time=time(13, 0),
            price=299.99,
            available_seats=50,
            total_seats=100
        )
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Travel Lykk')
    
    def test_travel_options_view(self):
        response = self.client.get(reverse('travel_options'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FL001')
    
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/login/?next=/profile/')
    
    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_book_travel_requires_login(self):
        response = self.client.get(reverse('book_travel', args=[self.travel_option.pk]))
        self.assertRedirects(response, f'/login/?next=/book/{self.travel_option.pk}/')
    
    def test_book_travel_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('book_travel', args=[self.travel_option.pk]))
        self.assertEqual(response.status_code, 200)
