from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, date, time, timedelta
from bookings.models import TravelOption
import uuid


class Command(BaseCommand):
    help = 'Create sample travel options for testing'

    def handle(self, *args, **options):
        TravelOption.objects.all().delete()
        
        cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
            'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte'
        ]
        
        travel_types = ['flight', 'train', 'bus']
        
        created_count = 0
        
        for i in range(50):
            import random
            source = random.choice(cities)
            destination = random.choice([city for city in cities if city != source])
            travel_type = random.choice(travel_types)
            
            departure_date = timezone.now().date() + timedelta(days=random.randint(1, 90))
            
            departure_hour = random.randint(6, 22)
            departure_minute = random.choice([0, 15, 30, 45])
            departure_time = time(departure_hour, departure_minute)
            
            travel_duration = timedelta(hours=random.randint(1, 8))
            departure_datetime = datetime.combine(departure_date, departure_time)
            arrival_datetime = departure_datetime + travel_duration
            
            travel_id = f"{travel_type.upper()[:2]}{str(uuid.uuid4())[:6].upper()}"
            
            if travel_type == 'flight':
                base_price = random.randint(150, 800)
            elif travel_type == 'train':
                base_price = random.randint(50, 300)
            else:
                base_price = random.randint(25, 150)
            
            total_seats = random.choice([30, 40, 50, 60, 80, 100])
            available_seats = random.randint(int(total_seats * 0.2), total_seats)
            
            travel_option = TravelOption.objects.create(
                travel_id=travel_id,
                travel_type=travel_type,
                source=source,
                destination=destination,
                departure_date=departure_date,
                departure_time=departure_time,
                arrival_date=arrival_datetime.date(),
                arrival_time=arrival_datetime.time(),
                price=base_price,
                available_seats=available_seats,
                total_seats=total_seats
            )
            
            created_count += 1
            
            if created_count % 10 == 0:
                self.stdout.write(f'Created {created_count} travel options...')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample travel options!')
        )
