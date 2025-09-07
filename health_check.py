#!/usr/bin/env python

import os
import sys
import django
from django.core.management import execute_from_command_line

project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_booking.settings')

django.setup()

from django.contrib.auth.models import User
from bookings.models import TravelOption, Booking, UserProfile
from django.test.client import Client
from django.urls import reverse


def test_database_connectivity():
    print("🔍 Testing database connectivity...")
    try:
        users_count = User.objects.count()
        travel_count = TravelOption.objects.count()
        bookings_count = Booking.objects.count()
        
        print(f"  ✅ Database connected successfully")
        print(f"  📊 Users: {users_count}, Travel Options: {travel_count}, Bookings: {bookings_count}")
        return True
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False


def test_url_patterns():
    print("\n🌐 Testing URL patterns...")
    client = Client()
    
    urls_to_test = [
        ('home', 200),
        ('travel_options', 200),
        ('login', 200),
        ('register', 200),
    ]
    
    all_passed = True
    for url_name, expected_status in urls_to_test:
        try:
            url = reverse(url_name)
            response = client.get(url)
            if response.status_code == expected_status:
                print(f"  ✅ {url_name} ({url}): {response.status_code}")
            else:
                print(f"  ❌ {url_name} ({url}): Expected {expected_status}, got {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"  ❌ {url_name}: Error - {e}")
            all_passed = False
    
    return all_passed


def test_models():
    print("\n📋 Testing models...")
    try:
        sample_travel = TravelOption.objects.first()
        if sample_travel:
            print(f"  ✅ TravelOption model working - Sample: {sample_travel.travel_id}")
        else:
            print("  ⚠️  No travel options found - run 'python manage.py create_sample_data'")
        
        admin_users = User.objects.filter(is_superuser=True)
        if admin_users.exists():
            print(f"  ✅ User model working - Admin users: {admin_users.count()}")
        else:
            print("  ⚠️  No admin users found - run 'python manage.py createsuperuser'")
        
        return True
    except Exception as e:
        print(f"  ❌ Model test failed: {e}")
        return False


def test_template_rendering():
    print("\n🎨 Testing template rendering...")
    client = Client()
    
    try:
        response = client.get(reverse('home'))
        if 'ZipGo' in response.content.decode():
            print("  ✅ Templates rendering correctly")
            return True
        else:
            print("  ❌ Template content not found")
            return False
    except Exception as e:
        print(f"  ❌ Template rendering failed: {e}")
        return False


def test_static_files():
    print("\n📁 Testing static files...")
    from django.conf import settings
    
    try:
        static_url = settings.STATIC_URL
        static_root = getattr(settings, 'STATIC_ROOT', None)
        
        print(f"  ✅ STATIC_URL: {static_url}")
        if static_root:
            print(f"  ✅ STATIC_ROOT: {static_root}")
        else:
            print("  ⚠️  STATIC_ROOT not set - needed for production")
        
        return True
    except Exception as e:
        print(f"  ❌ Static files test failed: {e}")
        return False


def main():
    print("🏥 TRAVEL LYKK HEALTH CHECK")
    print("=" * 50)
    
    tests = [
        test_database_connectivity,
        test_url_patterns,
        test_models,
        test_template_rendering,
        test_static_files,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🏁 HEALTH CHECK COMPLETE: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems operational!")
        return 0
    else:
        print("⚠️  Some issues detected. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
