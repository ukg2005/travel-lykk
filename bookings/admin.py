from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import TravelOption, UserProfile, Booking


@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ['travel_id', 'travel_type', 'source', 'destination', 'departure_date', 'departure_time', 'price', 'available_seats']
    list_filter = ['travel_type', 'source', 'destination', 'departure_date']
    search_fields = ['travel_id', 'source', 'destination']
    ordering = ['departure_date', 'departure_time']
    list_editable = ['price', 'available_seats']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'date_of_birth']
    search_fields = ['user__username', 'user__email', 'phone_number']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'travel_option', 'number_of_seats', 'total_price', 'status', 'booking_date']
    list_filter = ['status', 'booking_date', 'travel_option__travel_type']
    search_fields = ['booking_id', 'user__username', 'travel_option__travel_id']
    readonly_fields = ['booking_id', 'total_price', 'booking_date']
    ordering = ['-booking_date']


# Extend User admin to include profile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
