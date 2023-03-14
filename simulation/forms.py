from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class PlaceForm(ModelForm):
    class Meta:
        model = PlaceOfInstallation
        fields = '__all__'

class PlaceOfInstallationForm(forms.Form):
    DISTRICT_CHOICES = [
        ('district', 'Περιφέρεια'),
        ('attiki', 'Αττική'),
        ('anatoliki_makedonia_thraki', 'Ανατολική Μακεδονία & Θράκη'),
        ('vorio_aigaio', 'Βόρειο Αιγαίο'),
        ('dytiki_ellada', 'Δυτική Ελλάδα'),
        ('dytiki_makedonia', 'Δυτική Μακεδονία'),
        ('ipeiros', 'Ήπειρος'),
        ('thessalia', 'Θεσσαλία'),
        ('ionioi_nisoi', 'Ιόνιοι Νήσοι'),
        ('kentriki_makedonia', 'Κεντρική Μακεδονία'),
        ('kriti', 'Κρήτη'),
        ('notio_aigaio', 'Νότιο Αιγαίο'),
        ('peloponnisos', 'Πελοπόννησος'),
        ('sterea_ellada', 'Στερεά Ελλάδα'),
    ]

    PHASE_LOAD = [('phase_load', 'Παροχή'), ('single_phase', 'Μονοφασική'), ('3_phase', 'Τριφασική'), ]

    select_district = forms.ChoiceField(choices=DISTRICT_CHOICES, label='Επιλέξτε Περιφέρεια και Παροχή',
                                        initial='district')
    select_phase = forms.ChoiceField(choices=PHASE_LOAD, initial='phase_load')


""""
    class Meta:
        model = PlaceOfInstallation
        fields = ('district_name', 'city_name', 'district_code')
        widgets = {
            'district_name': forms.TextInput(attrs={'class': 'form-control'}),
            'city_name': forms.TextInput(attrs={'class': 'form-control'}),
            'district_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district_name'].label = 'District Name'
        self.fields['city_name'].label = 'City Name'
        self.fields['district_code'].label = 'District Code'
"""""

class EnergyConsumptionForm(forms.Form):
    KWh_CHOICES = [
        ('annual_kW', 'KWh σε ετήσια βάση'),
        ('1500', '1500-2000'),
        ('2000', '2000-2500'),
        ('2500', '2500-3500'),
        ('3000', '3500-4500'),
    ]
    select_kwh = forms.ChoiceField(choices=KWh_CHOICES, label='Επιλέξτε KWh', initial = 'annual_kW')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ('old_password', 'new_password1', 'new_password2')

        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Current Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'
