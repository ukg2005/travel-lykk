from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Booking, TravelOption


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class TravelSearchForm(forms.Form):
    TRAVEL_TYPE_CHOICES = [
        ('', 'All Types'),
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]
    
    travel_type = forms.ChoiceField(
        choices=TRAVEL_TYPE_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    source = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'From'})
    )
    destination = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To'})
    )
    departure_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats', 'passenger_names', 'contact_email', 'contact_phone']
        widgets = {
            'number_of_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'passenger_names': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Enter passenger names separated by commas (e.g., John Doe, Jane Smith)'
            }),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['contact_email'].initial = self.user.email
            if hasattr(self.user, 'userprofile'):
                self.fields['contact_phone'].initial = self.user.userprofile.phone_number
    
    def clean_number_of_seats(self):
        number_of_seats = self.cleaned_data['number_of_seats']
        if self.travel_option and number_of_seats > self.travel_option.available_seats:
            raise forms.ValidationError(
                f"Only {self.travel_option.available_seats} seats are available."
            )
        return number_of_seats
    
    def clean_passenger_names(self):
        passenger_names = self.cleaned_data['passenger_names']
        names = [name.strip() for name in passenger_names.split(',') if name.strip()]
        number_of_seats = self.cleaned_data.get('number_of_seats', 0)
        
        if len(names) != number_of_seats:
            raise forms.ValidationError(
                f"Please provide exactly {number_of_seats} passenger name(s)."
            )
        
        return ', '.join(names)
