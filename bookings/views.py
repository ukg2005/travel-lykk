from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.db import transaction
from .models import TravelOption, Booking, UserProfile
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm, TravelSearchForm, BookingForm


def home(request):
    form = TravelSearchForm(request.GET or None)
    travel_options = TravelOption.objects.filter(
        departure_date__gte=timezone.now().date(),
        available_seats__gt=0
    )
    
    if form.is_valid():
        travel_type = form.cleaned_data.get('travel_type')
        source = form.cleaned_data.get('source')
        destination = form.cleaned_data.get('destination')
        departure_date = form.cleaned_data.get('departure_date')
        
        if travel_type:
            travel_options = travel_options.filter(travel_type=travel_type)
        if source:
            travel_options = travel_options.filter(source__icontains=source)
        if destination:
            travel_options = travel_options.filter(destination__icontains=destination)
        if departure_date:
            travel_options = travel_options.filter(departure_date=departure_date)
    
    paginator = Paginator(travel_options, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookings/home.html', {
        'form': form,
        'page_obj': page_obj,
        'travel_options': page_obj,
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to ZipGo!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    return render(request, 'bookings/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def travel_options(request):
    form = TravelSearchForm(request.GET or None)
    travel_options_qs = TravelOption.objects.filter(
        departure_date__gte=timezone.now().date(),
        available_seats__gt=0
    )
    
    if form.is_valid():
        travel_type = form.cleaned_data.get('travel_type')
        source = form.cleaned_data.get('source')
        destination = form.cleaned_data.get('destination')
        departure_date = form.cleaned_data.get('departure_date')
        
        if travel_type:
            travel_options_qs = travel_options_qs.filter(travel_type=travel_type)
        if source:
            travel_options_qs = travel_options_qs.filter(source__icontains=source)
        if destination:
            travel_options_qs = travel_options_qs.filter(destination__icontains=destination)
        if departure_date:
            travel_options_qs = travel_options_qs.filter(departure_date=departure_date)
    
    paginator = Paginator(travel_options_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookings/travel_options.html', {
        'form': form,
        'page_obj': page_obj,
        'travel_options': page_obj,
    })


@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, id=travel_id)
    
    if not travel_option.is_available:
        messages.error(request, 'This travel option is no longer available.')
        return redirect('travel_options')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel_option, user=request.user)
        if form.is_valid():
            with transaction.atomic():
                travel_option.refresh_from_db()
                if form.cleaned_data['number_of_seats'] > travel_option.available_seats:
                    messages.error(request, 'Not enough seats available.')
                    return redirect('book_travel', travel_id=travel_id)
                
                booking = form.save(commit=False)
                booking.user = request.user
                booking.travel_option = travel_option
                booking.total_price = travel_option.price * booking.number_of_seats
                booking.save()
                
                travel_option.available_seats -= booking.number_of_seats
                travel_option.save()
                
                messages.success(request, f'Booking confirmed! Your booking ID is {booking.booking_id}')
                return redirect('my_bookings')
    else:
        form = BookingForm(travel_option=travel_option, user=request.user)
    
    return render(request, 'bookings/book_travel.html', {
        'form': form,
        'travel_option': travel_option,
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookings/my_bookings.html', {
        'page_obj': page_obj,
        'bookings': page_obj,
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if not booking.can_cancel():
        messages.error(request, 'This booking cannot be cancelled. Cancellation is only allowed 24 hours before departure.')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        with transaction.atomic():
            travel_option = booking.travel_option
            travel_option.available_seats += booking.number_of_seats
            travel_option.save()
            
            booking.status = 'cancelled'
            booking.save()
            
            messages.success(request, f'Booking {booking.booking_id} has been cancelled successfully.')
        return redirect('my_bookings')
    
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})


def booking_detail(request, booking_id):
    if request.user.is_authenticated:
        booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    else:
        booking = get_object_or_404(Booking, booking_id=booking_id)
    
    return render(request, 'bookings/booking_detail.html', {'booking': booking})
