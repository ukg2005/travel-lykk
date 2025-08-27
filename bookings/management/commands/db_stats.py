from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import TravelOption, Booking


class Command(BaseCommand):
    help = 'Display database statistics'

    def handle(self, *args, **options):
        users_count = User.objects.count()
        travel_options_count = TravelOption.objects.count()
        bookings_count = Booking.objects.count()
        
        flights_count = TravelOption.objects.filter(travel_type='flight').count()
        trains_count = TravelOption.objects.filter(travel_type='train').count()
        buses_count = TravelOption.objects.filter(travel_type='bus').count()
        
        confirmed_bookings = Booking.objects.filter(status='confirmed').count()
        cancelled_bookings = Booking.objects.filter(status='cancelled').count()
        pending_bookings = Booking.objects.filter(status='pending').count()
        
        self.stdout.write(self.style.SUCCESS('\n=== TRAVEL LYKK DATABASE STATISTICS ===\n'))
        
        self.stdout.write(f'👥 Total Users: {users_count}')
        self.stdout.write(f'✈️  Total Travel Options: {travel_options_count}')
        self.stdout.write(f'   - Flights: {flights_count}')
        self.stdout.write(f'   - Trains: {trains_count}')
        self.stdout.write(f'   - Buses: {buses_count}')
        
        self.stdout.write(f'\n🎫 Total Bookings: {bookings_count}')
        self.stdout.write(f'   - Confirmed: {confirmed_bookings}')
        self.stdout.write(f'   - Cancelled: {cancelled_bookings}')
        self.stdout.write(f'   - Pending: {pending_bookings}')
        
        total_available_seats = sum(opt.available_seats for opt in TravelOption.objects.all())
        self.stdout.write(f'\n💺 Total Available Seats: {total_available_seats}')
        
        self.stdout.write(self.style.SUCCESS('\n=== END STATISTICS ===\n'))
