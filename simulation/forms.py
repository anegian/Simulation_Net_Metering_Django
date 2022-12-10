from django import forms

class CalculatorForm(forms.Form):
    first_name = forms.CharField(label='First Name:', max_length=100)
    last_name = forms.CharField(label='Last Name:', max_length=100)
    email = forms.EmailField(label='Email:')
